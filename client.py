import json
import time
from socket import *
import re
import sys

import argparse
import pickle


def init_socket(addr, port):
    try:
        s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        s.connect((addr, port))  # Соединиться с сервером
        return s
    except Exception as e:
        print(e)


def pres_mes_form(name='undefined_user', status="Yep, I am here!"):
    #return json.dumps({
    return pickle.dumps({
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
    #socket.send(msg.encode('utf-8'))
    socket.send(msg)

def rx_mes(socket):
    data = socket.recv(1000000)
    print('Сообщение от сервера: ', pickle.loads(data), ', длиной ', len(data), ' байт')
    data_dict = pickle.loads(data)

    if re.search(r'^1\d\d', str(data_dict["response"])):
        print("Получено информационное сообщение от сервера с содержимым: ", data_dict["alert"])

    if re.search(r'^2\d\d', str(data_dict["response"])):
        print("Получено сообщение от сервера об успешном завершении с содержимым: ", data_dict["alert"])

    if re.search(r'^4\d\d', str(data_dict["response"])):
        print("Получено сообщение от сервера об ошибке на стороне клиента с содержимым: ", data_dict["alert"])

    if re.search(r'^5\d\d', str(data_dict["response"])):
        print("Получено сообщение от сервера об ошибке на стороне сервера с содержимым: ", data_dict["alert"])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Client App')
    parser.add_argument('-a', '--address', default='localhost')
    parser.add_argument('-p', '--port', default=7777, type=int)

    my_soc = init_socket(parser.parse_args().address, parser.parse_args().port)
    if my_soc:
        send_msg(my_soc, pres_mes_form("Nikolay"))
        rx_mes(my_soc)
        my_soc.close()

