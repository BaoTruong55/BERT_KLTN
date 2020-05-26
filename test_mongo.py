# from pymongo import MongoClient

# client = MongoClient('localhost', 27017)

# db = client['pymongo_test']

# posts = db.posts
# post_1 = {
#     'title': 'Python and MongoDB',
#     'content': 'PyMongo is fun, you guys',
#     'author': 'Scott'
# }
# post_2 = {
#     'title': 'Virtual Environments',
#     'content': 'Use virtual environments, you guys',
#     'author': 'Scott'
# }
# post_3 = {
#     'title': 'Learning Python',
#     'content': 'Learn Python, it is easy',
#     'author': 'Bill'
# }
# new_result = posts.insert_many([post_1, post_2, post_3])
# print('Multiple posts: {0}'.format(new_result.inserted_ids))

# bills_post = posts.find_one({'author': 'Bill'})
# print(bills_post)


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

# comment = Comment(
#     comment = 'abc',
# )

# post = Post(
#     title = 'post sample',
#     idPost = '123',
#     link = 'https://www.abc.com/xyz'
# )

# post.comments.append(comment)

category = Category(
    name='Thời sự',
    alias='thoi_su',
    posts= [
        Post(
            title = 'post sample',
            idPost = '123',
            link = 'https://www.abc.com/xyz',
            comments = [
                Comment(
                    comment = 'abc',
                ).save()
            ]
        ).save()
    ]
)
# category.posts.append(comment)
# category.
# category.posts.save()
category.save()
# print(category.posts.comments)
# categorsy.save()       # This will perform an insert
# print(post_1.title)
# post_1.title = 'A Better Post Title'
# post_1.save()       # This will perform an atomic edit on "title"
# print(post_1.title)
