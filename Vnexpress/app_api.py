
from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from infer_predict import *
from post_crawl import *
from model_vnexpress import *
from flask_cors import CORS, cross_origin
from datetime import datetime, date, timedelta
from dateutil import parser
# TODO ==== Main ===============================================================
app = Flask(__name__)
CORS(app)
api = Api(app)

isLabelNeg = lambda item: item.label == 0
isLabelPos = lambda item: item.label == 1
getComment = lambda item: item.comment
getUserLike = lambda item: item.userLike
getCommentsInPost = lambda item: item.comments
getIdPost = lambda item: item.idPost

def formatDate(date):
    return str(f'{date:%m/%d/%Y}')

def classifyCommentByDate(posts):
    classifyPost = {}
    for post in posts:
        if post.publishTime.strftime('%m/%d/%Y') in classifyPost:
            classifyPost[post.publishTime.strftime('%m/%d/%Y')].append(post)
        else:
            classifyPost[post.publishTime.strftime('%m/%d/%Y')] = [post]
    
    listPost = list(
        map(
            lambda item: {
                "title": item.title,
                "url": item.url,
                "thumbnailUrl": item.thumbnailUrl,
                "description": item.description,
                "count_comment": len(item.comments)
            },
            posts
        )
    )


    listPost.sort(key=lambda item: item['count_comment'], reverse=True)

    classifyComment = {}
    for key, value in classifyPost.items():
        comments = sum(list(map(getCommentsInPost, value)), [])

        comments_neg = list(filter(isLabelNeg, comments))
        comments_pos = list(filter(isLabelPos, comments))

        comments_text_neg = list(map(getComment, comments_neg))
        comments_text_pos = list(map(getComment, comments_pos))


        classifyComment[key] = {
            "pos": len(comments_pos),
            "neg": len(comments_neg),
        }
    
    classifyCommentFormat = []
    for key in classifyComment:
        classifyCommentFormat.append({
            "date": key,
            "data": classifyComment[key]
        })

    return classifyCommentFormat, listPost[:20]


def tag(id, dateFrom, dateTo):
    postsInTag = Tag.objects.get(idTag=id).posts
    
    posts = Post.objects(
        publishTime__gte=parser.parse(dateFrom),
        publishTime__lte=parser.parse(dateTo),
        idPost__in = list(map(getIdPost, postsInTag))
    )

    return classifyCommentByDate(posts)

def category(id, dateFrom, dateTo):
    postsInCategory = Category.objects.get(idCategory=id).posts

    posts = Post.objects(
        publishTime__gte=parser.parse(dateTo),
        publishTime__lte=parser.parse(dateFrom),
        idPost__in = list(map(getIdPost, postsInCategory))
    )

    return classifyCommentByDate(posts)

def topic(id, dateFrom, dateTo):
    postsInTopic = Topic.objects.get(idTopic=id).posts
    posts = Post.objects(
        publishTime__gte=parser.parse(dateTo),
        publishTime__lte=parser.parse(dateFrom),
        idPost__in = list(map(getIdPost, postsInTopic))
    )

    return classifyCommentByDate(posts)

def countPostInTopic(id, dateFrom, dateTo):
    postsInTopic = Topic.objects.get(idTopic=id).posts

    if len(postsInTopic) > 1:
        posts = Post.objects(
            publishTime__gte=parser.parse(dateFrom),
            publishTime__lte=parser.parse(dateTo),
            idPost__in = list(map(getIdPost, postsInTopic))
        )
    else:
        posts = []

    return len(posts)   

def top20Topic():
    today = formatDate(date.today())
    fromDate  = formatDate(date.today() - timedelta(days=30))
    topics = Topic.objects()

    topics_obj = []
    for topic in topics:
        topics_obj.append({
            "idTopic": topic.idTopic, 
            "title" : topic.title,
            "description": topic.description,
            "count_post": countPostInTopic(topic.idTopic, fromDate, today)
        })
    topics_obj = list(filter(lambda item: item["count_post"] > 0, topics_obj))
    topics_obj.sort(key=lambda item: item["count_post"], reverse=True)

    return topics_obj

def countPostInTag(idTag, dateFrom, dateTo):
    postsInTag = Tag.objects().get(idTag=idTag).posts

    if len(postsInTag) > 1:
        posts = Post.objects(
            publishTime__gte=parser.parse(dateFrom),
            publishTime__lte=parser.parse(dateTo),
            idPost__in=list(map(getIdPost, postsInTag))
        )
    else:
        posts = []

    return len(posts)

def top20Tag():
    today = formatDate(date.today())
    fromDate  = formatDate(date.today() - timedelta(days=30))
    tags = Tag.objects()

    tags_obj = []
    for tag in tags:
        tags_obj.append({
            "idTag": tag.idTag,
            "name" : tag.name,
            "count_post": countPostInTag(tag.idTag, fromDate, today)
        })
    tags_obj = list(filter(lambda item: item["count_post"] > 0, tags_obj))
    
    tags_obj.sort(key=lambda item: item["count_post"], reverse=True)
    
    return tags_obj[:20]


