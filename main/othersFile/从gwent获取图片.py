import os
import json
import requests
from lxml import etree

numbers = []
fileNameIdList = []
# 取消过滤'衍生卡'请使用希里ID:112101
start_id_str = "202201"
download_dir = "downloaded_images"
# Gwent收录版本号
version = '11.6.0'
for fileName in os.listdir("downloaded_images/low"):
    fileNameIdList.append(fileName[:6])
    print(fileName[:6])

cardDict = open("main/resources/config/card_json.json", "r",encoding="utf-8")
card_list = json.loads(cardDict.read())

isStart = False
for keys in card_list:
    if keys == start_id_str:
        isStart = True
    if isStart == True:
        # check 
        if not keys.isdigit():
            print("检测到key不是纯数字作为唯一ID",keys)
        elif keys in fileNameIdList:
            print("检测到图片已存在",keys)
        else:
            numbers.append(keys) 

def download_image(number):
    # 构建URL
    url = f"https://gwent.one/cn/card/{number}/{version}"
    print("当前请求:",url)
    # 发送请求并获取响应内容
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        # 请求异常，进行重试
        print(f"请求发生异常，进行重试 for {number}: {str(e)}",url)
        download_image(number)
        return
    
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
                    try:
                        response = requests.get(link)
                    except requests.RequestException as e:
                        # 请求异常，进行重试
                        print(f"请求发生异常，进行重试 for {number}: {str(e)}")
                        download_image(number)
                        return
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

print("开始下载!")
# 下载图片
for number in numbers:
    download_image(number)
