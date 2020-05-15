import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup
import requests

prefix_id = 'test_'
index = 0
idPost = []

URL = "https://vnexpress.net/tho-dan-giua-covid-19-4094885.html"
content = requests.get(URL)
soup = BeautifulSoup(content.text, 'html.parser') 
for link in soup.find_all('span'):
    if link.get('data-objectid') != None:
        idPost.append(link.get('data-objectid'))
# ! Get reply comment from a comment in a post
def getChildrenComment(idPost, idParent):
    url = "https://usi-saas.vnexpress.net/index/getreplay?siteid=1000000&objectid="+str(idPost)+"&objecttype=1&id="+str(idParent)+"&limit=1000&offset=0&cookie_aid=ld3j1th433fuuy28.1589343761&sort_by=like&template_type=1"
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            dataChildrenComments = newUrl.read().decode()
            dataChildrenComments = json.loads(dataChildrenComments, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            for i in dataChildrenComments.data.items:
                arrList = i.content.split(";",1)
                listParentComments.append(arrList[-1])

# ! Get parent comment in a post 
def getParentComments(idPost):
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000&frommobile=0&sort=like&is_onload=0&objectid="+str(idPost)+"&objecttype=1&siteid=1003750&categoryid=1003784&usertype=4&template_type=1"
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            dataParentComments = newUrl.read().decode()
            dataParentComments = json.loads(dataParentComments, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            for i in dataParentComments.data.items:
                listParentComments.append(i.content)
                getChildrenComment(idPost, i.parent_id)
    return listParentComments

# TODO ============================================== Main ==============================================

with open('crawlPostVnExp.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['id', 'text'])

listParentComments = []
getParentComments(idPost[0])
print("So luong comment trong post la: "+str(len(listParentComments)))
with open('crawlPostVnExp.csv', 'a+', newline='') as file:
    writer = csv.writer(file)
    for i in listParentComments:
        id = prefix_id + '0' * (6 - len(str(index))) + str(index)
        index = index + 1
        writer.writerow([id, str(i)])