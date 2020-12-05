from model import Net
from data_loader import *
from functions import *

device = 'cuda' if torch.cuda.is_available() else 'cpu'
max_tokens_length = 256
 
class Args():
  def __init__(self):
    self.max_turn = 2
    self.over_sample = True # turn 1 + turn 2
    self.normalize = True   # True: target = dot - norm | False: target = dot product
    self.prepend = True     # emo prepend
    self.stop_crit_num_epochs = 5 # early stop
    self.learning_rate = 1e-5
    self.epochs = 30
    self.hits_at_nb_cands = 100 # p@1,100
    self.display_iter = 100 # help="Frequency of train logging"
    self.batch_size = 32
    self.optimizer = "adamax"
    self.train = False  # Train or evaluate
    self.log_file = "logs/phobert_normalize_finetuned.txt"
    self.model_file = "models/phobert_normalize_finetuned.pt"

option = Args()
logger = get_logger(option)

#-----------------------
net = Net(device, False)

if device == "cuda":
  torch.cuda.set_device(-1) # get the lastest device (GPU)
  net = torch.nn.DataParallel(net)
  net.cuda()
  
net.load_state_dict(torch.load(option.model_file), strict = False)
# net.load_state_dict(torch.load("models/phobert_auto.pt"), strict = False)
net.eval()
 
#--------------------------------
all_cands = torch.load("torch_pre_load/all_cands_finetuned_normalize.pth")
train_iter = torch.load("torch_pre_load/train_iter.pth")
#--------------------------------
train_dataset = []
with torch.no_grad():
    for i, ex in enumerate(train_iter):
        batch_size = ex[0].size(0)
        params = [
            field
            if field is not None
            else None
            for field in ex
        ]
        train_dataset.extend(params[1])

#--------------------------------
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
  return str.format("{}",tokenizer.decode(outs[0][0][0][2:-1])).replace("_", " ")