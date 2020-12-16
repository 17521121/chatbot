from torch.utils import data
import torch
import numpy as np
from model import Net
from data_loader import *
from functions import *
from chuyendoidaitu import *
from duytridoithoai import *


device = 'cuda' if torch.cuda.is_available() else 'cpu'
max_tokens_length = 256


class Args():
  def __init__(self):
    self.max_turn = 2
    self.over_sample = True  # turn 1 + turn 2
    self.normalize = True   # True: target = dot - norm | False: target = dot product
    self.prepend = True     # emo prepend
    self.stop_crit_num_epochs = 5  # early stop
    self.learning_rate = 1e-5
    self.epochs = 30
    self.hits_at_nb_cands = 100  # p@1,100
    self.display_iter = 100  # help="Frequency of train logging"
    self.batch_size = 32
    self.optimizer = "adamax"
    self.train = False  # Train or evaluate
    self.log_file = "logs/phobert_normalize_finetuned.txt"
    self.model_file = "models/phobert_normalize_finetuned.pt"


option = Args()
logger = get_logger(option)

# -----------------------
net = Net(device, False)

if device == "cuda":
  torch.cuda.set_device(-1)  # get the lastest device (GPU)
  net = torch.nn.DataParallel(net)
  net.cuda()

net.load_state_dict(torch.load(option.model_file), strict=False)
# net.load_state_dict(torch.load("models/phobert_auto.pt"), strict = False)
net.eval()

# --------------------------------
all_cands = torch.load("torch_pre_load/all_cands_finetuned_normalize.pth")
train_iter = torch.load("torch_pre_load/train_iter.pth")
# --------------------------------


class TextData(data.Dataset):
    def __init__(
        self,
        splitname,
        maxlen=256,  # max number of tokens per sentence
        history_len=2,
        prepend=True,  # add label as prefix
        over_sample=False
    ):

        df = open(f"{splitname}.csv", "r", encoding="utf-8").readlines()
        self.max_hist_len = history_len * 2 - 1
        self.data = []
        history = []
        for i in tqdm(range(1, len(df))):

            cparts = df[i - 1].strip().split(",")
            sparts = df[i].strip().split(",")
            if cparts[0] == sparts[0]:

                history.append(preprocess(cparts[5]))
                idx = int(sparts[1])
                if (idx % 2) == 0:
                    # Lay cac turn cuoi
                    # SOC start of comment
                    sentence2 = preprocess(sparts[5])

                    if over_sample:
                        history[-1] = history[-1].replace(
                            "?", "").replace("!", "").strip()
                        # if(len(history) == 1):
                        self.data.append([history[-1], sentence2, sparts[2]])
                        sentence1 = " | ".join(history[-self.max_hist_len:])
                        if(len(history) != 1):
                            self.data.append([sentence1, sentence2, sparts[2]])

                    else:
                        history[-1] = history[-1].replace(
                            "?", "").replace("!", "").strip()
                        sentence1 = " | ".join(history[-self.max_hist_len:])
                        self.data.append([sentence1, sentence2, sparts[2]])
            else:
                history = []

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


train_dataset = TextData(
    "ED/train_manual",
    maxlen=max_tokens_length,
    history_len=option.max_turn,
    prepend=option.prepend,
    over_sample=option.train and option.over_sample
)

# --------------------------------


def predict(context, top_n=5, normalize=True):
    """
    returns a list of top_n tuples ("sentence", "score")
    """

    all_input_ids = txt2vec(context, 256)
    with torch.no_grad():
        if device == "cuda":
            all_input_ids = all_input_ids.cuda(non_blocking=True)

        ctx = net(all_input_ids)
        scores, index = score_candidates(ctx, all_cands, top_n, normalize)
        response = []
        for i, (score, index) in enumerate(zip(scores.squeeze(0), index.squeeze(0)), 1):
            response.append((train_dataset[index], float(score)))

        return response


def clean_answer(outs):
    return outs[0][0][1], outs[0][0][2]


# n1 = ["tôi", "bạn"]
# n2 = ["mẹ", "con"]
# his = []
# while 1:
#     chat_text = input()
#     chat_text = convert_sentence(chat_text, n1[0], n1[1])

#     if chat_text  in user_hello:
#         out = hello_user()
#     elif chat_text in user_say_bye:
#         out = bye_user()
#     else:
#         his.append(chat_text)
#         outs = predict(" | ".join(his[-1:]), top_n = 3, normalize = option.normalize)
#         out, emo_text = clean_answer(outs)
#         his.append(out)

#     out = revert_sentence(out, n2[0], n2[1]) 
#     out = '. '.join(i.capitalize() for i in out.split(' . '))
#     print(out)
