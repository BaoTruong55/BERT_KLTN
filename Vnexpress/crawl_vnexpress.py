import urllib.request
import json
import random
from collections import namedtuple
import csv
from bs4 import BeautifulSoup  # BeautifulSoup is in bs4 package
import requests
import dateutil.parser
from model_vnexpress import *
import re
import unidecode
from datetime import date, timedelta
import time
from utils import *
from dateutil import parser
# from infer_predict import *

PATH_SAVE_CSV = 'crawlVnExp-temp-da.csv'


def get_info_topic(id_topic, article_topic):
    topic = Topic.objects(idTopic=id_topic).first()
    if topic != None:
        return topic

    url = 'https://vnexpress.net/topic/{articleTopic}-{topicId}'.format(
        articleTopic=article_topic,
        topicId=id_topic
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
        idTopic=id_topic,
        articleTopic=article_topic,
        title=title,
        description=description
    )

    topic.save()

    return topic


def get_info_tag(list_tag):
    url = "https://gw.vnexpress.net/tg/tag_detail?tag_id={listTag}&data_select=tag_id,tag_name,tag_url,tax_variations".format(
        listTag=','.join(list_tag))
    data_tag = get_json_from_url(url)
    tags = []
    for _, item in data_tag['data'].items():
        tag = Tag.objects(idTag=str(item['tag_id'])).first()

        if tag == None:
            tag = Tag(
                idTag=str(item['tag_id']),
                name=item['tag_name'],
                url=item['tag_url']
            )
            tag.save()

        tags.append(tag)

    return tags


def choice_script(scripts):
    for script in scripts:
        topic_id = re.findall("{'article_topic_ID':'(.*?)'}", str(script))
        topic = re.findall("{'article_topic':'(.*?)'}", str(script))
        tag_id = re.findall("{'tag_id':'(.*?)'}", str(script))
        if len(topic_id) != 0 or len(topic) != 0 or len(tag_id) != 0:
            return str(script)
    return ""


def get_info_post(url, id_post):
    post = Post.objects(idPost=id_post).first()
    if post != None:
        return post, None, None

    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')

    # script have info topicid, article topic, tag id

    script = choice_script(soup.find_all('script'))

    topic_id = re.findall("{'article_topic_ID':'(.*?)'}", script)
    if len(topic_id) != 0:
        topic_id = topic_id[0]
    else:
        topic_id = ''

    article_topic = re.findall("{'article_topic':'(.*?)'}", script)
    if len(article_topic) != 0:
        article_topic = '-'.join(unmark_vietnamese(
            article_topic[0].lower()).split(' '))
    else:
        article_topic = ''

    tag_ids = re.findall("{'tag_id':'(.*?)'}", script)
    if len(tag_ids) != 0:
        tag_ids = tag_ids[0].split(', ')
    else:
        tag_ids = []

    info_tags = None
    if len(tag_ids) != 0:
        info_tags = get_info_tag(tag_ids)
    print(info_tags)

    info_topic = None
    if topic_id != '':
        info_topic = get_info_topic(topic_id, article_topic)

    title = soup.find('title').text

    description = soup.find('meta', attrs={'name': 'description'})
    if description != None:
        description = description['content']
    else:
        description = ''

    publish_time = soup.find('meta', attrs={'name': 'its_publication'})
    if publish_time != None:
        publish_time = publish_time['content']
    else:
        publish_time = '0'

    thumbnail_url = soup.find('meta', attrs={'itemprop': 'thumbnailUrl'})
    if thumbnail_url != None:
        thumbnail_url = thumbnail_url['content']
    else:
        thumbnail_url = ''

    post = Post(
        idPost=id_post,
        title=title,
        description=description,
        publishTime=timestamp_to_datetime(publish_time),
        url=url,
        thumbnailUrl=thumbnail_url
    )
    post.save()

    return post, info_tags, info_topic


