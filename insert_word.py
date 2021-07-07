import pymysql, re

f = open('dict.txt')
# 链接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='123456',
                     database='dict',
                     charset='utf8')
cur = db.cursor()
for line in f:
    tup = re.findall(r'(\w+)\s+(.*)', line)[0]
    sql = 'insert into words (word,mean) VALUES ("%s","%s")' % tup

    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
f.close()
cur.close()
db.close()
