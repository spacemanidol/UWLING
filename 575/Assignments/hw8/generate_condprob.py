import numpy as np
import torch
import sys

from pytorch_pretrained_bert import GPT2LMHeadModel, GPT2Tokenizer

class LM():
    def __init__(self,GPU, model_name_or_path="gpt2"):
        self.device = torch.device(GPU if torch.cuda.is_available() else "cpu")
        self.enc = GPT2Tokenizer.from_pretrained(model_name_or_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.model.eval()
        self.start_token = '<|endoftext|>'
        print("Loaded GPT-2 model!")
    def generate_conditionalprobs(self, x,y):
        in_text = ' '.join([x]+[y])
        start_t = torch.full((1, 1),self.enc.encoder[self.start_token], device=self.device, dtype=torch.long)
        context = self.enc.encode(in_text)
        context = torch.tensor(context, device=self.device, dtype=torch.long).unsqueeze(0)
        context = torch.cat([start_t, context], dim=1)
        logits, _ = self.model(context)
        yhat = torch.softmax(logits[0, :-1], dim=-1)
        y = context[0, 1:]
        sorted_preds = np.argsort(-yhat.data.cpu().numpy())
        real_topk_probs = yhat[np.arange(0, y.shape[0], 1), y].data.cpu().numpy().tolist()
        torch.cuda.empty_cache()
        return real_topk_probs[-1]

def read_probs(filename):
    probs = {}
    with open(filename,'r') as f:
        for l in f:
            l = l.strip().split()
            if len(l) > 2:
                probs[(l[0],l[1])] = l[2]
    return probs

def read_pairs(filename, probs):
    pairs = {}
    i = 0
    with open(filename,'r') as f:
        for l in f:
            i += 1
            l = l.strip().split()
            if len(l) > 1:
                if (l[0], l[1]) not in probs:
                    pairs[(l[0],l[1])] = 0
    print('{} probabilities loaded and {} already exist. Calculating remaining {} condprobs'.format(i, len(probs),len(pairs)))
    return pairs

def join(probs, probs2, filename):
    joint = {}
    for p in probs:
        joint[p] = probs[p]
    for p in probs2:
        joint[p] = probs2[p]
    with open(filename,'w') as w:
        for p in joint:
            w.write('{} {} {}\n'.format(p[0],p[1],joint[p]))
    return joint

def generate_condprob(probs,filename,GPU):
    lm = LM(GPU)
    i = 0
    with open('output'+filename,'w') as w:
        for p in pairs:
            if i %10000 == 0:
                print("Generated {} pairs".format(i))
            probs[(p[0],p[1])] = lm.generate_conditionalprobs(p[0],p[1])
            i+= 1
            w.write("{} {} {}\n".format(p[0],p[1],probs[(p[0],p[1])]))

if __name__ == '__main__':
     if len(sys.argv) < 4:
        print("Usage:python generate_condprobs.py <probs> <pairs> <GPU cuda:0>")
        exit(-1)
    else:
        probs = read_probs(sys.argv[1])
        pairs = read_pairs(sys.argv[2], probs)
        generate_condprob(probs,sys.argv[2],sys.argv[3])
