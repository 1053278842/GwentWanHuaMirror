import MySQLdb
import re

db = MySQLdb.connect("117.50.175.251", "root", "LiuLong123123+", "blog", charset='utf8' )

cursor = db.cursor()
sql = 'SELECT * FROM article '
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        context = row[5]
        context_md = row[6]
        # 这里改！！！！！！！！！！！！！！！！！！！！！！！！！
        result = re.sub(r'http://(onemorechance.xyz)/',"http://117.50.175.251:8232/",context,0,0)
        result_md = re.sub(r'http://(onemorechance.xyz)/',"http://117.50.175.251:8232/",context_md,0,0)
        print(result_md)
        try:
            updateSql = "UPDATE article SET context = '{0}' , context_md = '{1}' where id = {2}".format(result, result_md ,id)
            cursor.execute(updateSql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

except:
    print("error")

db.close()


#############################################################################################
# db = MySQLdb.connect("117.50.175.251", "root", "LiuLong123123+", "blog", charset='utf8' )

# cursor = db.cursor()
# sql = 'SELECT * FROM article '
# try:
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     for row in results:
#         id = row[0]
#         context = row[5]
#         context_md = row[6]
#         # 这里改！！！！！！！！！！！！！！！！！！！！！！！！！
#         result = re.sub(r'http://(110.42.155.172)/',"http://117.50.175.251:8232/",context,0,0)
#         result_md = re.sub(r'http://(110.42.155.172)/',"http://117.50.175.251:8232/",context_md,0,0)
#         print(result_md)
#         try:
#             updateSql = "UPDATE article SET context = '{0}' , context_md = '{1}' where id = {2}".format(result, result_md ,id)
#             cursor.execute(updateSql)
#             db.commit()
#         except Exception as e:
#             print(e)
#             db.rollback()

# except:
#     print("error")

# db.close()
