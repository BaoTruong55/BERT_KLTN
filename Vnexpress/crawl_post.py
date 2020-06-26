import urllib.request
import json
from collections import namedtuple
import csv
from bs4 import BeautifulSoup
import requests

# get comment from vnexpress
prefix_id = 'test_'
index = 0


def get_json_from_url(url):
    with urllib.request.urlopen(url) as newUrl:
        if newUrl != None:
            document = newUrl.read().decode()
            dataJson = json.loads(document,
                                  object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return dataJson

# URL = "https://vnexpress.net/tho-dan-giua-covid-19-4094885.html"


def get_info_post_crawl(URL):
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    idPost = soup.find('meta', attrs={'name': 'its_id'}).get('content')

    description = soup.find('meta', attrs={'name': 'description'})
    if description != None:
        description = description['content']
    else:
        description = ''

    thumbnail_url = soup.find('meta', attrs={'itemprop': 'thumbnailUrl'})
    if thumbnail_url != None:
        thumbnail_url = thumbnail_url['content']
    else:
        thumbnail_url = ''
    title = soup.find('title').text
    return idPost, title, description, thumbnail_url

# ! Get reply comment from a comment in a post


def get_children_comment(id_post, id_parent):
    list_comment = []
    url = "https://usi-saas.vnexpress.net/index/getreplay?limit=1000000&objecttype=1&offset=0&objectid={objectid}&id={id}".format(
        objectid=id_post, id=id_parent)

    data_comments = get_json_from_url(url)
    if type(data_comments.data) is not list:
        for i in data_comments.data.items:
            arrList = i.content.split(";", 1)
            list_comment.append(arrList[-1])

    return list_comment

# ! Get parent comment in a post


def get_comments_crawl(id_post):
    list_comment = []
    url = "https://usi-saas.vnexpress.net/index/get?limit=1000000&siteid=1000000&objecttype=1&objectid={objectid}".format(
        objectid=id_post)
    data_comments = get_json_from_url(url)
    if type(data_comments.data) is not list:
        for i in data_comments.data.items:
            list_comment.append(i.content)
            list_comment.extend(get_children_comment(id_post, i.parent_id))

    return list_comment

