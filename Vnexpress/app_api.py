
from flask import Flask, request, Response
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
# from infer_predict import *
from crawl_post import *
from crawl_vnexpress import get_info_post, get_comments
from model_vnexpress import *
from flask_cors import CORS, cross_origin
from datetime import datetime, date, timedelta
from dateutil import parser
import time
import os

# TODO ==== Main ===============================================================
application = Flask(__name__)
CORS(application)
api = Api(application)

SUB_URL = os.environ.get("SUB_URL", '/vnexpress')


def format_date(date):
    return str(f'{date:%m/%d/%Y}')


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


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


def sentiment_in_posts(posts):
    comments = sum(list(map(Post.get_comments, posts)), [])
    comments_pos = list(filter(Comment.is_label_pos, list(comments)))
    comments_neg = list(filter(Comment.is_label_neg, list(comments)))

    return {
        "comments_pos": comments_pos,
        "comments_neg": comments_neg
    }


def classify_comment_by_date(posts, date_from, date_to):
    classify_post = {}
    for single_date in daterange(parser.parse(date_from), parser.parse(date_to)):
        classify_post[single_date.strftime('%m/%d/%Y')] = []

    for post in posts:
        classify_post[post.publishTime.strftime('%m/%d/%Y')].append(post)

    list_post = list(
        map(
            lambda item: {
                "title": item.title,
                "url": item.url.split('#')[0],
                "thumbnailUrl": item.thumbnailUrl,
                "description": item.description,
                "count_comment": len(item.comments)
            },
            list(posts)
        )
    )

    list_post.sort(key=lambda item: item['count_comment'], reverse=True)

    classify_comment = {}
    for key, value_posts in classify_post.items():
        comments = sum(list(map(Post.get_comments, value_posts)), [])

        comments_neg = list(filter(Comment.is_label_neg, comments))
        comments_pos = list(filter(Comment.is_label_pos, comments))
        # comments_text_neg = list(map(GET_COMMENT, comments_neg))
        # comments_text_pos = list(map(GET_COMMENT, comments_pos))

        posts_map = list(
            map(
                lambda item: {
                    "title": item.title,
                    "url": item.url.split('#')[0],
                    "thumbnailUrl": item.thumbnailUrl,
                    "description": item.description,
                    "count_comment": len(item.comments)
                },
                list(value_posts)
            )
        )

        classify_comment[key] = {
            "count_post": len(posts_map),
            "posts": posts_map,
            "pos": len(comments_pos),
            "neg": len(comments_neg),
        }

    classify_comment_format = []
    for key in classify_comment:
        classify_comment_format.append({
            "date": key,
            "data": classify_comment[key]
        })

    return classify_comment_format, list_post[:20]


def tag(id, date_from, date_to):
    posts_in_tag = Tag.objects.get(idTag=id).posts
    posts = filter_posts_by_date(posts_in_tag, date_from, date_to)
    return classify_comment_by_date(posts, date_from, date_to)


def category(id, date_from, date_to):
    posts_in_category = Category.objects.get(idCategory=id).posts
    posts = filter_posts_by_date(posts_in_category, date_from, date_to)
    return classify_comment_by_date(posts, date_from, date_to)


def topic(id, date_from, date_to):
    posts_in_topic = Topic.objects.get(idTopic=id).posts
    posts = filter_posts_by_date(posts_in_topic, date_from, date_to)
    return classify_comment_by_date(posts, date_from, date_to)


def posts_in_topic(id, date_from, date_to):
    posts_in_topic = Topic.objects.get(idTopic=id).posts
    return Topic.get_posts_by_date(posts_in_topic, date_from, date_to)


def posts_in_tag(id, date_from, date_to):
    posts_in_tag = Tag.objects.get(idTag=id).posts
    return Tag.get_posts_by_date(posts_in_tag, date_from, date_to)


class Vnexpress(Resource):
    def get(self):
        url = request.args.get('url')
        id_post, title, description, thumbnail_url = get_info_post_crawl(url)
        comments = get_comments_crawl(id_post)

        if len(comments) == 0:
            return {"error": "The article has no comments"}

        df = normalize_data(comments)
        df_result = predict_data(df)
        df_output = DataFrame(df_result, columns=['data_text', 'label'])
        df_negatives = df_output[df_output['label'] == 0]
        df_possitives = df_output[df_output['label'] == 1]

        output = {
            "title": title,
            "description": description,
            "thumbnailUrl": thumbnail_url,
            "pos": len(df_possitives.index),
            "neg": len(df_negatives.index),
            "commentPos": df_possitives.to_dict("records"),
            "commentNeg": df_negatives.to_dict("records")
        }

        return Response(
            json.dumps(output),
            mimetype='application/json'
        )


class VnexpressInDatabase(Resource):
    def get(self):
        url = request.args.get('url')
        id_post, title, description, thumbnail_url = get_info_post_crawl(url)
        post = Post.objects(idPost=id_post).first()

        if post != None:
            sentiment = sentiment_in_posts([post])

        if post == None or (len(sentiment['comments_pos']) == 0 and len(sentiment['comments_neg']) == 0):
            post, tags, topic = get_info_post(url, id_post)
            if tags != None:
                for tag in tags:
                    if post not in tag.posts:
                        tag.posts.append(post)
                    tag.save()

            if topic != None:
                if post not in topic.posts:
                    topic.posts.append(post)
                topic.save()

            comments = get_comments(id_post)

            for index, comment in enumerate(comments, start=1):
                if comment not in post.comments:
                    post.comments.append(comment)
                post.save()

            return {"error": "The article not predict comments"}

        output = {
            "title": title,
            "description": description,
            "thumbnailUrl": thumbnail_url,
            "pos": len(sentiment['comments_pos']),
            "neg": len(sentiment['comments_neg']),
            "commentPos": list(map(
                lambda item:
                {
                    "data_text": item.comment,
                    "label": item.label
                },
                list(sentiment['comments_pos'])
            )),
            "commentNeg": list(map(
                lambda item:
                {
                    "data_text": item.comment,
                    "label": item.label
                },
                list(sentiment['comments_neg'])
            )),
        }

        return Response(
            json.dumps(output),
            mimetype='application/json'
        )


