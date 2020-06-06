
from mongoengine import *
import datetime

connect('vnexpress', host='localhost', port=27017,  alias='db1')

class Comment(Document):
    __version = DecimalField(default=2)
    idComment = StringField(required=True, unique = True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    comment = StringField(required=True)
    label = DecimalField()
    createTime = DateTimeField()
    meta = {'db_alias': 'db1'}

class Post(Document):
    __version = DecimalField(default=2)
    idPost = StringField(required=True, unique = True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
    # date = DateTimeField(default=datetime.datetime.now)
    timeStamp = DecimalField()
    link = StringField(required=True)
    link_thumbnail = StringField(required=False)
    description = StringField(required=False)
    comments = ListField(ReferenceField(Comment))
    meta = {'db_alias': 'db1'}

class Tag(Document):
    __version = DecimalField(default=2)
    idTag = StringField(required=True, unique = True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    name = StringField(required=True)
    url = StringField(required=True)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db1'}

class Topic(Document):
    __version = DecimalField(default=2)
    idTopic = StringField(required=True, unique = True)
    articleTopic = StringField(required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
    description = StringField(required=False)
    posts = ListField(ReferenceField(Post))
    meta = {'db_alias': 'db1'}

class Category(Document):
    __version = DecimalField(default=2)
    idCategory = StringField(required=True, unique = True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField(required=True)
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