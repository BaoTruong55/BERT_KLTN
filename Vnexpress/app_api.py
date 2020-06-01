
from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup
import requests
from infer_predict import *

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

# TODO ==== Main ===============================================================

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
