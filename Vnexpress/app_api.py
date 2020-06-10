
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
    
    classifyComment = {}
    for key, value in classifyPost.items():
        comments = sum(list(map(getCommentsInPost, value)), [])

        comments_neg = list(filter(isLabelNeg, comments))
        comments_pos = list(filter(isLabelPos, comments))

        comments_text_neg = list(map(getComment, comments_neg))
        comments_text_pos = list(map(getComment, comments_pos))


        classifyComment[key] = {
            "pos": {
                "count": len(comments_pos),
                # "comments": comments_text_pos
            },
            "neg": {
                "count": len(comments_neg),
                # "comments": comments_text_neg
            }
        }

    return classifyComment


def tag(id, dateTo, dateFrom):
    postsInTag = Tag.objects.get(idTag=id).posts
    
    posts = Post.objects(
        publishTime__gte=parser.parse(dateTo),
        publishTime__lte=parser.parse(dateFrom),
        idPost__in = list(map(getIdPost, postsInTag))
    )

    return classifyCommentByDate(posts)

def category(id, dateTo, dateFrom):
    postsInCategory = Category.objects.get(idCategory=id).posts
    posts = Post.objects(
        publishTime__gte=parser.parse(dateTo),
        publishTime__lte=parser.parse(dateFrom),
        idPost__in = list(map(getIdPost, postsInCategory))
    )
    
    return classifyCommentByDate(posts)

def topic(id, dateTo, dateFrom):
    postsInTopic = Topic.objects.get(idTopic=id).posts
    posts = Post.objects(
        publishTime__gte=parser.parse(dateTo),
        publishTime__lte=parser.parse(dateFrom),
        idPost__in = list(map(getIdPost, postsInTopic))
    )

    return classifyCommentByDate(posts)

def countPostInTopic(id, dateTo, dateFrom):
    postsInTopic = Topic.objects.get(idTopic=id).posts

    if len(postsInTag) > 1:
        posts = Post.objects(
            publishTime__gte=parser.parse(dateTo),
            publishTime__lte=parser.parse(dateFrom),
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
            # "title" : topic.title,
            # "description": topic.description,
            "count_post": countPostInTopic(topic.idTopic, today, fromDate)
        })
    topics_obj = list(filter(lambda item: item["count_post"] > 0, topics_obj))
    topics_obj.sort(key=lambda item: item["count_post"], reverse=True)
    
    return topics_obj

def countPostInTag(idTag, dateTo, dateFrom):
    postsInTag = Tag.objects().get(idTag=idTag).posts

    if len(postsInTag) > 1:
        posts = Post.objects(
            # publishTime__gte=parser.parse(dateTo),
            # publishTime__lte=parser.parse(dateFrom),
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
            "name" : tag.name,
            "count_post": countPostInTag(tag.idTag, today, fromDate)
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
        sentiment_by_date = tag('1266196', dateTo, dateFrom)
        total_pos = 0
        total_neg = 0
        for key, value in sentiment_by_date.items():
            total_pos = total_pos + value['pos']['count']
            total_neg = total_neg + value['neg']['count']

        result = {
            "total_pos": total_pos,
            "total_neg": total_neg,
            "sentiment_by_date": sentiment_by_date
        }

        return Response(json.dumps(result), mimetype='application/json')

api.add_resource(Vnexpress, '/vnexpress')
api.add_resource(Covid, '/vnexpress/covid')

if __name__ == '__main__':
    app.run()