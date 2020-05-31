import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests

index = 0
prefix_id = 'id_'
listData = []
listCategory = [
  "78",
  "77",
  "84",
  "163",
  "2365",
  "87",
  "13030",
  "160",
  "13033",
  "161",
  "9607",
  "162",
  "2429",
  "80",
  "2353",
  "9824",
  "9675",
  "12938",
  "12494",
  "13242",
  "17101",
  "18977",
  "16770",
  "91"
]
firstStrURL = "https://shopee.vn/api/v2/search_items/?by=sales&limit=100&match_id="
lastStrURL = "&newest=0&order=desc&page_type=search&rating_filter=1&version=2"
with open('crawlShopee.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['id', 'text'])
for m in listCategory:
    # ! Crawl item Id from catelogy
    URL = firstStrURL+ str(m) + lastStrURL
    with urllib.request.urlopen(URL) as urlCategory:
        if urlCategory != None:
            dataCategory = urlCategory.read().decode()
            dataCategory = json.loads(dataCategory, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    arrayPRD = []
    for prd in dataCategory.items:
        arrayPRD.append([prd.itemid, prd.shopid])
    print(str(len(arrayPRD))+" ["+str(m)+"]")
    for j in arrayPRD:
        print("[itemId: "+str(j[0])+"] [shopId: "+str(j[1])+"]")
        urlData = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid="+str(j[0])+"&limit=10000&offset=0&shopid="+str(j[1])+"&type=0"
        with urllib.request.urlopen(urlData) as url:
            if url != None:
                data = url.read().decode()
                data = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                newUrl = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid="+str(j[0])+"&limit="+str(data.data.item_rating_summary.rating_total)+"&offset=0&shopid="+str(j[1])+"&type=0"
                listData = []
                with urllib.request.urlopen(newUrl) as url2:
                    if url2 != None:
                        newData = url2.read().decode()
                        newData = json.loads(newData, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                        # print(newData)
                        if newData.data.ratings != None:
                            for x in newData.data.ratings:
                                if x.comment != None and x.comment != "":
                                    listData.append(x.comment)
                with open('crawlShopee.csv', 'a+', newline='') as file:
                    writer = csv.writer(file)
                    for i in listData:
                        id = prefix_id + '0' * (6 - len(str(index))) + str(index)
                        index = index + 1
                        writer.writerow([id, i])
    print("=====================================================================================================")
