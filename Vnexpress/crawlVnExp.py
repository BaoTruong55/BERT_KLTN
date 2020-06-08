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
import time
from utils import *
from infer_predict import *

pathSaveCSV = 'crawlVnExp-temp-da.csv'

def getInfoTopic(idTopic, articleTopic):
    topic = Topic.objects(idTopic=idTopic)
    if len(topic) != 0:
        return topic[0]    
    
    url = 'https://vnexpress.net/topic/{articleTopic}-{topicId}'.format(
        articleTopic = articleTopic,
        topicId = idTopic
    )
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')

    description = soup.find('meta', attrs={'name': 'description'})
    if description != None:
        description = description['content']
    else:
        description = ''

    title = soup.find('title').text

    topic = Topic(
        idTopic = idTopic,
        articleTopic = articleTopic,
        title = title,
        description = description
    )
    
    topic.save()

    return topic

def getInfoTag(listTag):
    url = "https://gw.vnexpress.net/tg/tag_detail?tag_id={listTag}&data_select=tag_id,tag_name,tag_url,tax_variations".format(listTag = ','.join(listTag))
    dataTag = getJsonFromURL(url)
    tags = []
    for key, item in dataTag['data'].items():
        tag = Tag.objects(idTag=str(item['tag_id']))

        if len(tag) == 0:
            tag = Tag(
                idTag = str(item['tag_id']),
                name = item['tag_name'],
                url = item['tag_url']
            )
            tag.save()
        else:
            tag = tag[0]

        tags.append(tag)

    return tags

def getInfoPost(url, idPost):
    post = Post.objects(idPost=idPost)
    if len(post) != 0:
        return post[0], None, None

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
    
    
    infoTags = None
    if len(tagIds) != 0:
        infoTags = getInfoTag(tagIds)

    infoTopic = None
    if topicId != '':
        infoTopic = getInfoTopic(topicId, articleTopic)


    title = soup.find('title').text
    
    description = soup.find('meta', attrs={'name': 'description'})
    if description != None:
        description = description['content']
    else:
        description = ''

    publishTime = soup.find('meta', attrs={'name': 'its_publication'})
    if publishTime != None:
        publishTime = publishTime['content']
    else:
        publishTime = '0'
    
    thumbnailUrl = soup.find('meta', attrs={'itemprop': 'thumbnailUrl'})
    if thumbnailUrl != None:
        thumbnailUrl = thumbnailUrl['content']
    else:
        thumbnailUrl = ''

    post = Post(
        idPost = idPost,
        title = title,
        description = description,
        publishTime = timestampToDatetime(publishTime),
        url = url,
        thumbnailUrl = thumbnailUrl
    )
    
    post.save()

    return post, infoTags, infoTopic


def getInfoCategory(idCategory, title):
    category = Category.objects(idCategory=idCategory)
    if len(category) != 0:
        return category[0]
    
    today = formatDate(date.today())
    url = 'https://vnexpress.net/category/day?cateid={cateid}&allcate={allcate}&fromdate={fromdate}&todate={todate}&page={page}'.format(
        cateid = idCategory,
        allcate = idCategory,
        page = 1,
        fromdate = datetimeToTimestamp(today),
        todate = datetimeToTimestamp(today)
    )
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    description = soup.find('meta', attrs={'name': 'description'})['content']

    category = Category(
        idCategory = idCategory,
        title = title,
        description = description
    )
    category.save()

    return category

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

    if 'data'in dataComments \
        and dataComments['data']['total'] > 0 \
        and dtype(dataComments['data']) is not list:
        for item in dataComments['data']['items']:
            comment = Comment.objects(idComment=item['comment_id'])
            if len(comment) == 0:
                comment = Comment(
                    idComment = str(item['comment_id']),
                    comment = item['content'],
                    createTime = timestampToDatetime(item['creation_time']),
                    userLike = item['userlike']
                )
                comment.save()
            else:
                comment = comment[0]
                
            comments.append(comment)
    return comments

