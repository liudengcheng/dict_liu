"""
    将dict。text导入到数据库中
"""
import pymysql,re
# 链接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='123456',
                     database='dict',
                     charset='utf8')
# 　获取游标
cur = db.cursor()



# 执行ｓｑｌ语句

fd=open('dict1.txt')

#获取单词与意思
while True:
    mystr=re.sub('\s+',' ',fd.readline(1048)).split(' ')
    if not mystr:
        break
    word=mystr[0]
    mean=' '.join(mystr[1:])
    # word='abacus'
    # mean="n.frame with beads that slide along parallel rods, used for teaching numbers to children, and (in some countries) for counting"

    # 数据操作
    sql_select="select * from words where word='%s';"%word
    cur.execute(sql_select)

    if cur.fetchone():
        # print("exist")
        continue
    else:
        try:
            sql_insert = 'insert into words(word,mean) values("%s","%s");'%(word,mean)
            cur.execute(sql_insert)
            db.commit()
            print(word,'successed')
        except Exception as e:
            db.rollback()
            print(e)
print("finished")