import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests
import dateutil.parser
from model_vnexpress import *
import re
import unidecode
from datetime import date, timedelta
# from infer_predict import *
import time

index = 0
PREFIX_ID = 'test_'
total = 1
pathSaveCSV = 'crawlVnExp-temp-da.csv'

# categoryThoiSu = "https://vnexpress.net/category/day?cateid=1001005&fromdate={fromdate}&todate={todate}&allcate=1001005&page={page}"

tagCovid = "https://vnexpress.net/tag/covid-19-1266216-p{page}"

def getJsonFromURL(url):
    content = requests.get(url)
    dataJson = content.json()

    return dataJson

def dateToTimestamp(date):
    return int(dateutil.parser.parse(date, dayfirst=True).timestamp())

def unmarkTiengViet(str):
    return unidecode.unidecode(str)

def removeDuplicate(listInfoPost):
    idsPost = []
    infoPosts = []
    for infoPostCurrent in listInfoPost:
        if infoPostCurrent['id'] not in idsPost:
            infoPosts.append(infoPostCurrent)
            idsPost.append(infoPostCurrent['id'])    
    
    return infoPosts

# getInfo
def getInfoTopic(topicId, articleTopic):
    url = 'https://vnexpress.net/topic/{articleTopic}-{topicId}'.format(
        articleTopic = articleTopic,
        topicId = topicId
    )
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')

    description = soup.find('meta', attrs={'name': 'description'})['content']
    title = soup.find('title').text

    return {
        'id': topicId,
        'articleTopic': articleTopic, 
        'title': title,
        'description': description
    }
    
def getInfoTag(listTag):
    url = "https://gw.vnexpress.net/tg/tag_detail?tag_id={listTag}&data_select=tag_id,tag_name,tag_url,tax_variations".format(listTag = ','.join(listTag))
    dataTag = getJsonFromURL(url)
    tags = []
    for key, value in dataTag['data'].items():
        tags.append({
            "id": str(value['tag_id']),
            "name": value['tag_name'],
            "url": value['tag_url']
        })

    return tags

