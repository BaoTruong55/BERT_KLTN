import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests
import dateutil.parser
from model_vnexpress import *
import re
import unidecode


index = 0
prefix_id = 'test_'
url = "4098456"
total = 1
pathSaveCSV = 'crawlVnExp-temp-da.csv'

categoryThoiSu = "https://vnexpress.net/category/day?cateid=1001005&fromdate={fromdate}&todate={todate}&allcate=1001005&page={page}"

tagCovid = "https://vnexpress.net/tag/covid-19-1266216-p{page}"

def getJsonFromURL(url):
    content = requests.get(url)
    dataJson = content.json()

    return dataJson

def dateToTimestamp(date):
    return dateutil.parser.parse(date, dayfirst=True).timestamp()

def unmarkTiengViet(str):
    return unidecode.unidecode(str)

def getInfoTag(listTag):
    url = "https://gw.vnexpress.net/tg/tag_detail?tag_id={listTag}&data_select=tag_id,tag_name,tag_url,tax_variations".format(listTag = ','.join(listTag))
    print(url)
    print(getJsonFromURL(url))

def getInfoPost(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    
    script = soup.find_all('script')[3]
    # print(script.text.split(';')[0])

    # for el in script.text.split(';'):
    #     if str(el).find('article_topic_ID') > 0:
    #         print(el)
    # print(script)
    topicId = re.findall("{'article_topic_ID':'(.*?)'}", script.text)
    if len(topicId) != 0:
        topicId = topicId[0]
    else:
        topicId = ''

    titleTopic = re.findall("{'article_topic':'(.*?)'}", script.text)
    if len(titleTopic) != 0:
        titleTopic = '-'.join(unmarkTiengViet(titleTopic[0].lower()).split(' '))
    else:
        titleTopic = ''
    
    listTag = re.findall("{'tag_id':'(.*?)'}", script.text)
    if len(listTag) != 0:
        listTag = listTag[0].split(', ')
    else:
        listTag = []    

    print(topicId)
    print(titleTopic)
    print(listTag)
    getInfoTag(listTag)

# getInfoPost('https://vnexpress.net/cong-to-vien-co-lan-can-khi-xem-ho-so-vu-luong-huu-phuoc-4109080.html')
# getInfoPost('https://vnexpress.net/linh-trung-an-dang-chien-tich-au-da-len-mang-4108937.html')

# ! Get id post from url search
def getInfoPostByList(URL, date):
    listInfoPost = []
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser') 
    # idPost = soup.find("meta", attrs={"name": "tt_article_id"})['content']
    for elementSource in soup.find_all('article', attrs={"class": "item-news-common"}):
        soupEl = BeautifulSoup(content.text, 'html.parser')
        link = soupEl.find('a', attrs={'class': 'count_cmt', 'href': True})['href']
        objectId = soupEl.find('span', attrs={'data-objectid': True})['data-objectid']
        listInfoPost.append({'link': link, 'id': objectId})

    timePublic = []
    for element in soup.find_all('span', attrs={"class": "time-public"}):
        timePublic.append(element.text)

    status = True

    try:
        listInfoPost = listInfoPost[:timePublic.index(date)]
        status = False
    except:
        print()

    return listInfoPost, status


# ! Get reply comment from a comment in a post
def getChildrenComment(idPost, idParent):
    listComment = []
    url = "https://usi-saas.vnexpress.net/index/getreplay?limit=1000000&objecttype=1&offset=0&objectid={objectid}&id={id}".format(objectid = idPost, id = idParent)

    dataComments = getJsonFromURL(url)

    if type(dataComments['data']) is not list:
        print(dataComments['data'])
        for item in dataComments['data']['items']:
            listComment.append({
                'comment': item['content'],
                'createTime': item['creation_time'],
                'userLike': item['userlike']
            })

            print(item)
    return listComment

# ! Get parent comment in a post 
def getComments(idPost):
    listComment = []
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000000&siteid=1000000&objecttype=1&objectid={objectid}".format(objectid = idPost)
    dataComments = getJsonFromURL(url)
    if type(dataComments['data']) is not list:
        for item in dataComments['data']['items']:
            listComment.append({
                'comment': item['content'],
                'createTime': item['creation_time'],
                'userLike': item['userlike']
            })

            if 'replays' in item and 'total' in item['replays']:
                listComment.extend(getChildrenComment(idPost, item['parent_id']))

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

# TODO ====== Main =============================================================

def getInfoPostByDate(url, date):
    listIdPost = []
    status = True
    page_index = 1
    while status:
        idPosts, status = getInfoPostByList(
            url.format(page = page_index),
            date = date
        )
        listIdPost.extend(idPosts)
        print("Pages: [{page}] Number of post: {numOfPost}".format(
            page=page_index,
            numOfPost=len(idPosts)
        ))
        page_index = page_index + 1
        if status:
            status = len(idPosts)

    return listIdPost

def getInfoPostByPage(url, page):
    listIdPost = []
    status = True
    page_index = 1
    for page_index in range(1, page+1):
        print (status)
        idPosts, status = getInfoPostByList(url.format(page = page_index), date = None)
        listIdPost.extend(idPosts)
        print("Pages: [{page}] Number of post: {numOfPost}".format(
            page=page_index,
            numOfPost=len(idPosts)
        ))
    
    return listIdPost


def getInfoPostByCategory(url, fromdate, todate):
    listIdPost = []
    status = True
    page_index = 1
    while status:
        idPosts, status = getInfoPostByList(url.format(
            page = page_index,
            fromdate = dateToTimestamp(fromdate),
            todate = dateToTimestamp(todate)
        ), date = None)
        listIdPost.extend(idPosts)
        print("Pages: [{page}] Number of post: {numOfPost}".format(
            page=page_index,
            numOfPost=len(idPosts)
        ))
        page_index = page_index + 1
        status = len(idPosts) != 0
    
    return listIdPost

with open(pathSaveCSV, 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['id', 'text'])

# listIdPost = getInfoPostByCategory(categoryThoiSu, '1/4/2020', '26/5/2020')
listInfoPost = getInfoPostByPage(tagCovid, 5)
print(listInfoPost)
totalPost = len(listInfoPost)
for index, post in enumerate(listInfoPost, start = 1):
    print("Post[{index}/{total}]: [{post}]".format(
        post = post['id'],
        index = index,
        total = totalPost
    ))
    listComments = getComments(str(post['id']))
    totalComment = len(listComments)
    for index, comment in enumerate(listComments, start = 1):
        print('[{index}/{totalComment}] - {comment}'.format(
            comment = comment['comment'],
            index = index,
            totalComment = totalComment
        ))

        Comment(
            comment = comment['comment']
        ).save()
        
    writeCSVFile(listComments, total)
    total = total + totalComment
