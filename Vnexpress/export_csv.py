from model_vnexpress import *
import csv
import html

PATH = "dataset/file-{index}.csv"


def first_thing_write_csv(path):
    with open(path, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'text', 'label'])


comments = Comment.objects()[:70000]


def format_text(text):
    text = "".join(text.split('<br/>'))
    text = ".".join(text.split(';'))
    return html.unescape(text)


count = len(comments)
for index in range(0, 70):
    first_thing_write_csv(PATH.format(index=index))
    with open(PATH.format(index=index), 'a+', newline='') as file:
        writer = csv.writer(file)
        for comment in comments[(index*1000): (index*1000)+1000]:
            writer.writerow(
                [comment.idComment, format_text(comment.comment), comment.label])