# ! Get parent comment in a post 
def getComments(idPost):
    comments = []
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000000&siteid=1000000&objecttype=1&objectid={objectid}".format(objectid = idPost)
    print(url)
    dataComments = getJsonFromURL(url)

    if 'data'in dataComments \
        and type(dataComments['data']) is not list:
        for item in dataComments['data']['items']:
            comment = Comment.objects(idComment=item['comment_id'])
            if len(comment) == 0:
                comment = Comment(
                    idComment = str(item['comment_id']),
                    comment = item['content'],
                    createTime = timestampToDatetime(item['creation_time']),
                    userLike = item['userlike']
                )
                comment.save()
            else:
                comment = comment[0]

            comments.append(comment)

            if item['comment_id'] != item['parent_id'] \
                and 'replays' in item \
                and 'total' in item['replays']:
                comments.extend(getChildrenComment(idPost, comment['parent_id']))

    return comments


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

    return removeDuplicate(infoPosts)

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

    return removeDuplicate(infoPosts)

def getInfoPostByCategory(category, fromdate, todate):
    infoPosts = []
    totalCategory = len(category)
    for indexCategory, item in enumerate(category, start=1):
        status = True
        page_index = 1
        category = getInfoCategory(item['id'], item['title'])
        
        print('category [{indexCategory}/{totalCategody}]: [{id}] {title}'.format(
            indexCategory=indexCategory,
            totalCategody=totalCategory,
            title=item['title'],
            id=item['id']
        ))

        while status:
            url = 'https://vnexpress.net/category/day?cateid={cateid}&allcate={allcate}&fromdate={fromdate}&todate={todate}&page={page}'.format(
                        cateid = item['id'],
                        allcate = item['id'],
                        page = page_index,
                        fromdate = datetimeToTimestamp(fromdate),
                        todate = datetimeToTimestamp(todate)
                    )
            infoPostsPageCurrent, status = getInfoPostByList(url, date = None)
            for indexPost, infoPost in enumerate(infoPostsPageCurrent, start=0):
                post, tags, topic = getInfoPost(infoPost['link'], infoPost['id'])
                
                infoPostsPageCurrent[indexPost]['post'] = post
                
                print('- {title}'.format(
                    title=post.title
                ))


                if post not in category.posts:
                    category.posts.append(post)
                category.save()

                if tags != None:
                    for tag in tags:
                        if post not in tag.posts:
                            tag.posts.append(post)
                        tag.save()

                if topic != None: 
                    if post not in topic.posts:
                        topic.posts.append(post)
                    topic.save()

            infoPosts.extend(infoPostsPageCurrent)

            print("Pages: [{page}] Number of post: {numOfPost}".format(
                page=page_index,
                numOfPost=len(infoPostsPageCurrent)
            ))
            page_index = page_index + 1
            status = len(infoPostsPageCurrent) != 0

    return removeDuplicate(infoPosts)

def crawlAllNDays(N):
    category = getCategoryFromJson()
    today = formatDate(date.today())
    fromDate  = formatDate(date.today() - timedelta(days=N))

    infoPosts = getInfoPostByCategory(category, fromDate, today)
    totalPost = len(infoPosts)
    print("="*20 + "get comment" + "="*20)
    total = 1
    for index, infoPost in enumerate(infoPosts, start = 1):
        print("Post[{index}/{total}]: [{post}]".format(
            post = infoPost['id'],
            index = index,
            total = totalPost
        ))
        comments = getComments(str(infoPost['id']))
        
        totalComment = len(comments)
        for index, comment in enumerate(comments, start = 1):
            print('[{index}/{totalComment}] - {comment}'.format(
                comment = comment.comment,
                index = index,
                totalComment = totalComment
            ))
            if comment not in infoPost['post'].comments:
                infoPost['post'].comments.append(comment)
        infoPost['post'].save()
            
        total = total + totalComment

def crawlAllThreeDays():
    crawlAllNDays(3)

def crawlAllAWeek():
    crawlAllNDays(7)

def crawlAllAMonth():
    crawlAllNDays(30)

def predictComment():
    comments  = Comment.objects(label=None)
    print(len(comments))
    if len(comments) > 0:
        commentText = list(map(getCommentText, comments))
        commentId = list(map(getCommentId, comments))
        df = NomalizeDataCommentVnexpress(commentId, commentText)
        df_result = PredictData(df)
        for comment in comments:
            comment.label = df_result[df_result['id'] == comment.idComment]['label']
            comment.save() 
    print('Done')

if __name__ == '__main__':
    start = time.time()
   
    # crawlAllThreeDays()
    # crawlAllAMonth()
    predictComment()

    end = time.time()
    print(time.strftime("%H:%M:%S", time.gmtime(end - start)))