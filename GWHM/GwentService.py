import MainController as mc
import CardService as cs
from threading import Thread
from FileTool import *
from GwentEnum import *

def start():
    mc.main()

def get_my_deck_cards(location,playerId):
    cs.main()
    return cs.get_my_deck_cards(location,playerId)

def get_my_all_cards(playerId):
    cs.main()
    return cs.get_my_all_cards(playerId)

def get_deck_remove_cards(curr_memo_cards,deck_component_card_id_list,scale_factor):
    # 实例化图片池，存储到temp中
    create_deck_preview_temp_file(curr_memo_cards,scale_factor)
    # 存放本次扫描结果内内存中的 card_id 列表
    curr_memory_card_id_list= []
    for card_instance_id in curr_memo_cards:
        if curr_memo_cards[card_instance_id]["Location"] == hex(Location.DECK.value):
            curr_memory_card_id_list.append(card_instance_id)
    # 刚刚减少的对象 在A里不在B里的对象
    remove_card_id_list = []
    for i in deck_component_card_id_list:
        if i not in curr_memory_card_id_list:
            remove_card_id_list.append(i)
    return remove_card_id_list

def get_deck_add_cards(curr_memo_cards,deck_component_card_id_list,scale_factor):
    # 实例化图片池，存储到temp中
    create_deck_preview_temp_file(curr_memo_cards,scale_factor)
    # 存放本次扫描结果内内存中的 card_id 列表
    # 过滤出指定Location的卡牌
    curr_memory_card_id_list= []
    for card_instance_id in curr_memo_cards:
        if curr_memo_cards[card_instance_id]["Location"] == hex(Location.DECK.value):
            curr_memory_card_id_list.append(card_instance_id)
    # 增加的对象     在B里不在A的对象
    add_card_id_list = []
    for i in curr_memory_card_id_list:
        if i not in deck_component_card_id_list:
            add_card_id_list.append(i)
    return add_card_id_list

