
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


def format_date(date):
    return str(f'{date:%m/%d/%Y}')


def check_post(item):
    # print(len(list(item.posts)))
    return item.name.lower().find('chính trị') == -1


def top_topics(days):
    today = format_date(date.today())
    from_date = format_date(date.today() - timedelta(days=days))
    topics = Topic.objects(__raw__={"$where": "this.posts.length > 5"})
    topics = list(
        filter(lambda item: item.title.lower().find('chính trị') == -1, topics))

    total_topic = len(topics)
    topics_obj = []

    for index, topic in enumerate(topics, start=1):
        print("[{index}/{total}] - {title}".format(index=index,
                                                   total=total_topic, title=topic.title))
        topics_obj.append({
            "topic": topic,
            "posts": topic.get_posts_by_date(
                from_date,
                today
            )
        })

    topics_obj = list(filter(lambda item: len(
        item["posts"]) > 0, list(topics_obj)))
    topics_obj.sort(key=lambda item: len(item["posts"]), reverse=True)

    topics_result = list(map(lambda item: item["topic"], topics_obj[:30]))
    posts_result = sum(
        list(map(lambda item: item["posts"], topics_obj[:30])),
        []
    )

    return topics_result, posts_result, from_date, today


def top_tags(days):
    today = format_date(date.today())
    from_date = format_date(date.today() - timedelta(days=days))

    tags = Tag.objects(__raw__={"$where": "this.posts.length > 50"})
    print(len(tags))
    tags = list(
        filter(check_post, list(tags)))
    print(len(tags))
    total_tags = len(tags)
    tags_obj = []

    for index, tag in enumerate(tags, start=1):
        print("[{index}/{total}] - {name}".format(index=index,
                                                  total=total_tags, name=tag.name))
        tags_obj.append({
            "tag": tag,
            "posts": tag.get_posts_by_date(
                from_date,
                today
            )

        })

    tags_obj = list(filter(lambda item: len(
        item["posts"]) > 10, list(tags_obj)))
    tags_obj.sort(key=lambda item: len(item["posts"]), reverse=True)

    tags_result = list(map(lambda item: item["tag"], tags_obj[:30]))
    posts_result = sum(
        list(map(lambda item: item["posts"], tags_obj[:30])), [])

    return tags_result, posts_result, from_date, today


def top_tag_in_week():
    tags, posts, date_from, date_to = top_tags(7)
    top_tag = TopTag(
        unitTime="week",
        tags=tags,
        posts=posts,
        dateFrom=date_from,
        dateTo=date_to
    )
    top_tag.save()


def top_tag_in_month():
    tags, posts, date_from, date_to = top_tags(30)
    top_tag = TopTag(
        unitTime="month",
        tags=tags,
        posts=posts,
        dateFrom=date_from,
        dateTo=date_to
    )
    top_tag.save()


def top_topic_in_week():
    topics, posts, date_from, date_to = top_topics(7)
    top_topic = TopTopic(
        unitTime="week",
        topics=topics,
        posts=posts,
        dateFrom=date_from,
        dateTo=date_to
    )
    top_topic.save()


def top_topic_in_month():
    topics, posts, date_from, date_to = top_topics(30)
    top_topic = TopTopic(
        unitTime="month",
        topics=topics,
        posts=posts,
        dateFrom=date_from,
        dateTo=date_to
    )
    top_topic.save()


def save_top_tag():
    top_tag = TopTag.objects(
        unitTime='month'
    ).order_by('-created').first()
    tags = list(map(
        lambda item: {
            "id": item.idTag,
            "title": item.name,
                "url": item.url,
                "count_posts": len(
                    item.get_posts_by_date(
                        top_tag.dateFrom,
                        top_tag.dateTo
                    )
                ),
                }, list(top_tag.tags)
    ))
    with open('top_tag.json', 'w') as json_file:
        json.dump(tags, json_file)


def save_top_topic():
    top_topic = TopTopic.objects(
        unitTime='month'
    ).order_by('-created').first()
    topics = list(map(
        lambda item: {
            "id": item.idTopic,
            "title": "-".join(item.title.split('-')[:-1]),
            "description": item.description,
            "count_posts": len(
                item.get_posts_by_date(
                    top_topic.dateFrom,
                    top_topic.dateTo
                )
            ),
        }, list(top_topic.topics)
    ))
    with open('top_topic.json', 'w') as json_file:
        json.dump(topics, json_file)


if __name__ == '__main__':
    start = time.time()
    # top_topic_in_week()
    # top_topic_in_month()
    # top_tag_in_week()
    # top_tag_in_month()
    save_top_tag()
    save_top_topic()

    end = time.time()
    print(time.strftime("%H:%M:%S", time.gmtime(end - start)))
