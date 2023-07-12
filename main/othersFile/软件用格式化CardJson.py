import os
import json
import requests
from lxml import etree



cardDict = open("main/resources/config/card_json.json", "r",encoding="utf-8")
card_list = json.loads(cardDict.read())
card_list_local = {}

for key, value in card_list.items():
    card_list_local[key] = {
        "name": value["name"],
        "factionId": int(value["factionId"]),
        "rarity": int(value["rarity"]),
        "provision": int(value["provision"]),
        "cardType": int(value["type"]),
        "power": int(value["power"]),
        "armor": int(value["armor"])
    }

with open("main/resources/config/card_json_local.json", 'w',encoding='utf8') as write_f:
        write_f.write(json.dumps(card_list_local, indent=4, ensure_ascii=False))