class Covid(Resource):
    def get(self):
        date_to = request.args.get('dateto')
        date_from = request.args.get('datefrom')
        sentiment_by_date, top_post = tag('1266196', date_from, date_to)
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
        return Response(
            json.dumps(result),
            mimetype='application/json'
        )


class TopTopics(Resource):
    def get(self):
        # top_topic = TopTopic.objects(
        #     unitTime='month'
        # ).order_by('-created').first()
        # topics = list(map(
        #     lambda item: {
        #         "id": item.idTopic,
        #         "title": "-".join(item.title.split('-')[:-1]),
        #         "description": item.description,
        #         "count_posts": len(
        #             item.get_posts_by_date(
        #                 top_topic.dateFrom,
        #                 top_topic.dateTo
        #             )
        #         ),
        #     }, list(top_topic.topics)
        # ))

        with open('top_topic.json') as json_file:
            tags = json.load(json_file)
        return Response(
            json.dumps(topics),
            mimetype='application/json'
        )


class TopTags(Resource):
    def get(self):
        # top_tag = TopTag.objects(
        #     unitTime='month'
        # ).order_by('-created').first()
        # tags = list(map(
        #     lambda item: {
        #         "id": item.idTag,
        #         "title": item.name,
        #         "url": item.url,
        #         "count_posts": len(
        #             item.get_posts_by_date(
        #                 top_tag.dateFrom,
        #                 top_tag.dateTo
        #             )
        #         ),
        #     }, list(top_tag.tags)
        # ))

        with open('top_tag.json') as json_file:
            tags = json.load(json_file)
        return Response(
            json.dumps(tags),
            mimetype='application/json'
        )


class Categories(Resource):
    def get(self):
        category = Category.objects()

        if category == None:
            return Response(
                json.dumps(
                    {"error": "current can not get category!"}
                ),
                mimetype='application/json'
            )

        listCategory = list(map(
            lambda item: {
                "idCategory": item.idCategory,
                "title": item.title,
                "description": item.description
            },
            category
        ))
        return Response(
            json.dumps(listCategory),
            mimetype='application/json'
        )


class CategorySentiment(Resource):
    def get(self):
        idCategory = request.args.get('idcategory')
        date_to = request.args.get('dateto')
        date_from = request.args.get('datefrom')
        sentiment_by_date, top_post = category(idCategory, date_from, date_to)
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
        return Response(
            json.dumps(result),
            mimetype='application/json'
        )


class TagSentiment(Resource):
    def get(self):
        id_tag = request.args.get('idtag')
        top_tag = TopTag.objects(
            unitTime='month'
        ).order_by('-created').first()

        if top_tag == None:
            return Response(
                json.dumps(
                    {"error": "current can not get top tag!"}
                ),
                mimetype='application/json'
            )

        if request.args.get('dateto') != None:
            date_to = request.args.get('dateto')
        else:
            date_to = format_date(top_tag.dateTo)

        if request.args.get('datefrom') != None:
            date_from = request.args.get('datefrom')
        else:
            date_from = format_date(top_tag.dateFrom)

        sentiment_by_date, top_post = tag(id_tag, date_from, date_to)
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
        return Response(
            json.dumps(result),
            mimetype='application/json'
        )


class TopicSentiment(Resource):
    def get(self):
        id_topic = request.args.get('idtopic')

        top_topic = TopTopic.objects(
            unitTime='month'
        ).order_by('-created').first()

        if top_topic == None:
            return Response(
                json.dumps(
                    {"error": "current can not get top topic!"}
                ),
                mimetype='application/json'
            )

        if request.args.get('dateto') != None:
            date_to = request.args.get('dateto')
        else:
            date_to = format_date(top_topic.dateTo)

        if request.args.get('datefrom') != None:
            date_from = request.args.get('datefrom')
        else:
            date_from = format_date(top_topic.dateFrom)

        sentiment_by_date, top_post = topic(id_topic, date_from, date_to)
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
        return Response(
            json.dumps(result),
            mimetype='application/json'
        )


api.add_resource(Vnexpress, SUB_URL)
api.add_resource(VnexpressInDatabase, SUB_URL + '/post')
api.add_resource(Covid, SUB_URL + '/covid')
api.add_resource(TopTags, SUB_URL + '/toptag')
api.add_resource(TopTopics, SUB_URL + '/toptopic')
api.add_resource(Categories, SUB_URL + '/categories')
api.add_resource(TagSentiment, SUB_URL + '/tagsentiment')
api.add_resource(TopicSentiment, SUB_URL + '/topicsentiment')
api.add_resource(CategorySentiment, SUB_URL + '/categorysentiment')

if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(
        host='0.0.0.0',
        port=ENVIRONMENT_PORT,
        debug=ENVIRONMENT_DEBUG
    )
