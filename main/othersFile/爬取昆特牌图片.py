import json
from time import sleep
from urllib import request
from selenium import webdriver
import requests 
import os
from multiprocessing import Process

def process():
    wait_time = 180
    runtime = 300

    # 1.打开浏览器，输入网址
    cardDict = open("card_json.json", "r",encoding="utf-16")
    card_list = json.loads(cardDict.read())
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
    chrome_options.add_argument('--ignore-certificate-errors')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    # browser.maximize_window() # 浏览器最大化
    # browser.get('https://www.playgwent.com/en/decks/builder/card/details/202140')
    browser.implicitly_wait(30) # 加入隐式等待，防止崩溃
    start_id_str = "202156"
    # 202093 - 202097 无图片
    # 202123 sd
    for keys in card_list:
        

        # check 
        if not keys.isdigit():
            print("检测到key不是纯数字作为唯一ID",keys)
            continue

        if keys < start_id_str:
            print(keys,keys < start_id_str)
            continue
        
        print("图片爬取已从ID:"+keys+"处开始!")

        url_str = 'https://www.playgwent.com/en/decks/builder/card/details/'
        url_str += keys
        browser.get(url_str)
        browser.implicitly_wait(30) # 加入隐式等待，防止崩溃

        img_url = get_img_url(browser)
        if img_url != "" and img_url != None:
            writeImg(img_url,keys)
        else:
            continue

        # browser.refresh()

def get_img_url(browser):
    bg_url = ""
    bg_img_div=browser.find_elements_by_xpath('//div[@class="CardDetailsImage__CardDetailsImageContainer-sc-1m81vda-10 ijFgOK"]/div')   
    if len(bg_img_div) > 0:
        bg_url = bg_img_div[0].value_of_css_property('background-image')
        temp_str_array = bg_url.split("),")
        if len(temp_str_array) > 0:
            bg_url = temp_str_array[0].lstrip('url("').rstrip('"),')
            return bg_url

def writeImg(url,fileName):
    path="./GwentImg/"
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    headers = { 'Connection': 'close',}

    # sleep(1)
    r=requests.get(url,headers=headers)
    try:
        with open(path+fileName+".jpg",'wb') as f:
            f.write(r.content)
            f.close()
    except IOError:
        print("IO异常")

if __name__=='__main__':

    #OS创建文件夹
    img_file_path="./GwentImg"
    if not os.path.exists(img_file_path):
        os.makedirs(img_file_path)


    process_list=[]
    for i in range(0,1):
        temp_p=Process(target=process,args=())
        temp_p.start()
        process_list.append(temp_p)
    
    for p in process_list:
        p.join()
    
    print("测试完成!")
