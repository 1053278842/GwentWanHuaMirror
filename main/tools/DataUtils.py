import datetime
import time


# [2001501,400153] => hash
# 卡组转哈希值，无视元素顺序
def transListCtIdToHash(decks):
    return hash(frozenset(decks))

def shortenText(text,length):
    if len(text) >= length:
        return text[:length-3] + "..."
    else :
        return text

def transStrTimeToStamp(time,format):
    # if format == "yyyy-MM-dd HH:mm:ss":
    return datetime.datetime.strptime(time,format)

def transStrTimeToTimestamp(format_time,format):
    # if format == "yyyy-MM-dd HH:mm:ss":
    datetime_time = datetime.datetime.strptime(format_time,format)
    time_str = datetime_time.timetuple()
    timestamp = int(time.mktime(time_str))
    timestamp = timestamp*1000
    return timestamp