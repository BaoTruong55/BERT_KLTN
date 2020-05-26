import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup
import requests

prefix_id = 'test_'
index = 0

URL = "https://vnexpress.net/tho-dan-giua-covid-19-4094885.html"
content = requests.get(URL)
soup = BeautifulSoup(content.text, 'html.parser')

idPost = soup.find("meta", attrs={"name": "tt_article_id"})['content']

# ! Get reply comment from a comment in a post
def getChildrenComment(idPost, idParent):
    listComment = []
    url = "https://usi-saas.vnexpress.net/index/getreplay?limit=1000000&objecttype=1&offset=0&objectid={objectid}&id={id}".format(objectid = idPost, id = idParent)
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            dataChildrenComments = newUrl.read().decode()
            dataChildrenComments = json.loads(dataChildrenComments,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            for i in dataChildrenComments.data.items:
                arrList = i.content.split(";",1)
                listComment.append(arrList[-1])
    return listComment

# ! Get parent comment in a post 
def getComments(idPost):
    listComment = []
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000000&siteid=1000000&objecttype=1&objectid={objectid}".format(objectid = idPost)
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            dataParentComments = newUrl.read().decode()
            dataParentComments = json.loads(dataParentComments,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            for i in dataParentComments.data.items:
                listComment.append(i.content)
                listComment.extend(getChildrenComment(idPost, i.parent_id))

    return listComment

# TODO ============================================== Main ==============================================

with open('crawlPostVnExp.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['id', 'text'])

listComment = []
listComment = getComments(idPost)

print("So luong comment trong post la: "+str(len(listComment)))
with open('crawlPostVnExp.csv', 'a+', newline='') as file:
    writer = csv.writer(file)
    print(listComment)
    for i in listComment:    
        id = prefix_id + '0' * (6 - len(str(index))) + str(index)
        index = index + 1
        writer.writerow([id, str(i)])