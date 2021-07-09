"""
    dict项目用于处理数据
"""
import time

import pymysql
import hashlib


# 编写功能类 提供给服务端使用
class Database:
    def __init__(self,
                 database='dict',
                 host='localhost',
                 user='root',
                 passwd='123456',
                 port=3306,
                 charset='utf8',
                 ):
        self.database = database
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.charset = charset
        # self.table = table
        self.connect_db()  # 连接数据库

    # 创建数据库
    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  user=self.user,
                                  port=self.port,
                                  database=self.database,
                                  passwd=self.passwd,
                                  charset=self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.cur.close()
        self.db.close()

    def register(self, name, passwd):
        sql = "select * from user where name = '%s';" % name
        self.cur.execute(sql)
        if self.cur.fetchone():
            return False
        hash = self.hash_password(name, passwd)
        sql = "insert into user (name,passwd) values('%s','%s');" % (name, hash.hexdigest())
        try:
            self.cur.execute(sql)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def hash_password(self, name, passwd):
        hash = hashlib.md5((name + 'the-salt').encode())
        hash.update(passwd.encode())
        return hash

    def login(self, name, passwd):
        hash = self.hash_password(name, passwd)
        sql = "select * from user where name = '%s' and passwd = '%s';" % (name, hash.hexdigest())
        self.cur.execute(sql)
        if self.cur.fetchone():
            return True
        return False

    def insert_history(self, name, word):
        tm = time.ctime()
        sql = "insert into hist (name,word,time) values (%s,%s,%s);"
        try:
            self.cur.execute(sql, [name, word, tm])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def query(self, word):
        sql = "select mean from words where word = '%s';" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]
        return None

    def query_history(self, name, number):
        sql = "select time,word from hist where name ='%s' order by id desc" % name
        if number is not '0':
            sql += " limit %s" % number
        sql+=';'
        self.cur.execute(sql)
        return str(self.cur.fetchall())
