import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup
import requests

# get comment from vnexpress
prefix_id = 'test_'
index = 0

def getJsonFromURL(url):
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            document = newUrl.read().decode()
            dataJson = json.loads(document,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return dataJson

# URL = "https://vnexpress.net/tho-dan-giua-covid-19-4094885.html"
def  getInfoPost(URL):
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    idPost = soup.find('meta', attrs={'name': 'its_id'}).get('content')
    description = soup.find('meta', attrs={'name': 'description'}).get('content')
    title = soup.find('title').text 
    return idPost, title, description
    
# ! Get reply comment from a comment in a post
def getChildrenComment(idPost, idParent):
    listComment = []
    url = "https://usi-saas.vnexpress.net/index/getreplay?limit=1000000&objecttype=1&offset=0&objectid={objectid}&id={id}".format(objectid = idPost, id = idParent)

    dataComments = getJsonFromURL(url)
    if type(dataComments.data) is not list:
        for i in dataComments.data.items:
            arrList = i.content.split(";",1)
            listComment.append(arrList[-1])

    return listComment

# ! Get parent comment in a post 
def getComments(idPost):
    listComment = []
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000000&siteid=1000000&objecttype=1&objectid={objectid}".format(objectid = idPost)
    dataComments = getJsonFromURL(url)
    if type(dataComments.data) is not list:
        for i in dataComments.data.items:
            listComment.append(i.content)
            listComment.extend(getChildrenComment(idPost, i.parent_id))

    return listComment