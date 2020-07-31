import os
from mongoengine import *
from datetime import datetime, date, timedelta
from dateutil import parser

MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", 'vnexpress')
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME", 'twoman')
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", 'twoman123456')
MONGODB_HOSTNAME = os.environ.get("MONGODB_HOSTNAME", 'labando.com')

if MONGODB_USERNAME != '' and MONGODB_PASSWORD != '':
    connect(
        db=MONGODB_DATABASE,
        username=MONGODB_USERNAME,
        password=MONGODB_PASSWORD,
        host=MONGODB_HOSTNAME,
        port=27017,
        alias='db'
    )
else:
    connect(
        db=MONGODB_DATABASE,
        host=MONGODB_HOSTNAME,
        port=27017,
        alias='db'
    )


def format_date(date):
    return str(f'{date:%m/%d/%Y}')


def filter_posts_by_date(postsSource, date_from, date_to):
    if type(date_from) is datetime:
        date_from = format_date(date_from)

    if type(date_to) is datetime:
        date_to = format_date(date_to)

    posts = list(filter(
        lambda item:
            item.publishTime <= parser.parse(date_to) + timedelta(days=1) and
            item.publishTime >= parser.parse(date_from), list(postsSource)
    ))
    return posts


class Comment(Document):
    __version = DecimalField(default=4)
    idComment = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.utcnow)
    comment = StringField(required=True)
    label = IntField()
    createTime = DateTimeField()
    userLike = DecimalField()
    meta = {'db_alias': 'db'}

    def is_label_neg(self):
        return self.label == 0

    def is_label_pos(self):
        return self.label == 1

    def get_comment(self):
        return self.comment


class Post(Document):
    __version = DecimalField(default=3)
    idPost = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.utcnow)
    title = StringField(required=True)
    publishTime = DateTimeField()
    url = StringField(required=True)
    thumbnailUrl = StringField(required=False)
    description = StringField(required=False)
    comments = ListField(ReferenceField(Comment))
    meta = {'db_alias': 'db'}

    def get_comments(self):
        return self.comments


class Tag(Document):
    __version = DecimalField(default=2)
    idTag = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.utcnow)
    name = StringField(required=True)
    url = StringField(required=True)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}

    def get_posts_by_date(self, date_from, date_to):
        posts = filter_posts_by_date(self.posts, date_from, date_to)
        return posts


class TopTag(Document):
    __version = DecimalField(default=2)
    created = DateTimeField(default=datetime.utcnow)
    unitTime = StringField(required=True)
    dateFrom = DateTimeField(required=True)
    dateTo = DateTimeField(required=True)
    tags = ListField(ReferenceField(Tag))
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}


class Topic(Document):
    __version = DecimalField(default=2)
    idTopic = StringField(required=True, unique=True)
    articleTopic = StringField(required=True)
    created = DateTimeField(default=datetime.utcnow)
    title = StringField(required=True)
    description = StringField(required=False)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}

    def get_posts_by_date(self, date_from, date_to):
        posts = filter_posts_by_date(self.posts, date_from, date_to)
        return posts


class TopTopic(Document):
    __version = DecimalField(default=2)
    created = DateTimeField(default=datetime.utcnow)
    unitTime = StringField(required=True)
    dateFrom = DateTimeField(required=True)
    dateTo = DateTimeField(required=True)
    topics = ListField(ReferenceField(Topic))
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}


class Category(Document):
    __version = DecimalField(default=2)
    idCategory = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.utcnow)
    title = StringField(required=True)
    description = StringField(required=False)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}

    def get_posts_by_date(self, date_from, date_to):
        posts = filter_posts_by_date(self.posts, date_from, date_to)
        return posts