def get_info_category(id_category, title):
    category = Category.objects(idCategory=id_category)
    if len(category) != 0:
        return category[0]

    today = format_date(date.today())
    url = 'https://vnexpress.net/category/day?cateid={cateid}&allcate={allcate}&fromdate={fromdate}&todate={todate}&page={page}'.format(
        cateid=id_category,
        allcate=id_category,
        page=1,
        fromdate=datetime_to_timestamp(today),
        todate=datetime_to_timestamp(today)
    )
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    description = soup.find('meta', attrs={'name': 'description'})['content']

    category = Category(
        idCategory=id_category,
        title=title,
        description=description
    )
    category.save()

    return category

# ! Get id post from url search


def get_info_post_by_list(URL, date):
    list_info_post = []
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    for elementSource in soup.find_all('article', attrs={"class": "item-news item-news-common"}):
        link = elementSource.find(
            'a', attrs={'class': 'count_cmt', 'href': True})
        if link != None:
            link = link['href']

        object_id = elementSource.find('span', attrs={'data-objectid': True})
        if object_id != None:
            object_id = object_id['data-objectid']

        if link != None and object_id != None:
            list_info_post.append({'link': link, 'id': object_id})

    time_public = []
    for element in soup.find_all('span', attrs={"class": "time-public"}):
        time_public.append(element.text)

    status = True

    try:
        list_info_post = list_info_post[:time_public.index(date)]
        status = False
    except:
        print()

    if len(list_info_post) == 0:
        status = False

    return list_info_post, status


# ! Get reply comment from a comment in a post
def get_children_comment(id_post, id_parent):
    comments = []
    url = "https://usi-saas.vnexpress.net/index/getreplay?limit=1000000&objecttype=1&offset=0&objectid={objectid}&id={id}".format(
        objectid=id_post, id=id_parent)

    data_comments = get_json_from_url(url)

    if 'data' in data_comments \
            and data_comments['data']['total'] > 0 \
            and type(data_comments['data']) is not list:
        for item in data_comments['data']['items']:
            try:
                comment = Comment.objects(idComment=item['comment_id']).first()
                if comment == None:
                    comment = Comment(
                        idComment=str(item['comment_id']),
                        comment=item['content'],
                        createTime=timestamp_to_datetime(
                            item['creation_time']),
                        userLike=item['userlike']
                    )
                    comment.save()

                comments.append(comment)

            except:
                print()

    return comments

# ! Get parent comment in a post


def get_comments(id_post):
    comments = []
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000000&siteid=1000000&objecttype=1&objectid={objectid}".format(
        objectid=id_post)
    print(url)
    data_comments = get_json_from_url(url)

    if 'data' in data_comments \
            and type(data_comments['data']) is not list:
        for item in data_comments['data']['items']:
            try:
                comment = Comment.objects(idComment=item['comment_id']).first()
                if comment == None:
                    comment = Comment(
                        idComment=str(item['comment_id']),
                        comment=item['content'],
                        createTime=timestamp_to_datetime(
                            item['creation_time']),
                        userLike=item['userlike']
                    )
                    comment.save()

                comments.append(comment)

                if item['comment_id'] != item['parent_id'] \
                        and 'replays' in item \
                        and 'total' in item['replays']:
                    comments.extend(get_children_comment(
                        id_post,
                        comment['parent_id']
                    ))
            except:
                print()

    return comments


# TODO ====== Main =============================================================

