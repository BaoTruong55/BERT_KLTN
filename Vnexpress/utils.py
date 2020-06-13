import unidecode
import requests
import dateutil
import urllib.request
import json
from datetime import date, timedelta, datetime

PREFIX_ID = 'test_'


def get_json_from_url(url):
    content = requests.get(url)
    dataJson = content.json()

    return dataJson


def datetime_to_timestamp(date):
    return int(dateutil.parser.parse(date, dayfirst=True).timestamp())


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(int(timestamp))


def unmark_vietnamese(str):
    return unidecode.unidecode(str)


def first_thing_write_csv(path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'text'])


def format_date(date):
    return str(f'{date:%d/%m/%Y}')


def remove_duplicate(list_info_posts):
    ids_post = []
    info_posts = []
    for info_post_current in list_info_posts:
        if info_post_current['id'] not in ids_post:
            info_posts.append(info_post_current)
            ids_post.append(info_post_current['id'])

    return info_posts


def write_cv_file(path, list_data, total):
    with open(path, 'a+', newline='') as file:
        writer = csv.writer(file)
        for num, data in enumerate(list_data, start=total):
            id = "{prefix_id}{len_zero}{number}".format(
                prefix_id=PREFIX_ID,
                len_zero='0' * (6 - len(str(num))),
                number=num
            )
            writer.writerow([id, data])


def get_category_from_json():
    with open('./category.json') as f:
        data = json.load(f)

    return data


def GET_COMMENT_TEXT(item): return item.comment
def GET_COMMENT_ID(item): return item.idComment

