import os
import json
import requests
from lxml import etree

cardDict = open("main/resources/config/card_json.json", "r",encoding="utf-16")
card_list = json.loads(cardDict.read())

fileNameIdList = []
for fileName in os.listdir("main/resources/images/GwentImg原图"):
    fileNameIdList.append(fileName[:6])

for keys in card_list:
    

    # check 
    if not keys.isdigit():
        print("检测到key不是纯数字作为唯一ID",keys)
        continue
    
    if keys < start_id_str:
        print(keys,keys < start_id_str)
        continue

    # 已经有该图片
    if keys in fileNameIdList:
        continue
        
numbers = [202705]
download_dir = "downloaded_images"


for number in numbers:
    # 构建URL
    url = f"https://gwent.one/cn/card/{number}/11.6.0"
    
    # 发送请求并获取响应内容
    response = requests.get(url)
    
    if response.status_code == 200:
        html = response.text
        
        # 解析HTML
        tree = etree.HTML(html)
        
        # 获取下载链接
        download_links = tree.xpath('//div[@class="dl-link"]/a[last()]/@href')
        
        if download_links:
            # 下载文件
            for link in download_links:
                # 提取目录名称
                directory = link.split("/")[-2]
                if directory == "low":
                    # 创建目录
                    os.makedirs(f"{download_dir}/{directory}", exist_ok=True)
                    
                    filename = f"{download_dir}/{directory}/{number}.jpg"  # 使用数字作为文件名
                    response = requests.get(link)
                    
                    # 将文件保存到本地
                    with open(filename, 'wb') as file:
                        file.write(response.content)
                    
                    print(f"已下载文件: {filename}")
        else:
            print(f"未找到下载链接 for {number}")
    elif response.status_code == 404:
        print(f"页面不存在 for {number}")
    else:
        print(f"请求失败 for {number}，状态码: {response.status_code}")
