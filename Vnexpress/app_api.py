
from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup
import requests
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
import json
from pandas import DataFrame

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

args = parser.parse_args("""--test_path ./data2/data/test.csv
--dict_path ./PhoBERT_base_transformers/dict.txt
--config_path ./PhoBERT_base_transformers/config.json
--bpe-codes ./PhoBERT_base_transformers/bpe.codes
--pretrained_path ./PhoBERT_base_transformers/model.bin
--ckpt_path ./models
--rdrsegmenter_path ./VnCoreNLP/VnCoreNLP-1.1.1.jar""".split())
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


# read data test and tokenize
# test_df = pd.read_csv(args.test_path,sep='\t').fillna("###")
# test_df.text = test_df.text.progress_apply(lambda x: ' '.join([' '.join(sent) for sent in rdrsegmenter.tokenize(x)]))

def NomalizeData(comments):
    df = pd.DataFrame({"text": comments, "data_text": comments})

    df.text = df.text.progress_apply(lambda x: ' '.join([' '.join(sent) for sent in rdrsegmenter.tokenize(x)]))
    print(df)
    return df

# X_test = convert_lines(test_df, vocab, bpe,args.max_sequence_length)

def PredictData(df):
    X_test = convert_lines(df, vocab, bpe,args.max_sequence_length)
    preds_en = []
    for fold in range(1):
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
    print(preds_en)
    df["label_test"] = (preds_en > 0.5).astype(np.int)
    return df

# get comment from vnexpress
prefix_id = 'test_'
index = 0

# URL = "https://vnexpress.net/tho-dan-giua-covid-19-4094885.html"
def  getIdPost(URL):
    content = requests.get(URL)
    idPost = []
    soup = BeautifulSoup(content.text, 'html.parser') 
    for link in soup.find_all('span'):
        if link.get('data-objectid') != None:
            idPost.append(link.get('data-objectid'))
    return idPost[0]
    
# ! Get reply comment from a comment in a post
def getChildrenComment(idPost, idParent, listParentComments):
    url = "https://usi-saas.vnexpress.net/index/getreplay?siteid=1000000&objectid="+str(idPost)+"&objecttype=1&id="+str(idParent)+"&limit=1000&offset=0&cookie_aid=ld3j1th433fuuy28.1589343761&sort_by=like&template_type=1"
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            dataChildrenComments = newUrl.read().decode()
            dataChildrenComments = json.loads(dataChildrenComments,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            for i in dataChildrenComments.data.items:
                arrList = i.content.split(";",1)
                listParentComments.append(arrList[-1])

# ! Get parent comment in a post 
def getParentComments(idPost):
    listParentComments = []
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000&frommobile=0&sort=like&is_onload=0&objectid="+str(idPost)+"&objecttype=1&siteid=1003750&categoryid=1003784&usertype=4&template_type=1"
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            dataParentComments = newUrl.read().decode()
            dataParentComments = json.loads(dataParentComments,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            for i in dataParentComments.data.items:
                listParentComments.append(i.content)
                getChildrenComment(idPost, i.parent_id, listParentComments)
    return listParentComments

# TODO ============================================== Main ==============================================

with open('crawlPostVnExp.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['id', 'text'])

app = Flask(__name__)
api = Api(app)

class Vnexpress(Resource):
    def get(self):
        url = request.args.get('url')
        idPost =  getIdPost(url)
        listParentComments = getParentComments(idPost)
        df = NomalizeData(listParentComments)
        df_result = PredictData(df)
        df_output = DataFrame(df_result, columns= ['data_text', 'label_test'])
        df_negatives = df_output[df_output['label_test'] == 0]
        df_possitives = df_output[df_output['label_test'] == 1]
        output = {"commentPos": df_possitives.to_dict("records"), "commentNeg": df_negatives.to_dict("records"), "pos": len(df_possitives.index), "neg": len(df_negatives.index)}
        result = Response(json.dumps(output), mimetype='application/json')
        return result
        
api.add_resource(Vnexpress, '/vnexpress') # Route_1

if __name__ == '__main__':
     app.run()
