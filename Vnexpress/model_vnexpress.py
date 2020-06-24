import os
from mongoengine import *
import datetime

MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", 'vnexpress')
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME", '')
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", '')
MONGODB_HOSTNAME = os.environ.get("MONGODB_HOSTNAME", 'localhost')

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


class Comment(Document):
    __version = DecimalField(default=4)
    idComment = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    comment = StringField(required=True)
    label = IntField()
    createTime = DateTimeField()
    userLike = DecimalField()
    meta = {'db_alias': 'db'}


class Post(Document):
    __version = DecimalField(default=3)
    idPost = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
    publishTime = DateTimeField()
    url = StringField(required=True)
    thumbnailUrl = StringField(required=False)
    description = StringField(required=False)
    comments = ListField(ReferenceField(Comment))
    meta = {'db_alias': 'db'}


class Tag(Document):
    __version = DecimalField(default=2)
    idTag = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    name = StringField(required=True)
    url = StringField(required=True)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}


class TopTag(Document):
    __version = DecimalField(default=2)
    created = DateTimeField(default=datetime.datetime.utcnow)
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
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
    description = StringField(required=False)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}


class TopTopic(Document):
    __version = DecimalField(default=2)
    created = DateTimeField(default=datetime.datetime.utcnow)
    unitTime = StringField(required=True)
    dateFrom = DateTimeField(required=True)
    dateTo = DateTimeField(required=True)
    topics = ListField(ReferenceField(Topic))
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}


class Category(Document):
    __version = DecimalField(default=2)
    idCategory = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
    description = StringField(required=False)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db'}
