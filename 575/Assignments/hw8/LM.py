import numpy as np
import torch

from pytorch_pretrained_bert import GPT2LMHeadModel, GPT2Tokenizer,BertTokenizer, BertForMaskedLM

class LM():
    def __init__(self, model_name_or_path="gpt2"):
        #super(LM, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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
        
class BERTLM():
    def __init__(self, model_name_or_path="bert-base-cased"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(model_name_or_path,do_lower_case=False)
        self.model = BertForMaskedLM.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.model.eval()
        self.mask_tok = self.tokenizer.convert_tokens_to_ids(["[MASK]"])[0]
        self.pad = self.tokenizer.convert_tokens_to_ids(["[PAD]"])[0]
        print("Loaded BERT model!")
    def generate_conditionalprobs(self, x,y):
        in_text = "[CLS] {} {} [SEP]".format(x,y)
        tokenized_text = self.tokenizer.tokenize(in_text)
        y_toks = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        segments_ids = [0] * len(y_toks)
        y = torch.tensor([y_toks]).to(self.device)
        segments_tensor = torch.tensor([segments_ids]).to(self.device)
        input_batches = []
        target_batches = []
        for min_ix in range(0, len(y_toks), 3):
            max_ix = min(min_ix + 3, len(y_toks) - 1)
            cur_input_batch = []
            cur_target_batch = []
            # Construct each batch
            for running_ix in range(max_ix - min_ix):
                tokens_tensor = y.clone()
                mask_index = min_ix + running_ix
                tokens_tensor[0, mask_index + 1] = self.mask_tok
                # Reduce computational complexity by subsetting
                min_index = max(0, mask_index - max_context)
                max_index = min(tokens_tensor.shape[1] - 1, mask_index + max_context + 1)
                tokens_tensor = tokens_tensor[:, min_index:max_index]
                # Add padding
                needed_padding = max_context * 2 + 1 - tokens_tensor.shape[1]
                if min_index == 0 and max_index == y.shape[1] - 1:
                    # Only when input is shorter than max_context
                    left_needed = (max_context) - mask_index
                    right_needed = needed_padding - left_needed
                    p = torch.nn.ConstantPad1d((left_needed, right_needed), self.pad)
                    tokens_tensor = p(tokens_tensor)
                elif min_index == 0:
                    p = torch.nn.ConstantPad1d((needed_padding, 0), self.pad)
                    tokens_tensor = p(tokens_tensor)
                elif max_index == y.shape[1] - 1:
                    p = torch.nn.ConstantPad1d((0, needed_padding), self.pad)
                    tokens_tensor = p(tokens_tensor)
                cur_input_batch.append(tokens_tensor)
                cur_target_batch.append(y[:, mask_index + 1])
            cur_input_batch = torch.cat(cur_input_batch, dim=0)
            cur_target_batch = torch.cat(cur_target_batch, dim=0)
            input_batches.append(cur_input_batch)
            target_batches.append(cur_target_batch)
        real_topk = []
        with torch.no_grad():
            for src, tgt in zip(input_batches, target_batches):
                logits = self.model(src, torch.zeros_like(src))[:,max_context + 1]
                yhat = torch.softmax(logits, dim=-1)
                real_topk_probs = yhat[np.arange(0, yhat.shape[0], 1), tgt].data.cpu().numpy().tolist()
        return real_topk_probs
    def check_probabilities(self, in_text, topk=40, max_context=20,batch_size=20):
        '''
        Same behavior as GPT-2
        Extra param: max_context controls how many words should be
        fed in left and right
        Speeds up inference since BERT requires prediction word by word
        '''
        in_text = "[CLS] " + in_text + " [SEP]"
        tokenized_text = self.tokenizer.tokenize(in_text)
        # Construct target
        y_toks = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        # Only use sentence A embedding here since we have non-separable seq's
        segments_ids = [0] * len(y_toks)
        y = torch.tensor([y_toks]).to(self.device)
        segments_tensor = torch.tensor([segments_ids]).to(self.device)
        input_batches = []
        target_batches = []
        for min_ix in range(0, len(y_toks), batch_size):
            max_ix = min(min_ix + batch_size, len(y_toks) - 1)
            cur_input_batch = []
            cur_target_batch = []
            # Construct each batch
            for running_ix in range(max_ix - min_ix):
                tokens_tensor = y.clone()
                mask_index = min_ix + running_ix
                tokens_tensor[0, mask_index + 1] = self.mask_tok
                # Reduce computational complexity by subsetting
                min_index = max(0, mask_index - max_context)
                max_index = min(tokens_tensor.shape[1] - 1, mask_index + max_context + 1)
                tokens_tensor = tokens_tensor[:, min_index:max_index]
                # Add padding
                needed_padding = max_context * 2 + 1 - tokens_tensor.shape[1]
                if min_index == 0 and max_index == y.shape[1] - 1:
                    # Only when input is shorter than max_context
                    left_needed = (max_context) - mask_index
                    right_needed = needed_padding - left_needed
                    p = torch.nn.ConstantPad1d((left_needed, right_needed), self.pad)
                    tokens_tensor = p(tokens_tensor)
                elif min_index == 0:
                    p = torch.nn.ConstantPad1d((needed_padding, 0), self.pad)
                    tokens_tensor = p(tokens_tensor)
                elif max_index == y.shape[1] - 1:
                    p = torch.nn.ConstantPad1d((0, needed_padding), self.pad)
                    tokens_tensor = p(tokens_tensor)
                cur_input_batch.append(tokens_tensor)
                cur_target_batch.append(y[:, mask_index + 1])
            cur_input_batch = torch.cat(cur_input_batch, dim=0)
            cur_target_batch = torch.cat(cur_target_batch, dim=0)
            input_batches.append(cur_input_batch)
            target_batches.append(cur_target_batch)
        real_topk = []
        pred_topk = []
        with torch.no_grad():
            for src, tgt in zip(input_batches, target_batches):
                # By construction, MASK is always the middle
                logits = self.model(src, torch.zeros_like(src))[:,max_context + 1]
                yhat = torch.softmax(logits, dim=-1)
                sorted_preds = np.argsort(-yhat.data.cpu().numpy())
                # TODO: compare with batch of tgt
                # [(pos, prob), ...]
                real_topk_pos = list([int(np.where(sorted_preds[i] == tgt[i].item())[0][0]) for i in range(yhat.shape[0])])
                real_topk_probs = yhat[np.arange(0, yhat.shape[0], 1), tgt].data.cpu().numpy().tolist()
                real_topk.extend(list(zip(real_topk_pos, real_topk_probs)))
                # # [[(pos, prob), ...], [(pos, prob), ..], ...]
                pred_topk.extend([list(zip(self.tokenizer.convert_ids_to_tokens(sorted_preds[i][:topk]),yhat[i][sorted_preds[i][:topk]].data.cpu().numpy().tolist())) for i in range(yhat.shape[0])])
        bpe_strings = [self.postprocess(s) for s in tokenized_text]
        pred_topk = [[(self.postprocess(t[0]), t[1]) for t in pred] for pred in pred_topk]
        payload = {'bpe_strings': bpe_strings,
                   'real_topk': real_topk,
                   'pred_topk': pred_topk}
        return payload
    def postprocess(self, token):
        with_space = True
        with_break = token == '[SEP]'
        if token.startswith('##'):
            with_space = False
            token = token[2:]
        if with_space:
            token = '\u0120' + token
        if with_break:
            token = '\u010A' + token
        return token