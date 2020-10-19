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
from flask import jsonify
from infer_predict import *

import time


def random_comments(comments, size):
    start = time.time()
    import random
    comments = list(comments)
    count_comment = len(comments)
    number_random = random.sample(
        range(0, count_comment), min(size, count_comment))
    print("get random comments")

    result = list(map(lambda index: comments[index], number_random))

    end = time.time()
    print(time.strftime("%H:%M:%S", time.gmtime(end - start)))

    return result


def predict_comment():
    count_comment = 5000
    while True:
        time.sleep(2.4)
        comments = Comment.objects(label=None)
        comments = random_comments(comments, 5000)
        count_comment = len(comments)
        if len(comments) > 0:
            comment_text = list(map(GET_COMMENT_TEXT, comments))
            comment_id = list(map(GET_COMMENT_ID, comments))
            df = nomalize_data_comment_vnexpress(comment_id, comment_text)
            df_result = predict_data(df)
            for comment in comments:
                comment.label = df_result[df_result['id']
                                          == comment.idComment]['label']
                comment.save()
    print('Done')


if __name__ == '__main__':
    start = time.time()

    predict_comment()

    end = time.time()
    print(time.strftime("%H:%M:%S", time.gmtime(end - start)))
