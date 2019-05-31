import sys

import numpy as np
import torch

from pytorch_pretrained_bert import GPT2LMHeadModel, GPT2Tokenizer

class LM():
    def __init__(self, model_name_or_path="gpt2"):
        #super(LM, self).__init__()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
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

def loadfile(filename):
    tasks = []
    with open(filename,'r') as f:
        for l in f:
            l = l.strip().split()
            tasks.append((l[0],l[1]))
    return tasks

if __name__ == '__main__':
    lm = LM()
    pairs = loadfile(sys.argv[1])
    print('there are {} tasks'.format(len(pairs)))
    i = 0
    with open('output'+sys.argv[1],'w') as w:
        for p in pairs:
            if i %10000 == 0:
                print("{} examples done".format(i))
            i += 1
            w.write('{}\t{}\t{}\n'.format(p[0],p[1],lm.generate_conditionalprobs(p[0],p[1])))
