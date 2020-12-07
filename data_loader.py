import numpy as np
from tqdm import tqdm
import torch
from torch.utils import data
from transformers import PhobertTokenizer
tokenizer = PhobertTokenizer.from_pretrained("vinai/phobert-base")

from vncorenlp import VnCoreNLP
rdrsegmenter = VnCoreNLP("vncorenlp/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m') 
pad_idx  = tokenizer.pad_token_id

from sklearn.preprocessing import LabelEncoder

all_labels = ['angry', 'annoyed', 'furious', 'disgusted', 'confident', 'prepared', 
              'excited', 'surprised', 'impressed', 'hopeful', 'faithful', 'trusting', 'proud', 'joyful', 'content',
              'sentimental', 'grateful', 'caring',
              'guilty', 'ashamed', 'embarrassed', 'afraid', 'terrified', 'anticipating', 'apprehensive','anxious',
              'sad', 'disappointed', 'nostalgic', 'devastated', 'lonely', 'jealous']

numOfLabels = len(all_labels)
lbEnc = LabelEncoder()
lbEnc.fit(all_labels)

def preprocess(text, split_sep = " "):
    return (
        text.replace(".", " . ")
        .replace("_comma_", " , ")
        .replace(". . .", " ... ")
        .replace(",", " , ")
        .replace(";", " ; ")
        .replace(":", " : ")
        .replace("'", " ' ")
        .replace("''", " \" ")
        .replace("!", " ! ")
        .replace("?", " ? ")
        .replace("  ", " ")
        .replace("  ", " ")
        .strip()
        .lower()
    )

def txt2vec(text, max_tokens_len):
    sentence = preprocess(text)
 
    word_segmented_text = rdrsegmenter.tokenize(sentence) 
    prevsent = []
   
    for i in word_segmented_text:
        prevsent += i
        
    subwords = '<s> ' + " ".join(prevsent) + ' </s>' 
   
    #text to tensor
    input_ids = tokenizer.encode(subwords, add_special_tokens = False)[-max_tokens_len:]
    return torch.LongTensor([input_ids])
   
def batchify(batch):
        
        input_list = list(zip(*batch))
        contexts, next_ = [
            pad(ex, pad_idx) for ex in [input_list[0], input_list[1]]
        ]
        
        # return contexts, next_, torch.tensor(lbEnc.transform(input_list[2]), dtype=torch.long)
        return contexts, next_, input_list[2]

def pad(tensors, padding_value=-1, max_len = 256):
    """
    Concatenate and pad the input tensors, which may be 1D or 2D.
    """

    max_len = max(t.size(-1) for t in tensors) 

    if tensors[0].dim() == 1:
        out = torch.LongTensor(len(tensors), max_len).fill_(padding_value)
        for i, t in enumerate(tensors):
            out[i, : t.size(0)] = t
        return out
    elif tensors[0].dim() == 2:
        max_width = max(t.size(0) for t in tensors)
        out = torch.LongTensor(len(tensors), max_width, max_len).fill_(padding_value)
        for i, t in enumerate(tensors):
            out[i, : t.size(0), : t.size(1)] = t
        return out
    else:
        raise ValueError("Input tensors must be either 1D or 2D!")


class EmpDataset(data.Dataset):
    def __init__(
        self,
        splitname,
        maxlen=256, # max number of tokens per sentence
        history_len=2,
        prepend = True, # add label as prefix
        over_sample = True
    ):
    
        df = open(f"{splitname}.csv", "r" ,encoding="utf-8").readlines()
        
        self.max_hist_len = history_len * 2 - 1
        self.data = []
        history = []
        for i in tqdm(range(1, len(df))):
             
            cparts = df[i - 1].strip().split(",")
            sparts = df[i].strip().split(",")
            if cparts[0] == sparts[0]:
                
                history.append(cparts[5])
                idx = int(sparts[1])
                if (idx % 2) == 0:
                    # Lay cac turn cuoi
                    # SOC start of comment
                    if prepend:
                        emo = str( lbEnc.transform([sparts[2]])[0])
                        sentence2 = emo + " " + sparts[5]
                    else:
                        sentence2 = sparts[5]
                    
                    if over_sample:
                        history[-1] = history[-1].replace("?", "").replace("!", "").strip()
                        #if(len(history) == 1):
                        self.data.append([txt2vec(history[-1], maxlen), txt2vec(sentence2, maxlen), sparts[2]])
                        
                        sentence1 = " | ".join(history[-self.max_hist_len :]) 
                        if(len(history) != 1):
                            self.data.append([txt2vec(sentence1, maxlen), txt2vec(sentence2, maxlen), sparts[2]])
                        
                    else:
                        history[-1] = history[-1].replace("?", "").replace("!", "").strip()
                        sentence1 = " | ".join(history[-self.max_hist_len :]) 
                        self.data.append([txt2vec(sentence1, maxlen), txt2vec(sentence2, maxlen), sparts[2]])
                        
            else:
                history = []
        
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]