import torch
import torch.nn as nn
from transformers import RobertaConfig
from transformers import RobertaModel

class Net(nn.Module):
    def __init__(self, device='cpu', pretrain = True):
        super().__init__()
        config = RobertaConfig.from_pretrained("vinai/phobert-base")
        if pretrain:
            self.roberta = RobertaModel.from_pretrained("vinai/phobert-base")
        else:
            self.roberta = RobertaModel(config)

        self.fc = nn.Linear(768, 300)
        self.device = device
       

    def forward(self, x):
        if self.device == "cuda":
            x = x.to(self.device, non_blocking=True)
        else:
            x = x.to(self.device)
        
        if self.training:
            self.roberta.train()
            enc = self.roberta(x)
        else:
            self.roberta.eval()
            with torch.no_grad():
                enc = self.roberta(x)
        
        # CLS
        enc = enc[0][:, 0, :]

        result  = self.fc(enc)
        return result

class CLS_Net(nn.Module):
    def __init__(self, numOfLabels, device='cpu', pretrain = True):
        super().__init__()
        config = RobertaConfig.from_pretrained("vinai/phobert-base")
        if pretrain:
            self.roberta = RobertaModel.from_pretrained("vinai/phobert-base")
        else:
            self.roberta = RobertaModel(config)

        self.fc1 = nn.Linear(768, 128)
        self.fc2 = nn.Linear(128, numOfLabels)
        self.device = device

    def forward(self, x):
        if self.device == "cuda":
            x = x.to(self.device, non_blocking=True)
        else:
            x = x.to(self.device)
        
        if self.training:
            self.roberta.train()
            enc, _ = self.roberta(x)
        else:
            self.roberta.eval()
            with torch.no_grad():
                enc, _ = self.roberta(x)
        
        # CLS
        enc = enc[:, 0, :]
        fc1 = self.fc1(enc)
        fc2  = self.fc2(fc1)
        return fc2
