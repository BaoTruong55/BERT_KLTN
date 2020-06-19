import urllib.request
import json
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
from infer_predict import *
from dateutil import parser

PATH_SAVE_CSV = 'crawlVnExp-temp-da.csv'


def get_info_topic(id_topic, article_topic):
    topic = Topic.objects(idTopic=id_topic)
    if len(topic) != 0:
        return topic[0]

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
        tag = Tag.objects(idTag=str(item['tag_id']))

        if len(tag) == 0:
            tag = Tag(
                idTag=str(item['tag_id']),
                name=item['tag_name'],
                url=item['tag_url']
            )
            tag.save()
        else:
            tag = tag[0]

        tags.append(tag)

    return tags


def get_info_post(url, id_post):
    post = Post.objects(idPost=id_post)
    if len(post) != 0:
        return post[0], None, None

    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')

    # script have info topicid, article topic, tag id
    script = soup.find_all('script')[3]

    topic_id = re.findall("{'article_topic_ID':'(.*?)'}", script.text)
    if len(topic_id) != 0:
        topic_id = topic_id[0]
    else:
        topic_id = ''

    article_topic = re.findall("{'article_topic':'(.*?)'}", script.text)
    if len(article_topic) != 0:
        article_topic = '-'.join(unmark_vietnamese(
            article_topic[0].lower()).split(' '))
    else:
        article_topic = ''

    tag_ids = re.findall("{'tag_id':'(.*?)'}", script.text)
    if len(tag_ids) != 0:
        tag_ids = tag_ids[0].split(', ')
    else:
        tag_ids = []

    info_tags = None
    if len(tag_ids) != 0:
        info_tags = get_info_tag(tag_ids)

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
            and dtype(data_comments['data']) is not list:
        for item in data_comments['data']['items']:
            comment = Comment.objects(idComment=item['comment_id'])
            if len(comment) == 0:
                comment = Comment(
                    idComment=str(item['comment_id']),
                    comment=item['content'],
                    createTime=timestamp_to_datetime(item['creation_time']),
                    userLike=item['userlike']
                )
                comment.save()
            else:
                comment = comment[0]

            comments.append(comment)
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
            comment = Comment.objects(idComment=item['comment_id'])
            if len(comment) == 0:
                comment = Comment(
                    idComment=str(item['comment_id']),
                    comment=item['content'],
                    createTime=timestamp_to_datetime(item['creation_time']),
                    userLike=item['userlike']
                )
                comment.save()
            else:
                comment = comment[0]

            comments.append(comment)

            if item['comment_id'] != item['parent_id'] \
                    and 'replays' in item \
                    and 'total' in item['replays']:
                comments.extend(get_children_comment(
                    id_post,
                    comment['parent_id']
                ))

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
        info_posts.extend(info_posts_page_current)
        print("Pages: [{page}] Number of post: {numOfPost}".format(
            page=page_index,
            numOfPost=len(info_posts_page_current)
        ))
        page_index = page_index + 1
        if status:
            status = len(info_posts_page_current)

    return remove_duplicate(info_posts)


def get_info_post_by_page(url, page):
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


def filter_posts_by_date(posts_source, date_from, date_to):
    posts = list(filter(
        lambda item:
            item.publishTime <= parser.parse(date_to) and
            item.publishTime >= parser.parse(date_from),
        posts_source
    ))
    return posts


def posts_in_topic(id, date_from, date_to):
    posts_in_topic = Topic.objects.get(idTopic=id).posts
    return filter_posts_by_date(posts_in_topic, date_from, date_to)


def posts_in_tag(id, date_from, date_to):
    posts_in_tag = Tag.objects.get(idTag=id).posts
    return filter_posts_by_date(posts_in_tag, date_from, date_to)


def top_topics(days):
    today = format_date(date.today())
    from_date = format_date(date.today() - timedelta(days=days))
    topics = Topic.objects()

    topics_obj = []
    for topic in topics:
        topics_obj.append({
            "topic": topic,
            "posts": posts_in_topic(topic.idTopic, from_date, today)
        })

    topics_obj = list(filter(lambda item: len(item["posts"]) > 0, topics_obj))
    topics_obj.sort(key=lambda item: len(item["posts"]), reverse=True)

    topics_result = list(map(lambda item: item["topic"], topics_obj[:30]))
    posts_result = sum(
        list(map(lambda item: item["posts"], topics_obj[:30])),
        []
    )

    return topics_result, posts_result, from_date, today


def top_tags(days):
    today = format_date(date.today())
    from_date = format_date(date.today() - timedelta(days=days))
    tags = Tag.objects()

    tags_obj = []

    for tag in tags:
        tags_obj.append({
            "tag": tag,
            "posts": posts_in_tag(tag.idTag, from_date, today)
        })

    tags_obj = list(filter(lambda item: len(item["posts"]) > 10, tags_obj))
    tags_obj.sort(key=lambda item: len(item["posts"]), reverse=True)

    tags_result = list(map(lambda item: item["tag"], tags_obj[:30]))
    posts_result = sum(
        list(map(lambda item: item["posts"], tags_obj[:30])), [])

    return tags_result, posts_result, from_date, today


def top_tag_in_week():
    tags, posts, date_from, date_to = top_tags(7)
    top_tag = TopTag(
        unitTime="week",
        tags=tags,
        posts=posts,
        dateFrom=date_from,
        dateTo=date_to
    )
    top_tag.save()


def top_tag_in_month():
    tags, posts, date_from, date_to = top_tags(30)
    top_tag = TopTag(
        unitTime="month",
        tags=tags,
        posts=posts,
        dateFrom=date_from,
        dateTo=date_to
    )
    top_tag.save()


def top_topic_in_week():
    topics, posts, date_from, date_to = top_topics(7)
    top_topic = TopTopic(
        unitTime="week",
        topics=topics,
        posts=posts,
        dateFrom=date_from,
        dateTo=date_to
    )
    top_topic.save()


def top_topic_in_month():
    topics, posts, date_from, date_to = top_topics(30)
    top_topic = TopTopic(
        unitTime="month",
        topics=topics,
        posts=posts,
        dateFrom=date_from,
        dateTo=date_to
    )
    top_topic.save()


def crawl_all_n_days(n):
    category = get_category_from_json()
    today = format_date(date.today())
    from_date = format_date(date.today() - timedelta(days=n))

    info_posts = get_info_post_by_category(category, from_date, today)
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


def predict_comment():
    comments = Comment.objects(label=None)
    print(len(comments))
    if len(comments) > 0:
        comment_text = list(map(GET_COMMENT_TEXT, comments))
        comment_id = list(map(GET_COMMENT_ID, comments))
        print(comment_text)
        print(comment_id)
        df = nomalize_data_comment_vnexpress(comment_id, comment_text)
        df_result = predict_data(df)
        for comment in comments:
            comment.label = df_result[df_result['id']
                                      == comment.idComment]['label']
            comment.save()
    print('Done')


if __name__ == '__main__':
    start = time.time()

    # crawl_all_n_days(0)
    # crawlAllThreeDays()
    # crawlAllAWeek()
    # crawlAllAMonth()
    crawl_all_three_days()
    predict_comment()

    top_topic_in_week()
    top_topic_in_month()
    top_tag_in_week()
    top_tag_in_month()

    end = time.time()
    print(time.strftime("%H:%M:%S", time.gmtime(end - start)))