def getInfoPost(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    
    # script have info topicid, article topic, tag id
    script = soup.find_all('script')[3]

    topicId = re.findall("{'article_topic_ID':'(.*?)'}", script.text)
    if len(topicId) != 0:
        topicId = topicId[0]
    else:
        topicId = ''

    articleTopic = re.findall("{'article_topic':'(.*?)'}", script.text)
    if len(articleTopic) != 0:
        articleTopic = '-'.join(unmarkTiengViet(articleTopic[0].lower()).split(' '))
    else:
        articleTopic = ''

    tagIds = re.findall("{'tag_id':'(.*?)'}", script.text)
    if len(tagIds) != 0:
        tagIds = tagIds[0].split(', ')
    else:
        tagIds = []
    
    
    infoTags = {}
    if len(tagIds) != 0:
        infoTags = getInfoTag(tagIds)

    infoTopic = {}
    if topicId != '':
        infoTopic = getInfoTopic(topicId, articleTopic)


    description = soup.find('meta', attrs={'name': 'description'})['content']
    publishTime = soup.find('meta', attrs={'name': 'its_publication'})['content']
    idPost = soup.find('meta', attrs={'name': 'its_id'})['content']
    title = soup.find('title').text
    thumbnail = soup.find('meta', attrs={'itemprop': 'thumbnailUrl'})['content'] 

    return {
        'id': idPost,
        'title': title,
        'description': description,
        'topicId': topicId,
        'tagIds': tagIds,
        'publishTime': publishTime,
        'thumbnail': thumbnail,
        'link': url
    }, infoTags, infoTopic

def getInfoCategory(idCategory, title):
    today = formatDate(date.today())
    url = 'https://vnexpress.net/category/day?cateid={cateid}&allcate={allcate}&fromdate={fromdate}&todate={todate}&page={page}'.format(
        cateid = idCategory,
        allcate = idCategory,
        page = 1,
        fromdate = dateToTimestamp(today),
        todate = dateToTimestamp(today)
    )
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')

    description = soup.find('meta', attrs={'name': 'description'})['content']

    return {
        'id': idCategory,
        'title': title,
        'description': description
    }

# getInfoPost('https://vnexpress.net/cong-to-vien-co-lan-can-khi-xem-ho-so-vu-luong-huu-phuoc-4109080.html')
# getInfoPost('https://vnexpress.net/linh-trung-an-dang-chien-tich-au-da-len-mang-4108937.html')

# ! Get id post from url search
def getInfoPostByList(URL, date):
    listInfoPost = []
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    for elementSource in soup.find_all('article', attrs={"class": "item-news item-news-common"}):
        link = elementSource.find('a', attrs={'class': 'count_cmt', 'href': True})
        if link != None:
            link = link['href']
        
        objectId = elementSource.find('span', attrs={'data-objectid': True})
        if objectId != None:
            objectId = objectId['data-objectid'] 
        print(link)
        if link != None and objectId != None:
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

    if len(listInfoPost) == 0:
        status = False

    return listInfoPost, status


# ! Get reply comment from a comment in a post
def getChildrenComment(idPost, idParent):
    comments = []
    url = "https://usi-saas.vnexpress.net/index/getreplay?limit=1000000&objecttype=1&offset=0&objectid={objectid}&id={id}".format(objectid = idPost, id = idParent)

    dataComments = getJsonFromURL(url)

    if type(dataComments['data']) is not list:
        for comment in dataComments['data']['items']:
            comments.append({
                'id': comment['comment_id'],
                'comment': comment['content'],
                'createTime': comment['creation_time'],
                'userLike': comment['userlike']
            })
    return comments

# ! Get parent comment in a post 
def getComments(idPost):
    comments = []
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000000&siteid=1000000&objecttype=1&objectid={objectid}".format(objectid = idPost)
    dataComments = getJsonFromURL(url)
    if type(dataComments['data']) is not list:
        for comment in dataComments['data']['items']:
            comments.append({
                'id': comment['comment_id'],
                'comment': comment['content'],
                'createTime': comment['creation_time'],
                'userLike': comment['userlike']
            })

            if 'replays' in comment and 'total' in comment['replays']:
                comments.extend(getChildrenComment(idPost, comment['parent_id']))

    return comments

def writeCSVFile(listData, total):
    with open(pathSaveCSV, 'a+', newline='') as file:
        writer = csv.writer(file)
        for num, data in enumerate(listData, start=total):
            id = "{prefix_id}{lenZero}{number}".format(
                prefix_id = PREFIX_ID,
                lenZero = '0' * (6 - len(str(num))),
                number = num
            )
            writer.writerow([id, data])

# TODO ====== Main =============================================================

def getInfoPostByDate(url, date):
    infoPosts = []
    status = True
    page_index = 1
    while status:
        infoPostsPageCurrent, status = getInfoPostByList(
            url.format(page = page_index),
            date = date
        )
        infoPosts.extend(infoPostsPageCurrent)
        print("Pages: [{page}] Number of post: {numOfPost}".format(
            page=page_index,
            numOfPost=len(infoPostsPageCurrent)
        ))
        page_index = page_index + 1
        if status:
            status = len(infoPostsPageCurrent)

    return infoPosts

def getInfoPostByPage(url, page):
    infoPosts = []
    status = True
    page_index = 1
    for page_index in range(1, page+1):
        infoPostsPageCurrent, status = getInfoPostByList(
            url.format(page = page_index),
            date = None
        )
        infoPosts.extend(infoPostsPageCurrent)
        print("Pages: [{page}] Number of post: {numOfPost}".format(
            page=page_index,
            numOfPost=len(infoPostsPageCurrent)
        ))

    # print(infoPosts)
    return infoPosts

def props(x):
    return dict((key, getattr(x, key)) for key in dir(x) if key not in dir(x.__class__))

def saveCategory(item):
    category = Category.objects(idCategory=item['id'])
    # print(category)
    if len(category) == 0:
        infoCategory = getInfoCategory(item['id'], item['text'])
        # print(infoCategory)
        category = Category(
            idCategory = infoCategory['id'],
            title = infoCategory['title'],
            description = infoCategory['description']
        )
        print(category.idCategory)
        category.save()
    else:
        print('have a db:', category[0])
        category = category[0]
    return category

def saveCategory(item):
    category = Category.objects(idCategory=item['id'])
    # print(category)
    if len(category) == 0:
        infoCategory = getInfoCategory(item['id'], item['text'])
        print(infoCategory)
        category = Category(
            idCategory = infoCategory['id'],
            title = infoCategory['title'],
            description = infoCategory['description']
        )
        print(category.idCategory)
        category.save()
    else:
        category = category[0]

    return category
    
def saveTag(item):
    tag = Tag.objects(idTag=item['id'])
    
    if len(tag) == 0:
        tag = Tag(
            idTag = item['id'],
            name = item['name'],
            url = item['url']
        )
        tag.save()
    else:
        tag = tag[0]
    
    return tag

def saveTopic(item):
    topic = Topic.objects(idTopic=item['id'])
    print(item)
    if len(topic) == 0:
        topic = Topic(
            idTopic = item['id'],
            articleTopic = item['articleTopic'],
            title = item['title'],
            description = item['description']
        )
        topic.save()
    else:
        topic = topic[0]
    
    return topic

def savePost(item):
    post = Post.objects(idPost=item['id'])
    if len(post) == 0:
        post = Post(
            idPost = item['id'],
            title = item['title'],
            description = item['description'],
            timeStamp = item['publishTime'],
            link = item['link'],
            link_thumbnail = item['thumbnail']
        )

        post.save()
    else:
        post = post[0]

    return post

def getInfoPostByCategory(category, fromdate, todate):
    infoPosts = []
    for item in category:
        # print(item)
        status = True
        page_index = 1
        category = saveCategory(item)

        while status:
            url = 'https://vnexpress.net/category/day?cateid={cateid}&allcate={allcate}&fromdate={fromdate}&todate={todate}&page={page}'.format(
                        cateid = item['id'],
                        allcate = item['id'],
                        page = page_index,
                        fromdate = dateToTimestamp(fromdate),
                        todate = dateToTimestamp(todate)
                    )
            infoPostsPageCurrent, status = getInfoPostByList(url, date = None)
            for infoPost in infoPostsPageCurrent:
                infoPost, infoTags, infoTopic = getInfoPost(infoPost['link'])
                post  = savePost(infoPost)
                
                category.posts.append(post)

                if len(infoTopic) != 0:
                    topic  = saveTopic(infoTopic)
                    topic.posts.append(post)
                    topic.save()

                for infoTag in infoTags:
                    tag = saveTag(infoTag)
                    tag.posts.append(post)
                    tag.save()

            infoPosts.extend(infoPostsPageCurrent)

            print("Pages: [{page}] Number of post: {numOfPost}".format(
                page=page_index,
                numOfPost=len(infoPostsPageCurrent)
            ))
            page_index = page_index + 1
            status = len(infoPostsPageCurrent) != 0

    return infoPosts

def getCategoryFromJson():
    with open('./category.json') as f:
        data = json.load(f)
        
    return data

def firstThingWriteCsv():
    with open(pathSaveCSV, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'text'])

