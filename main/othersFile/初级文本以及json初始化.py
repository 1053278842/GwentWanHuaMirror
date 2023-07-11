import binascii
import json
import os

import pymem


# 写入卡片json源文件
def writeCardDataJsonBaseFile():
    # base = 0x27378C48014
    # count = 0x4add8*2

    # +0x14 string的偏移
    base = 0x27378C48014
    count = 0x4add8*2
    value = pm.read_bytes(base,count)
    result=""
    for item in value:
        result += str(hex(item))[2:].zfill(2).upper()

    with open('main/resources/config/text_utf16.txt', 'wb+') as fp:
        fp.write(binascii.unhexlify(result).decode('utf-16').encode('utf-16'))
    print("写入成功！")
    return 0

# CardData源文件转化为Json
def CardDataFileToJson():
    data = {}
    with open('main/resources/config/text_utf16.txt', 'r', encoding='utf-16') as inFile:
        # 第二种：每行分开读取
        count = 0
        id = ""
        description = ""
        name = ""
        tip = ""
        for line in inFile:
            data_line = line.strip("\n")  # 去除首尾换行符，并按空格划分
            # 只转换cardTemplate开头的
            if line[:5].isdigit():
                id = data_line[0:6]
                rowStatus = line[7:9]
                if rowStatus == "fl":
                    description = data_line[14:-1]
                if rowStatus == "na":
                    name = data_line[12:]
                if rowStatus == "to":
                    tip = data_line[15:]
                    data[str(id)] = {'name':name,"description":description,"tip":tip}
                # print(tip)
            # data2.append([int(i) for i in data_line])    
    with open("main/resources/config/card_json.json", 'w',encoding='utf8') as write_f:
        write_f.write(json.dumps(data, indent=4, ensure_ascii=False))




############################## ############################### ############################### ############################### #
# 获取程式模块基址
def get_baseAddress():
    global pm
    global baseAddress
    pm = pymem.Pymem("Gwent.exe")
    baseAddress = pymem.process.module_from_name(
        pm.process_handle,"GameAssembly.dll"
    ).lpBaseOfDll

def main():
    get_baseAddress()

if __name__ =='__main__':
    main()
    writeCardDataJsonBaseFile()
    CardDataFileToJson()
    # 还需要使用爬虫文件！爬取新卡各种类型的图
