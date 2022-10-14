from threading import Thread

import MainController as mc
import services.CardService as cs
from enums.GwentEnum import *
from tools.decorators import *
from tools.FileTool import *


def get_my_all_cards(cardDeckInfo):
    return cs.get_my_all_cards(cardDeckInfo)

# 获取当前信息并按照BattleInfo对象返回
def getCurrBattleInfo():
    return cs.getCurrBattleInfo()


def get_deck_remove_cards(curr_memo_cards,deck_component_card_id_list,cardTypeInfo):
    # 存放本次扫描结果内内存中的 card_id 列表
    curr_memory_card_id_list= []
    for card_instance_id in curr_memo_cards:
        if (curr_memo_cards[card_instance_id]["Location"] == hex(cardTypeInfo.location.value) or
         curr_memo_cards[card_instance_id]["Location"] == hex(cardTypeInfo.secLocation.value)):
            curr_memory_card_id_list.append(card_instance_id)
    if cardTypeInfo.isMain:
        curr_memory_card_id_list = curr_memo_cards
    # 刚刚减少的对象 在A里不在B里的对象
    remove_card_id_list = []
    for i in deck_component_card_id_list:
        if i not in curr_memory_card_id_list:
            remove_card_id_list.append(i)
    return remove_card_id_list

def get_deck_add_cards(curr_memo_cards,deck_component_card_id_list,cardTypeInfo):
    # 存放本次扫描结果内内存中的 card_id 列表
    # 过滤出指定Location的卡牌
    curr_memory_card_id_list= []
    for card_instance_id in curr_memo_cards:
        if (curr_memo_cards[card_instance_id]["Location"] == hex(cardTypeInfo.location.value) or
         curr_memo_cards[card_instance_id]["Location"] == hex(cardTypeInfo.secLocation.value)):
            curr_memory_card_id_list.append(card_instance_id)
    if cardTypeInfo.isMain:
        curr_memory_card_id_list = curr_memo_cards
    # 增加的对象     在B里不在A的对象
    add_card_id_list = []
    for i in curr_memory_card_id_list:
        if i not in deck_component_card_id_list:
            add_card_id_list.append(i)
    return add_card_id_list

