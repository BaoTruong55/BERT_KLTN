import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests
import dateutil.parser
from model_vnexpress import *
index = 0
prefix_id = 'test_'
url = "4098456"
total = 1
pathSaveCSV = 'crawlVnExp-temp-da.csv'

categoryThoiSu = "https://vnexpress.net/category/day?cateid=1001005&fromdate={fromdate}&todate={todate}&allcate=1001005&page={page}"

tagCovid = "https://vnexpress.net/tag/covid-19-1266216-p{page}"

def dateToTimestamp(date):
    return dateutil.parser.parse(date, dayfirst=True).timestamp()

# ! Get id post from url search
def getIdPostByTopic(URL, date):
    listIdPost = []
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser') 
    idPost = soup.find("meta", attrs={"name": "tt_article_id"})['content']
    for element in soup.find_all('span', attrs={"data-objectid":True}):
        listIdPost.append(element.get('data-objectid'))
    timePublic = []
    for element in soup.find_all('span', attrs={"class": "time-public"}):
        timePublic.append(element.text)

    status = True

    try:
        listIdPost = listIdPost[:timePublic.index(date)]
        status = False
    except:
        print()

    return dict.fromkeys(listIdPost), status

def getJsonFromURL(url):
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            document = newUrl.read().decode()
            dataJson = json.loads(document,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return dataJson

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

def writeCSVFile(listData, total):
    with open(pathSaveCSV, 'a+', newline='') as file:
        writer = csv.writer(file)
        for num, data in enumerate(listData, start=total):
            id = "{prefix_id}{lenZero}{number}".format(
                prefix_id = prefix_id,
                lenZero = '0' * (6 - len(str(num))),
                number = num
                )
            writer.writerow([id, data])

# TODO ============================================== Main ==============================================

def getIdPostByDate(url, date):
    listIdPost = []
    status = True
    page_index = 1
    while status:
        idPosts, status = getIdPostByTopic(url.format(page = page_index), date = date)
        listIdPost.extend(idPosts)
        print("Pages: [{page}] Number of post: {numOfPost}".format(page=page_index, numOfPost=len(idPosts)))
        page_index = page_index + 1
        if status:
            status = len(idPosts)

    return listIdPost

def getIdPostByPage(url, page):
    listIdPost = []
    status = True
    page_index = 1
    for page_index in range(1, page+1):
        print (status)
        idPosts, status = getIdPostByTopic(url.format(page = page_index), date = None)
        listIdPost.extend(idPosts)
        print("Pages: [{page}] Number of post: {numOfPost}".format(page=page_index, numOfPost=len(idPosts)))
    
    return listIdPost


def getIdPostByCategory(url, fromdate, todate):
    listIdPost = []
    status = True
    page_index = 1
    while status:
        idPosts, status = getIdPostByTopic(url.format(
            page = page_index,
            fromdate = dateToTimestamp(fromdate),
            todate = dateToTimestamp(todate)
        ), date = None)
        listIdPost.extend(idPosts)
        print("Pages: [{page}] Number of post: {numOfPost}".format(page=page_index, numOfPost=len(idPosts)))
        page_index = page_index + 1
        status = len(idPosts) != 0
    
    return listIdPost

with open(pathSaveCSV, 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['id', 'text'])

# listIdPost = getIdPostByCategory(categoryThoiSu, '1/4/2020', '26/5/2020')
listIdPost = getIdPostByPage(tagCovid, 2)
print(listIdPost)
totalPost = len(listIdPost)
for index, idPost in enumerate(listIdPost, start = 1):
    print("Post[{index}/{total}]: [{post}]".format(
        post = idPost,
        index = index,
        total = totalPost
    ))
    listComments = getComments(str(idPost))
    totalComment = len(listComments)
    for index, comment in enumerate(listComments, start = 1):
        print('[{index}/{totalComment}] - {comment}'.format(
            comment = comment,
            index = index,
            totalComment = totalComment
            ))
        Comment(
            comment = comment
        ).save()
        
    writeCSVFile(listComments, total)
    total = total + totalComment
