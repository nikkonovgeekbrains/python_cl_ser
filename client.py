import json
import time
from socket import *
import re
import sys

import argparse


def init_socket(addr, port):
    try:
        s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        s.connect((addr, port))  # Соединиться с сервером
        return s
    except Exception as e:
        print(e)


def pres_mes_form(name='undefined_user', status="Yep, I am here!"):
    return json.dumps({
        "action": "presence",
        #"time": time.ctime(datetime.now().timestamp()),
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": name,
            "status": status
        }
    },)


def send_msg(socket, msg):
    socket.send(msg.encode('utf-8'))

def rx_mes(socket):
    data = socket.recv(1000000)
    print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
    data_dict = json.loads(data)

    if re.search(r'^1\d\d', str(data_dict["response"])):
        print("Получено информационное сообщение от сервера с содержимым: ", data_dict["alert"])

    if re.search(r'^2\d\d', str(data_dict["response"])):
        print("Получено сообщение от сервера об успешном завершении с содержимым: ", data_dict["alert"])

    if re.search(r'^4\d\d', str(data_dict["response"])):
        print("Получено сообщение от сервера об ошибке на стороне клиента с содержимым: ", data_dict["alert"])

    if re.search(r'^5\d\d', str(data_dict["response"])):
        print("Получено сообщение от сервера об ошибке на стороне сервера с содержимым: ", data_dict["alert"])


if __name__ == '__main__':
    print(sys.argv[1])
    my_soc = init_socket(sys.argv[1], int(sys.argv[2]))
    if my_soc:
        send_msg(my_soc, pres_mes_form("Nikolay"))
        rx_mes(my_soc)
        my_soc.close()

