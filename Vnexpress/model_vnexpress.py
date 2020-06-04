
from mongoengine import *
import datetime

connect('mongoengine_test', host='localhost', port=27017,  alias='db1')

class Comment(Document):
    __version = DecimalField(default=1)
    created = DateTimeField(default=datetime.datetime.utcnow)
    # modify = DateTimeField(default=datetime.datetime.utcnow)
    comment = StringField(required=True)
    label = DecimalField()
    meta = {'db_alias': 'db1'}

class Post(Document):
    __version = DecimalField(default=1)
    created = DateTimeField(default=datetime.datetime.utcnow)
    # modify = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
    idPost = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now)
    timeStamp = DecimalField()
    link = StringField(required=True)
    link_thumpnail = StringField(required=False)
    comments = ListField(ReferenceField(Comment))
    meta = {'db_alias': 'db1'}

class Category(Document):
    __version = DecimalField(default=1)
    created = DateTimeField(default=datetime.datetime.utcnow)
    # modify = DateTimeField(default=datetime.datetime.utcnow)
    name = StringField(required=True, max_lenght=200)
    alias = StringField(requires=False)
    description = StringField(required=False)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db1'}

class Topic(Document):
    __version = DecimalField(default=1)
    created = DateTimeField(default=datetime.datetime.utcnow)
    # modify = DateTimeField(default=datetime.datetime.utcnow)
    name = StringField(required=True, max_lenght=200)
    alias = StringField(requires=False)
    description = StringField(required=False)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db1'}

class Category(Document):
    __version = DecimalField(default=1)
    created = DateTimeField(default=datetime.datetime.utcnow)
    # modify = DateTimeField(default=datetime.datetime.utcnow)
    name = StringField(required=True, max_lenght=200)
    alias = StringField(requires=False)
    description = StringField(required=False)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db1'}


# category = Category(
#     name='Thời sự',
#     alias='thoi_su',
#     posts= [
#         Post(
#             title = 'post sample',
#             idPost = '123',
#             link = 'https://www.abc.com/xyz',
#             comments = [
#                 Comment(
#                     comment = 'abc',
#                 ).save()
#             ]
#         ).save()
#     ]
# )
# category.save()