import urllib.request, json 
from collections import namedtuple
import csv
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests

index = 0
prefix_id = 'id_'
listCatelogy = [
  "https://www.lazada.vn/laptop/",
  "https://www.lazada.vn/may-tinh-de-ban-va-phu-kien/",
  "https://www.lazada.vn/am-thanh/",
  "https://www.lazada.vn/camera-giam-sat-2/",
  "https://www.lazada.vn/may-anh-may-quay-phim/",
  "https://www.lazada.vn/may-quay-phim/",
  "https://www.lazada.vn/man-hinh-may-in/",
  "https://www.lazada.vn/dong-ho-thong-minh/",
  "https://www.lazada.vn/dieu-khien-choi-game/",
  "https://www.lazada.vn/phu-kien-dien-thoai-may-tinh-bang/",
  "https://www.lazada.vn/thiet-bi-thong-minh/",
  "https://www.lazada.vn/thiet-bi-so/",
  "https://www.lazada.vn/phu-kien-may-anh-may-quay-phim/",
  "https://www.lazada.vn/phu-kien-may-bay-camera/",
  "https://www.lazada.vn/thiet-bi-luu-tru-2/",
  "https://www.lazada.vn/phu-kien-may-vi-tinh/",
  "https://www.lazada.vn/linh-kien-may-tinh/",
  "https://www.lazada.vn/phu-kien-ong-kinh/",
  "https://www.lazada.vn/thiet-bi-mang/",
  "https://www.lazada.vn/phu-kien-may-choi-game/",
  "https://www.lazada.vn/tv-video-am-thanh-thiet-bi-deo-cong-nghe/",
  "https://www.lazada.vn/do-gia-dung-nho/",
  "https://www.lazada.vn/do-gia-dung-lon/",
  "https://www.lazada.vn/cham-soc-da-mat/",
  "https://www.lazada.vn/trang-diem/",
  "https://www.lazada.vn/dung-cu-cham-soc-sac-dep/",
  "https://www.lazada.vn/san-pham-tam-cham-soc-co-the/",
  "https://www.lazada.vn/san-pham-cham-soc-toc/",
  "https://www.lazada.vn/cham-soc-ca-nhan/",
  "https://www.lazada.vn/cham-soc-cho-nam-gioi/",
  "https://www.lazada.vn/nuoc-hoa/",
  "https://www.lazada.vn/thuc-pham-bo-sung/",
  "https://www.lazada.vn/thuc-pham-cho-sac-dep/",
  "https://www.lazada.vn/ho-tro-tinh-duc/",
  "https://www.lazada.vn/thiet-bi-y-te/",
  "https://www.lazada.vn/ta-dung-cu-ve-sinh/",
  "https://www.lazada.vn/sua-cong-thuc-bot-an-dam/",
  "https://www.lazada.vn/quan-ao-phu-kien-cho-be/",
  "https://www.lazada.vn/do-dung-bu-sua-an-dam/",
  "https://www.lazada.vn/xe-ghe-em-be/",
  "https://www.lazada.vn/cham-soc-tre-so-sinh-tre-nho/",
  "https://www.lazada.vn/tam-cham-soc-co-the-tre-so-sinh/",
  "https://www.lazada.vn/do-choi-tro-choi/",
  "https://www.lazada.vn/xe-mo-hinh-tro-choi-dieu-khien-tu-xa/",
  "https://www.lazada.vn/the-thao-tro-choi-ngoai-troi/",
  "https://www.lazada.vn/do-choi-cho-tre-so-sinh-chap-chung/",
  "https://www.lazada.vn/do-choi-giao-duc-tre-em/",
  "https://www.lazada.vn/bach-hoa-online-sua-uht-tiet-trung-sua-bot/",
  "https://www.lazada.vn/cac-loai-do-uong/",
  "https://www.lazada.vn/shop-Thuc-pham-tu-sua-do-lanh/",
  "https://www.lazada.vn/shop-do-hop/",
  "https://www.lazada.vn/shop-So-co-la-Snack-Keo/",
  "https://www.lazada.vn/shop-Nguyen-lieu-nau-an-lam-banh/",
  "https://www.lazada.vn/bach-hoa-online-chat-lau-chui-nha-cua/",
  "https://www.lazada.vn/bach-hoa-online-muong-nia-nhua/",
  "https://www.lazada.vn/cham-soc-nha-cua/",
  "https://www.lazada.vn/phu-kien-cho-thu-cung/",
  "https://www.lazada.vn/thuc-an-thu-cung/",
  "https://www.lazada.vn/do-dung-bep-phong-an/",
  "https://www.lazada.vn/tan-trang-nha-cua/",
  "https://www.lazada.vn/dung-cu-dien/",
  "https://www.lazada.vn/dung-cu-cam-tay-da-nang/",
  "https://www.lazada.vn/do-dung-phong-ngu-gia-dinh/",
  "https://www.lazada.vn/do-dung-phu-kien-phong-tam/",
  "https://www.lazada.vn/cac-loai-den/",
  "https://www.lazada.vn/san-pham-trang-tri-nha-cua/",
  "https://www.lazada.vn/san-pham-noi-that/",
  "https://www.lazada.vn/van-phong-pham-va-nghe-thu-cong/",
  "https://www.lazada.vn/truyen-thong-am-nhac-sach/",
  "https://www.lazada.vn/dung-cu-ve-sinh-2/",
  "https://www.lazada.vn/jeans-nu/",
  "https://www.lazada.vn/ao-nu/",
  "https://www.lazada.vn/do-ngu-noi-y/",
  "https://www.lazada.vn/phu-kien-cho-nu/",
  "https://www.lazada.vn/giay-nu-thoi-trang/",
  "https://www.lazada.vn/trang-phuc-cua-be-gai/",
  "https://www.lazada.vn/thoi-trang-giay-danh-cho-be-gai/",
  "https://www.lazada.vn/trang-phuc-nam/",
  "https://www.lazada.vn/giay-nam-thoi-trang/",
  "https://www.lazada.vn/do-lot-nam/",
  "https://www.lazada.vn/phu-kien-thoi-trang-nam/",
  "https://www.lazada.vn/trang-phuc-cua-be-trai/",
  "https://www.lazada.vn/thoi-trang-giay-cho-be-trai/",
  "https://www.lazada.vn/dong-ho-nu-thoi-trang/",
  "https://www.lazada.vn/trang-suc-nu/",
  "https://www.lazada.vn/kinh-mat/",
  "https://www.lazada.vn/kinh-mat-2/",
  "https://www.lazada.vn/tui-cho-nu/",
  "https://www.lazada.vn/dong-ho-nam-gioi/",
  "https://www.lazada.vn/trang-suc-nam/",
  "https://www.lazada.vn/tui-nam/",
  "https://www.lazada.vn/vali-ba-lo-tui-du-lich-2/",
  "https://www.lazada.vn/tui-danh-cho-tre-em/",
  "https://www.lazada.vn/do-the-thao-nam/",
  "https://www.lazada.vn/quan-ao-the-thao-cho-nam/",
  "https://www.lazada.vn/do-the-thao-nu/",
  "https://www.lazada.vn/quan-ao-the-thao-cho-nu/",
  "https://www.lazada.vn/vali-ba-lo-tui-du-lich-2/",
  "https://www.lazada.vn/hoat-dong-da-ngoai/",
  "https://www.lazada.vn/dung-cu-de-tap-the-hinh/",
  "https://www.lazada.vn/cac-mon-the-thao-vot/",
  "https://www.lazada.vn/cac-mon-tap-luyen-doi-khang/",
  "https://www.lazada.vn/dam-boc-vo-thuat-danh-mma/",
  "https://www.lazada.vn/cac-mon-the-thao-duoi-nuoc/",
  "https://www.lazada.vn/phu-kien-the-thao/",
  "https://www.lazada.vn/xe-mo-to-xe-tay-ga/",
  "https://www.lazada.vn/cham-soc-o-to/",
  "https://www.lazada.vn/phu-kien-trong-o-to-xe-may/",
  "https://www.lazada.vn/phu-kien-ngoai-o-to-xe-may/",
  "https://www.lazada.vn/bo-phan-phu-tung-thay-the-cho-xe/",
  "https://www.lazada.vn/hang-dien-tu-2/",
  "https://www.lazada.vn/dau-nhot-o-to-xe-may/",
  "https://www.lazada.vn/bo-phan-mo-to-phu-tung-thay-the-cho-mo-to/",
  "https://www.lazada.vn/do-bao-ho-mo-to/",
  "https://www.lazada.vn/phu-kien-gan-ngoai-mo-to/",
  "https://www.lazada.vn/dau-nhot-mo-to/",
  "https://www.lazada.vn/banh-xe-lop-xe-may/",
  "https://www.lazada.vn/dien-thoai-di-dong/",
  "https://www.lazada.vn/may-tinh-bang/",
  "https://www.lazada.vn/man-hinh-vi-tinh/",
  "https://www.lazada.vn/phu-kien-cho-tv/",
  "https://www.lazada.vn/dam-nu/",
  "https://www.lazada.vn/jumpsuit-nu/",
  "https://www.lazada.vn/invisible-unisex-fashion-4/",
  "https://www.lazada.vn/ba-lo-nu/",
  "https://www.lazada.vn/tui-deo-cheo-cho-nam/"
]

with open('crawlLazada.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'text'])
for k in listCatelogy:
    # ! Crawl item Id from catelogy
    URL = k
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser') 
    rows = soup.find_all('script')         # Print all occurrences
    tam = rows[3].get_text().split("=",1)
    convertStr = tam[1].replace("from", "a")
    convertStr = convertStr.replace("font-size", "a")
    # convertStr = convertStr.replace("18", "a")
    jsonData = json.loads(convertStr, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    arrayID = []
    for i in jsonData.mods.listItems:
        arrayID.append(i.itemId)
    # print(arrayID)
    print("======================================="+k+"=======================================")
    for j in arrayID:
        urlData = "https://my.lazada.vn/pdp/review/getReviewList?itemId="+j+"&pageSize=10000000&filter=0&sort=0&pageNo=1"
        listData = []
        print(urlData)
        with urllib.request.urlopen(urlData) as url:
            data = url.read().decode()
            data = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            if data.model.items != None:
                for x in data.model.items:
                    if x.reviewContent != None:
                        listData.append(x.reviewContent)
        with open('crawlLazada.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            for i in listData:
                id = prefix_id + '0' * (6 - len(str(index))) + str(index)
                index = index + 1
                # print(i)
                writer.writerow([id, i])