class Vnexpress(Resource):
    def get(self):
        url = request.args.get('url')
        idPost, title, description, thumbnailUrl =  getInfoPost(url)
        comments = getComments(idPost)

        if len(comments) == 0:
            return {"Error": "The article has no comments"}
        
        df = NomalizeData(comments)
        df_result = PredictData(df)
        df_output = DataFrame(df_result, columns= ['data_text', 'label'])
        df_negatives = df_output[df_output['label'] == 0]
        df_possitives = df_output[df_output['label'] == 1]
        
        output = {
            "title": title,
            "description": description,
            "thumbnailUrl": thumbnailUrl,
            "pos": len(df_possitives.index),
            "neg": len(df_negatives.index),
            "commentPos": df_possitives.to_dict("records"),
            "commentNeg": df_negatives.to_dict("records")
        }

        result = Response(json.dumps(output), mimetype='application/json')
        return result

class Covid(Resource):
    def get(self):
        dateTo   = request.args.get('dateto')
        dateFrom = request.args.get('datefrom')
        sentiment_by_date, top_post = tag('1266196', dateFrom, dateTo)
        total_pos = 0
        total_neg = 0
        for item in sentiment_by_date:
            total_pos = total_pos + item['data']['pos']
            total_neg = total_neg + item['data']['neg']

        result = {
            "total_pos": total_pos,
            "total_neg": total_neg,
            "top_post": top_post,
            "sentiment_by_date": sentiment_by_date
        }

        return Response(json.dumps(result), mimetype='application/json')

class TopTopic(Resource):
    def get(self):
        topics = top20Topic()
        
        return Response(json.dumps(topics), mimetype='application/json')


class TopTag(Resource):
    def get(self):
        tags = top20Tag()
        return Response(json.dumps(tags), mimetype='application/json')

class Categories(Resource):
    def get(seft):
        category = Category.objects()
        listCategory = list(
            map(
                lambda item: {
                    "idCategory": item.idCategory,
                    "title": item.title,
                    "description": item.description
                },
                category
            )
        )
        return Response(json.dumps(listCategory), mimetype='application/json')

class CategorySentiment(Resource):
    def get(seft):
        idCategory  = request.args.get('idcategory')
        dateTo   = request.args.get('dateto')
        dateFrom = request.args.get('datefrom')
        sentiment_by_date, top_post = category(idCategory, dateFrom, dateTo)
        total_pos = 0
        total_neg = 0
        for item in sentiment_by_date:
            total_pos = total_pos + item['data']['pos']
            total_neg = total_neg + item['data']['neg']

        result = {
            "total_pos": total_pos,
            "total_neg": total_neg,
            "top_post": top_post,
            "sentiment_by_date": sentiment_by_date
        }
        return Response(json.dumps(result), mimetype='application/json')

class CategorySentiment(Resource):
    def get(seft):
        idCategory  = request.args.get('idcategory')
        dateTo   = request.args.get('dateto')
        dateFrom = request.args.get('datefrom')
        sentiment_by_date, top_post = category(idCategory, dateFrom, dateTo)
        total_pos = 0
        total_neg = 0
        for item in sentiment_by_date:
            total_pos = total_pos + item['data']['pos']
            total_neg = total_neg + item['data']['neg']

        result = {
            "total_pos": total_pos,
            "total_neg": total_neg,
            "top_post": top_post,
            "sentiment_by_date": sentiment_by_date
        }
        return Response(json.dumps(result), mimetype='application/json')

class TagSentiment(Resource):
    def get(seft):
        idTag  = request.args.get('idtag')

        if request.args.get('dateto') != None:
            dateTo   = request.args.get('dateto')
        else:    
            dateTo = formatDate(date.today())
        

        if request.args.get('datefrom') != None:
            dateFrom   = request.args.get('datefrom')
        else:    
            dateFrom = formatDate(date.today() - timedelta(days=30))

        sentiment_by_date, top_post = tag(idTag, dateFrom, dateTo)
        total_pos = 0
        total_neg = 0
        for item in sentiment_by_date:
            total_pos = total_pos + item['data']['pos']
            total_neg = total_neg + item['data']['neg']

        result = {
            "total_pos": total_pos,
            "total_neg": total_neg,
            "top_post": top_post,
            "sentiment_by_date": sentiment_by_date
        }
        return Response(json.dumps(result), mimetype='application/json')

class TopicSentiment(Resource):
    def get(seft):
        idTopic  = request.args.get('idtopic')
        if request.args.get('dateto') != None:
            dateTo   = request.args.get('dateto')
        else:    
            dateTo = formatDate(date.today())
        

        if request.args.get('datefrom') != None:
            dateFrom   = request.args.get('datefrom')
        else:    
            dateFrom = formatDate(date.today() - timedelta(days=30))
        
        sentiment_by_date, top_post = topic(idTopic, dateFrom, dateTo)
        total_pos = 0
        total_neg = 0
        for item in sentiment_by_date:
            total_pos = total_pos + item['data']['pos']
            total_neg = total_neg + item['data']['neg']

        result = {
            "total_pos": total_pos,
            "total_neg": total_neg,
            "top_post": top_post,
            "sentiment_by_date": sentiment_by_date
        }
        return Response(json.dumps(result), mimetype='application/json')

api.add_resource(Vnexpress, '/vnexpress')
api.add_resource(Covid, '/vnexpress/covid')
api.add_resource(TopTopic, '/vnexpress/toptopic')
api.add_resource(TopTag, '/vnexpress/toptag')
api.add_resource(Categories, '/vnexpress/categories')
api.add_resource(TopicSentiment,'/vnexpress/topicsentiment')
api.add_resource(CategorySentiment,'/vnexpress/categorysentiment')
api.add_resource(TagSentiment,'/vnexpress/tagsentiment')

if __name__ == '__main__':
    app.run()