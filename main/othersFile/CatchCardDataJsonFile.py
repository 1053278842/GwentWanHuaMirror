import binascii
import json
import os
import xml.etree.ElementTree as ET

import mysql.connector
import pymem


# 写入卡片json源文件
def writeCardDataJsonBaseFile():

    # +0x14 string的偏移
    base = 0x1FD313BF014    # 第一行+0x14
    count = 0x16a3e8*2  # 第二行长度*2 
    value = pm.read_bytes(base,count)
    result=""
    for item in value:
        result += str(hex(item))[2:].zfill(2).upper()

    with open('main/resources/config/cardData_utf16.xml', 'wb+') as fp:
        fp.write(binascii.unhexlify(result).decode('utf-16').encode('utf-16'))
    print("写入成功！")
    return 0

# CardData源文件转化为Json
def CardDataFileToJson():
    tree = ET.parse('main/resources/config/cardData_utf16.xml')
    root = tree.getroot()
    with open('main/resources/config/card_json.json', 'r',encoding='utf-8') as f:
        data = json.load(f)

    driverCardData ={}

    for key, value in data.items():
        for template in root.findall('Template'):
            if template.attrib['Id'] == key:
                for element in template:
                    value['debugName'] = template.attrib['DebugName']
                    value['availability'] = template.attrib['Availability']
                    if element.tag == 'Rarity':
                        value['rarity'] = element.text
                    elif element.tag == 'Kind':
                        value['kind'] = element.text
                    elif element.tag == 'Type':
                        value['type'] = element.text
                    elif element.tag == 'SecondaryFactionId':
                        value['secondaryFactionId'] = element.text
                    elif element.tag == 'Tier':
                        value['tier'] = element.text
                    elif element.tag == 'Power':
                        value['power'] = element.text
                    elif element.tag == 'Provision':
                        value['provision'] = element.text
                    elif element.tag == 'InitialTimer':
                        value['initialTimer'] = element.text
                    elif element.tag == 'FactionId':
                        value['factionId'] = element.text
                    elif element.tag == 'Armor':
                        value['armor'] = element.text
                    # 衍生卡
                    if template.attrib['Availability'] == "0":
                        driverCardData[key] = value

    with open('main/resources/config/card_json.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    with open('main/resources/config/driverCard_json.json', 'w', encoding='utf-8') as f:
        json.dump(driverCardData, f, indent=4, ensure_ascii=False)

def saveToMySql():


    # 建立与MySQL数据库的连接
    cnx = mysql.connector.connect(
        user='root',
        password='LiuLong123123+',
        host='117.50.175.251',
        port=3306,
        database='GwentMirror'
    )

    # 创建游标对象
    cursor = cnx.cursor()


    # 插入数据到card_data表格
    insert_data_query = """
    INSERT INTO card (
        cid, name, description, tip, availability, rarity, 
        factionId, secondaryFactionId, tier, type, power, provision,
        initialTimer, armor
    ) VALUES (
        %(cid)s, %(name)s, %(description)s, %(tip)s, %(availability)s,
        %(rarity)s, %(factionId)s, %(secondaryFactionId)s, %(tier)s,
        %(type)s, %(power)s, %(provision)s, %(initialTimer)s, %(armor)s
    )
    """

    with open('main/resources/config/card_json.json', 'r',encoding='utf-8') as f:
        data = json.load(f)

        for card_id, card_data in data.items():
            cursor.execute(insert_data_query, {
                "cid": int(card_id),
                "name": card_data["name"],
                "description": card_data["description"],
                "tip": card_data["tip"],
                "availability": int(card_data["availability"]),
                "rarity": int(card_data["rarity"]),
                "factionId": int(card_data["factionId"]),
                "secondaryFactionId": int(card_data["secondaryFactionId"]),
                "tier": int(card_data["tier"]),
                "type": int(card_data["type"]),
                "power": int(card_data["power"]),
                "provision": int(card_data["provision"]),
                "initialTimer": int(card_data["initialTimer"]),
                "armor": int(card_data["armor"])
            })

    # 提交更改到数据库
    cnx.commit()

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()



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
    # main()
    # writeCardDataJsonBaseFile()
    # CardDataFileToJson()
    saveToMySql()
    # 还需要使用爬虫文件！爬取新卡各种类型的图
