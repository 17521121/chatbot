import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import os
import numpy as np
from transformers import AdamW, get_linear_schedule_with_warmup, get_constant_schedule
import time
import torch.nn.functional as F
import math
import logging
import sys
import json

def get_logger(opt):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s: [ %(message)s ]", "%m/%d/%Y %I:%M:%S %p")
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.handlers = []
    logger.addHandler(console)
    if opt.log_file:
        logfile = logging.FileHandler(opt.log_file, "a")
        logfile.setFormatter(fmt)
        logger.addHandler(logfile)
    command = " ".join(sys.argv)
    # logger.info(f"COMMAND: {command}")
    # logger.info("-" * 100)
    config = json.dumps(vars(opt), indent=4, sort_keys=True)
    logger.info(f"CONFIG:\n{config}")
    return logger


def score_candidates(all_context, all_cands, top_k=20, normalize = True):
    if normalize:
        dot_products = all_context.mm(all_cands.t())  # [ctx, cand]
        all_context = all_context.unsqueeze(1)
        dot_products -=  (all_context - all_cands).norm(2, -1)
    else:
        dot_products = all_context.mm(all_cands.t())  # [ctx, cand]
        
    scores, answers = dot_products.topk(top_k, dim=1)
    # Index of top-k items in decreasing order. Answers is of size [ctx, top_k]
    return scores, answers

def loss_fn(ctx, labels, normalize = True):
    batch_size = ctx.size(0)
    if normalize:
        dot_products = ctx.mm(labels.t())
        ctx = ctx.unsqueeze(1)
        dot_products -= ctx.subtract(labels).norm(2, -1)
    else:
        dot_products = ctx.mm(labels.t())
        
    log_prob = F.log_softmax(dot_products, dim=1)
    targets = log_prob.new_empty(batch_size).long()
    targets = torch.arange(batch_size, out=targets)
    loss = F.nll_loss(log_prob, targets)
    nb_ok = (log_prob.max(dim=1)[1] == targets).float().sum()
    return loss, nb_ok


def train(epoch, start_time, model, optimizer, opt, data_loader, normalize = True):
    """Run through one epoch of model training with the provided data loader."""
    model.train()
    # Initialize meters + timers
    train_loss = 0
    nb_ok = 0
    nb_exs = 0
    nb_losses = 0
    epoch_start = time.time()
    # Run one epoch
    for idx, ex in enumerate(data_loader, 1):
        params = [
            field
            if field is not None
            else None
            for field in ex
        ]
        ctx = model(params[0][:,0,:])
        cands = model(params[1][:,0,:])
        loss, ok = loss_fn(ctx, cands, normalize = normalize)
        nb_ok += ok
        nb_exs += ex[0].size(0)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_loss += loss.sum().item()
        nb_losses += 1
        if idx % opt.display_iter == 0 or idx == len(data_loader):
            avg_loss = train_loss / nb_losses
            acc = 100 * nb_ok / nb_exs
            elapsed = time.time() - start_time
            logging.info(
                f"train: Epoch = {epoch} | iter = {idx}/{len(data_loader)} | loss = "
                f"{avg_loss:.3f} | batch P@1 = {acc:.2f} % | elapsed time = "
                f"{elapsed:.2f} (s)"
            )
            train_loss = 0
            nb_losses = 0
    epoch_elapsed = time.time() - epoch_start
    logging.info(
        f"train: Epoch {epoch:d} done. Time for epoch = {epoch_elapsed:.2f} (s)"
    )


def validate(
    epoch,
    model,
    data_loader,   
    is_test=False,
    nb_candidates=100,
    shuffle="shuffled",
    normalize = True
):
    model.eval()
    examples = 0
    eval_start = time.time()
    sum_losses = 0
    n_losses = 0
    correct = 0
    all_context = []
    all_cands = []
    n_skipped = 0
   
    for i, ex in enumerate(data_loader):
        batch_size = ex[0].size(0)
        
        params = [
            field
            if field is not None
            else None
            for field in ex
        ]
        # ctx, cands = model(*params)
        ctx = model(params[0][:,0,:])
        cands = model(params[1][:,0,:])
        all_context.append(ctx)
        all_cands.append(cands)
        loss, nb_ok = loss_fn(ctx, cands, normalize = normalize)
        sum_losses += loss
        correct += nb_ok
        n_losses += 1
        examples += batch_size
        
    n_examples = 0
    if len(all_context) > 0:
        logging.info("Processing candidate top-K")
        all_context = torch.cat(all_context, dim=0)  # [:50000]  # [N, 2h]
        all_cands = torch.cat(all_cands, dim=0)  # [:50000]  # [N, 2h]
        acc_ranges = [1, 3, 10]
        n_correct = {r: 0 for r in acc_ranges}
        for context, cands in list(
            zip(all_context.split(nb_candidates), all_cands.split(nb_candidates))
        )[:-1]:
            _, top_answers = score_candidates(context, cands, normalize = normalize)
            n_cands = cands.size(0)
            gt_index = torch.arange(n_cands, out=top_answers.new(n_cands, 1))
            for acc_range in acc_ranges:
                n_acc = (top_answers[:, :acc_range] == gt_index).float().sum()
                n_correct[acc_range] += n_acc
            n_examples += n_cands
        accuracies = {r: 100 * n_acc / n_examples for r, n_acc in n_correct.items()}
        avg_loss = sum_losses / (n_losses + 0.00001)
        avg_acc = 100 * correct / (examples + 0.000001)
        valid_time = time.time() - eval_start
        logging.info(
            f"Valid ({shuffle}): Epoch = {epoch:d} | avg loss = {avg_loss:.3f} | "
            f"batch P@1 = {avg_acc:.2f} % | "
            + f" | ".join(
                f"P@{k},{nb_candidates} = {v:.2f}%" for k, v in accuracies.items()
            )
            + f" | valid time = {valid_time:.2f} (s)"
        )
        return avg_loss
    return 10

  