import urllib.request, json 
from collections import namedtuple
import csv

# output = './crawlLazada.csv'
index = 0
# f_output = open(output, "a")
# f_output.write('\t'.join(['id', 'text']) + '\n')
prefix_id = 'id_'

urlData = "https://my.lazada.vn/pdp/review/getReviewList?itemId=464500892&pageSize=10000000&filter=0&sort=0&pageNo=1&fbclid=IwAR3mZ9NyeFyf38-o2VFEO_GoHwMaOe79_SKsG63gEB9AmO7V-Jwv-12z9MA"
with urllib.request.urlopen(urlData) as url:
    data = url.read().decode()
    data = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    listData = []
    
    for x in data.model.items:
        if x.reviewContent != None:
            listData.append(x.reviewContent)
    with open('crawlLazada.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'text'])
        for i in listData:
            # if i != ' ':
            id = prefix_id + '0' * (6 - len(str(index))) + str(index)
            index = index + 1
            print(i)
            writer.writerow([id, i])

index = 0
