"""
    dict服务端
    处理请求逻辑
"""
import sys
from socket import *
from multiprocessing import Process
import signal
from operation_db import *

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)


def do_request(c, db):
    db.create_cursor()  # 生成游标db.cur
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(), ':', data)
        if not data or data[0] == "E":
            # db.close()
            c.close()
            sys.exit("客户端退出")
        elif data[0] == 'R':
            do_register(c, data, db)
        elif data[0] == 'L':
            do_login(c, data, db)
        elif data[0] == 'Q':
            do_query(c, db, data)
        elif data[0] == "H":
            do_query_history(c, db, data)


def do_query_history(c, db, data):
    name, number = split_data(data)
    data = db.query_history(name, number)
    if not data:
        c.send("无历史记录".encode())
    else:
        c.send(data.encode())


def do_query(c, db, data):
    name, word = split_data(data)
    # 插入历史记录
    db.insert_history(name, word)

    # 查单词,没查到返回none
    mean = db.query(word)
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        msg = (word + ':' + mean).encode()
        c.send(msg)


def do_login(c, data, db):
    name, passwd = split_data(data)
    if db.login(name, passwd):
        c.send('OK'.encode())
    else:
        c.send(b'FAIL')


def do_register(c, data, db):
    name, passwd = split_data(data)
    if db.register(name, passwd):
        c.send('OK'.encode())
    else:
        c.send(b'FAIL')


def split_data(data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    return name, passwd


def main():
    # 创建数据库链接对象
    db = Database()
    # 创建tcp套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("Listen the port 8000")
    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 等待客户端链接
    while True:
        try:
            c, addr = sockfd.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            sockfd.close()
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        p = Process(target=do_request, args=(c, db))
        p.daemon = True
        p.start()


if __name__ == "__main__":
    main()
