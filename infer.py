import pandas as pd
from models import *
from tqdm import tqdm
tqdm.pandas()
from torch import nn
import json
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from transformers import *
import torch
import matplotlib.pyplot as plt
import torch.utils.data
import torch.nn.functional as F
import argparse
from transformers.modeling_utils import * 
from fairseq.data.encoders.fastbpe import fastBPE
from fairseq.data import Dictionary
from vncorenlp import VnCoreNLP
from utils import * 

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--test_path', type=str, default='./data/test.csv')
parser.add_argument('--dict_path', type=str, default="./phobert/dict.txt")
parser.add_argument('--config_path', type=str, default="./phobert/config.json")
parser.add_argument('--rdrsegmenter_path', type=str, required=True)
parser.add_argument('--pretrained_path', type=str, default='./phobert/model.bin')
parser.add_argument('--max_sequence_length', type=int, default=256)
parser.add_argument('--batch_size', type=int, default=2)
parser.add_argument('--ckpt_path', type=str, default='./models')
parser.add_argument('--bpe-codes', default="./phobert/bpe.codes",type=str, help='path to fastBPE BPE')

args = parser.parse_args()
bpe = fastBPE(args)
rdrsegmenter = VnCoreNLP(args.rdrsegmenter_path, annotators="wseg", max_heap_size='-Xmx500m') 

# Load model
config = RobertaConfig.from_pretrained(
    args.config_path,
    output_hidden_states=True,
    num_labels=1
)
model_bert = RobertaForAIViVN.from_pretrained(args.pretrained_path, config=config)
model_bert.cuda()

# Load the dictionary  
vocab = Dictionary()
vocab.add_from_file(args.dict_path)

if torch.cuda.device_count():
    print(f"Testing using {torch.cuda.device_count()} gpus")
    model_bert = nn.DataParallel(model_bert)
    tsfm = model_bert.module.roberta
else:
    tsfm = model_bert.roberta

test_df = pd.read_csv(args.test_path,sep='\t').fillna("###")
test_df.text = test_df.text.progress_apply(lambda x: ' '.join([' '.join(sent) for sent in rdrsegmenter.tokenize(x)]))

X_test = convert_lines(test_df, vocab, bpe,args.max_sequence_length)

preds_en = []
for fold in range(5):
    print(f"Predicting for fold {fold}")
    preds_fold = []
    model_bert.load_state_dict(torch.load(os.path.join(args.ckpt_path, f"model_{fold}.bin")))
    test_dataset = torch.utils.data.TensorDataset(torch.tensor(X_test,dtype=torch.long))
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    model_bert.eval()
    pbar = tqdm(enumerate(test_loader),total=len(test_loader),leave=False)
    for i, (x_batch,) in pbar:
        y_pred = model_bert(x_batch.cuda(), attention_mask=(x_batch>0).cuda())
        y_pred = y_pred.view(-1).detach().cpu().numpy()
        preds_fold = np.concatenate([preds_fold, y_pred])
    preds_fold = sigmoid(preds_fold)
    preds_en.append(preds_fold)

preds_en = np.mean(preds_en,axis=0)
test_df["label_test"] = (preds_en > 0.5).astype(np.int)
test_df[["id","text","label_test"]].to_csv("submission.csv")
test_df['result'] = np.where(test_df['label'] == test_df['label_test'], 'true', 'false')
result_true = np.where(test_df['result'], 1, 0).sum()

df_negatives = test_df[test_df['label'] == 0]
df_possitives = test_df[test_df['label'] == 1]

true_negatives = np.where(df_negatives['result'] == 'true', 1, 0).sum()
false_negatives = np.where(df_negatives['result'] == 'false', 1, 0).sum()

true_possitives = np.where(df_possitives['result'] == 'true', 1, 0).sum()
false_possitives = np.where(df_possitives['result'] == 'false', 1, 0).sum()

actual_positive = true_possitives + false_negatives
recall = true_possitives / actual_positive

precision = true_possitives / (true_possitives + false_possitives)

f1 = 2 * (precision * recall)/ (precision + recall)

total = (true_negatives + false_negatives + true_possitives + false_possitives)
auc = (true_negatives + true_possitives) / total

print('true_negatives:' + str(true_negatives))
print('false_negatives:' + str(false_negatives))
print('true_possitives:' + str(true_possitives))
print('false_possitives:' + str(false_possitives))

print('recall:' + str(recall))
print('precision:' + str(precision))

print('F1_score:' + str(f1))
print('AUC', str(auc))