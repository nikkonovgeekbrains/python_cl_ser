import json
import time
from socket import *
import re
import sys

import argparse
import pickle
import os
import log.client_log_config
import logging

logger = logging.getLogger('app.client')



def init_socket(addr, port):
    try:
        s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        s.connect((addr, port))  # Соединиться с сервером
        logger.info("Соединение с сервером")
        return s
    except Exception as e:
        #print(e)
        logger.error(e)
        return None


def pres_mes_form(name='undefined_user', status="Yep, I am here!"):
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
    logger.debug(f"Отправлен пакет: {msg}")
    socket.send(msg)

def rx_mes(socket):
    data = socket.recv(1000000)
    logger.debug(f"Отправлен пакет: {data}")
    logger.info(f'Сообщение от сервера: {pickle.loads(data)}, длиной {len(data)} байт')
    #print('Сообщение от сервера: ', pickle.loads(data), ', длиной ', len(data), ' байт')
    data_dict = pickle.loads(data)
    proc_rx_mes(data_dict)

def proc_rx_mes(msg_dict):
    print(msg_dict)
    if "response" in msg_dict:
        if msg_dict["response"] == 100:
            print("Получено информационное сообщение от сервера с содержимым: ", msg_dict["alert"])
            return 1

        if msg_dict["response"] == 200:
            print("Получено сообщение от сервера об успешном завершении с содержимым: ", msg_dict["alert"])
            return 2

        if msg_dict["response"] == 400:
            print("Получено сообщение от сервера об ошибке на стороне клиента с содержимым: ", msg_dict["alert"])
            return 4

        if msg_dict["response"] == 500:
            print("Получено сообщение от сервера об ошибке на стороне сервера с содержимым: ", msg_dict["alert"])
            return 5
        else:
            return 0
    elif "action" in msg_dict:
        #print("Получен запрос проверки соединения с сервером")
        send_msg(my_soc, pres_mes_form("Nikolay"))
        logger.info("Получен запрос проверки соединения с сервером")
        return 5
    else:
        #print(f"Получено неизвестное сообщение от сервера: {msg_dict}")
        logger.info(f"Получено неизвестное сообщение от сервера: {msg_dict}")
        return 0




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Client App')
    parser.add_argument('-a', '--address', default='localhost')
    parser.add_argument('-p', '--port', default=7777, type=int)

    my_soc = init_socket(parser.parse_args().address, parser.parse_args().port)
    if my_soc:
        send_msg(my_soc, pres_mes_form("Nikolay"))
        rx_mes(my_soc)
        rx_mes(my_soc)
        my_soc.close()