def get_info_post_by_date(url, date):
    info_posts = []
    status = True
    page_index = 1
    while status:
        info_posts_page_current, status = get_info_post_by_list(
            url.format(page=page_index),
            date=date
        )

        for index_post, info_post in enumerate(info_posts_page_current, start=0):
            post, tags, topic = get_info_post(
                info_post['link'],
                info_post['id']
            )

            info_posts_page_current[index_post]['post'] = post

            print('- {title}'.format(
                title=post.title
            ))

            if tags != None:
                for tag in tags:
                    if post not in tag.posts:
                        tag.posts.append(post)
                    tag.save()

            if topic != None:
                if post not in topic.posts:
                    topic.posts.append(post)
                topic.save()

        info_posts.extend(info_posts_page_current)

        info_posts.extend(info_posts_page_current)
        print("Pages: [{page}] Number of post: {numOfPost}".format(
            page=page_index,
            numOfPost=len(info_posts_page_current)
        ))
        page_index = page_index + 1
        if status:
            status = len(info_posts_page_current)

    return remove_duplicate(info_posts)


def get_info_post_by_pages(url, page):
    info_posts = []
    page_index = 1
    for page_index in range(1, page+1):
        info_posts_page_current, status = get_info_post_by_list(
            url.format(page=page_index),
            date=None
        )
        info_posts.extend(info_posts_page_current)
        print("Pages: [{page}] Number of post: {numOfPost}".format(
            page=page_index,
            numOfPost=len(info_posts_page_current)
        ))

    return remove_duplicate(info_posts)


def get_info_post_by_category(category, from_date, to_date):
    info_posts = []
    total_category = len(category)
    for index_category, item in enumerate(category, start=1):
        status = True
        page_index = 1
        category = get_info_category(item['id'], item['title'])

        print('category [{indexCategory}/{totalCategory}]: [{id}] {title}'.format(
            indexCategory=index_category,
            totalCategory=index_category,
            title=item['title'],
            id=item['id']
        ))

        while status:
            url = 'https://vnexpress.net/category/day?cateid={cateid}&allcate={allcate}&fromdate={fromdate}&todate={todate}&page={page}'.format(
                cateid=item['id'],
                allcate=item['id'],
                page=page_index,
                fromdate=datetime_to_timestamp(from_date),
                todate=datetime_to_timestamp(to_date)
            )

            info_posts_page_current, status = get_info_post_by_list(
                url,
                date=None
            )
            for index_post, info_post in enumerate(info_posts_page_current, start=0):
                post, tags, topic = get_info_post(
                    info_post['link'],
                    info_post['id']
                )

                info_posts_page_current[index_post]['post'] = post

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

            info_posts.extend(info_posts_page_current)

            print("Pages: [{page}] Number of post: {numOfPost}".format(
                page=page_index,
                numOfPost=len(info_posts_page_current)
            ))
            page_index = page_index + 1
            status = len(info_posts_page_current) != 0

    return remove_duplicate(info_posts)


def crawl_all_n_days(n):
    category = get_category_from_json()
    today = format_date(date.today())
    from_date = format_date(date.today() - timedelta(days=n))

    info_posts = get_info_post_by_date(
        "https://vnexpress.net/chu-de/covid-19-1299-p{page}", from_date)
    total_post = len(info_posts)
    print("="*20 + "get comment" + "="*20)
    total = 1
    for index, info_post in enumerate(info_posts, start=1):
        print("Post[{index}/{total}]: [{post}]".format(
            post=info_post['id'],
            index=index,
            total=total_post
        ))
        comments = get_comments(str(info_post['id']))

        total_comment = len(comments)
        for index, comment in enumerate(comments, start=1):
            print('[{index}/{totalComment}] - {comment}'.format(
                comment=comment.comment,
                index=index,
                totalComment=total_comment
            ))
            if comment not in info_post['post'].comments:
                info_post['post'].comments.append(comment)
        info_post['post'].save()
        total = total + total_comment


def crawl_all_three_days():
    crawl_all_n_days(3)


def crawl_all_a_week():
    crawl_all_n_days(7)


def crawl_all_a_month():
    crawl_all_n_days(30)


if __name__ == '__main__':
    start = time.time()

    # crawl_all_n_days(30)
    # crawlAllThreeDays()
    # crawl_all_a_week()
    # crawl_all_a_month()

    end = time.time()
    print(time.strftime("%H:%M:%S", time.gmtime(end - start)))
