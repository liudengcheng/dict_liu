"""
    dict 客户端
    发起请求，展示结果
"""
from socket import *
import getpass

ADDR = ("127.0.0.1", 8000)
s = socket()
s.connect(ADDR)


def do_register():
    while True:
        name, password1 = input_name_password()
        password2 = getpass.getpass("Again:")
        if (" " in name) or (' ' in password1):
            print("用户名或者密码不能有空格")
        if password1 != password2:
            print("两次密码不一致")
            continue
        msg = "R %s %s" % (name, password1)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == "OK":
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


def do_query(name):
    while True:
        word = input("单词：")
        if word == '##':  # 结束查单词
            break
        msg = "Q %s %s" % (name, word)
        s.send(msg.encode())
        # 等待回复
        data = s.recv(2048).decode()
        print(data)
    # 创建网络连接


def do_query_history(name):
    number = input("请输入查询数量（1-10）,输入其值查询所有：")
    if number not in ('0 1 2 3 4 5 6 7 8 9 10'):
        number = '0'
    msg = "H %s %s" % (name, number)
    s.send(msg.encode())
    # 等待回复
    data = s.recv(2048).decode()
    print(data)


def login(name):
    while True:
        print("""
        ======================== Query ========================
        1.查单词                      2.历史记录                     3.注销
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_query(name)
        if cmd == '2':
            do_query_history(name)
        if cmd == '3':
            return
        else:
            print("请输入正确命令")


def do_login():
    name, password1 = input_name_password()
    msg = "L %s %s" % (name, password1)
    s.send(msg.encode())
    # 等待反馈
    data = s.recv(128).decode()
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print("登录失败")


def input_name_password():
    name = input("User:")
    password1 = getpass.getpass("Password:")
    return name, password1


def main():
    while True:
        print("""
        ======================== Welceome ========================
        1.注册                      2.登录                     3.退出
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_register()
        if cmd == '2':
            do_login()
        if cmd == '3':
            s.send(b'E')
            print("good bye")
            return
        else:
            print("请输入正确命令")


if __name__ == "__main__":
    main()
