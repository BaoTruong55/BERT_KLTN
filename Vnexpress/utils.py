import unidecode
import requests
import dateutil
import urllib.request, json 
from datetime import date, timedelta, datetime

PREFIX_ID = 'test_'

def getJsonFromURL(url):
    content = requests.get(url)
    dataJson = content.json()

    return dataJson

def datetimeToTimestamp(date):
    return int(dateutil.parser.parse(date, dayfirst=True).timestamp())

def timestampToDatetime(timestamp):
    return datetime.fromtimestamp(int(timestamp))

def unmarkTiengViet(str):
    return unidecode.unidecode(str)

def firstThingWriteCsv():
    with open(pathSaveCSV, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'text'])

def formatDate(date):
    return str(f'{date:%d/%m/%Y}')

def removeDuplicate(listInfoPost):
    idsPost = []
    infoPosts = []
    for infoPostCurrent in listInfoPost:
        if infoPostCurrent['id'] not in idsPost:
            infoPosts.append(infoPostCurrent)
            idsPost.append(infoPostCurrent['id'])    
    
    return infoPosts

def writeCSVFile(listData, total):
    with open(pathSaveCSV, 'a+', newline='') as file:
        writer = csv.writer(file)
        for num, data in enumerate(listData, start=total):
            id = "{prefix_id}{lenZero}{number}".format(
                prefix_id = PREFIX_ID,
                lenZero = '0' * (6 - len(str(num))),
                number = num
            )
            writer.writerow([id, data])

def getCategoryFromJson():
    with open('./category.json') as f:
        data = json.load(f)
        
    return data

def getCommentText(item):
    return item.comment

def getCommentId(item):
    return item.idComment