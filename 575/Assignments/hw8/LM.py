import numpy as np
import torch

from pytorch_pretrained_bert import GPT2LMHeadModel, GPT2Tokenizer

class LM():
    def __init__(self, model_name_or_path="gpt2"):
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
    def check_probabilities(self, in_text, topk=40):
        # Process input
        start_t = torch.full((1, 1),self.enc.encoder[self.start_token], device=self.device, dtype=torch.long)
        context = self.enc.encode(in_text)
        context = torch.tensor(context, device=self.device, dtype=torch.long).unsqueeze(0)
        context = torch.cat([start_t, context], dim=1)
        # Forward through the model
        logits, _ = self.model(context)
        # construct target and pred
        yhat = torch.softmax(logits[0, :-1], dim=-1)
        y = context[0, 1:]
        sorted_preds = np.argsort(-yhat.data.cpu().numpy())
        real_topk_probs = yhat[np.arange(0, y.shape[0], 1), y].data.cpu().numpy().tolist()
        real_topk_probs = list(map(lambda x: round(x, 5), real_topk_probs))
        real_topk_pos = list([int(np.where(sorted_preds[i] == y[i].item())[0][0]) for i in range(y.shape[0])])
        real_topk = list(zip(real_topk_pos, real_topk_probs))
        bpe_strings = [self.enc.decoder[s.item()] for s in context[0]]
        bpe_strings = [self.postprocess(s) for s in bpe_strings]
        pred_topk = [list(zip([self.enc.decoder[p] for p in sorted_preds[i][:topk]],list(map(lambda x: round(x, 5),yhat[i][sorted_preds[i][:topk]].data.cpu().numpy().tolist())))) for i in range(y.shape[0])]
        pred_topk = [[(self.postprocess(t[0]), t[1]) for t in pred] for pred in pred_topk]
        payload = {'bpe_strings': bpe_strings, 'real_topk': real_topk,'pred_topk': pred_topk}
        torch.cuda.empty_cache()
        return payload
    def postprocess(self, token):
        with_space = False
        with_break = False
        if token.startswith('Ġ'):
            with_space = True
            token = token[1:]
        elif token.startswith('â'):
            token = ' '
        elif token.startswith('Ċ'):
            token = ' '
            with_break = True
        token = '-' if token.startswith('â') else token
        token = '“' if token.startswith('ľ') else token
        token = '”' if token.startswith('Ŀ') else token
        token = "'" if token.startswith('Ļ') else token
        if with_space:
            token = '\u0120' + token
        if with_break:
            token = '\u010A' + token
        return token