def formatDate(date):
    return str(f'{date:%d/%m/%Y}')

def getCommentsText(item):
    return item['comment']

def getComment(item):
    return item.comment

def getCommentsId(item):
    return item['id']

if __name__ == '__main__':
    start = time.time()
    category = getCategoryFromJson()
    today = formatDate(date.today())
    fromDate  = formatDate(date.today() - timedelta(days=0))

    listInfoPost = getInfoPostByCategory(category, fromDate, today)
    # listInfoPost = removeDuplicate(getInfoPostByPage(tagCovid, 1))
    print(listInfoPost)
    # totalPost = len(listInfoPost)
    # for index, post in enumerate(listInfoPost, start = 1):
    #     print("Post[{index}/{total}]: [{post}]".format(
    #         post = post['id'],
    #         index = index,
    #         total = totalPost
    #     ))
    #     comments = getComments(str(post['id']))
    #     totalComment = len(comments)
    #     if totalComment > 0:
    #         commentText = list(map(getCommentsText, comments))
    #         commentId = list(map(getCommentsId, comments))
    #         print(commentText)
    #         print(commentId)
    #         df = NomalizeDataCommentVnexpress(commentId, commentText)
    #         df_result = PredictData(df)
            # print(df_result)
        # for index, comment in enumerate(comments, start = 1):
        #     print(comment)
            # print('[{index}/{totalComment}] - {comment}'.format(
            #     comment = comment['comment'],
            #     index = index,
            #     totalComment = totalComment
            # ))
            
    #         Comment(
    #             comment = comment['comment']
    #         ).save()
            
    #     writeCSVFile(comments, total)
        # total = total + totalComment
    
    end = time.time()
    print(time.strftime("%H:%M:%S", time.gmtime(end - start)))
