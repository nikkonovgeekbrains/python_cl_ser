import json
import time
from socket import *

import argparse
import sys


def init_socket(addr='', port=7777):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return s


def rx_cl_msg(client):
    data = client.recv(1000000)
    return data.decode('utf-8')

def form_cl_msg(input_mes):
    if json.loads(input_mes)["action"] == "presence":
        return json.dumps({
            "response": 100,
            #"time": time.ctime(datetime.now().timestamp()),
            "time": time.time(),
            "alert": "Hi, Client!"
        },)

def send_msg(cl, msg):
    print("Отправляется сообщение:", msg)
    cl.send(msg.encode('utf-8'))


if __name__ == '__main__':
    print(sys.argv[1])
    serv_soc = init_socket(sys.argv[1], int(sys.argv[2]))

    print(serv_soc)

    while True:
        client, addr = serv_soc.accept()
        inp_mes = rx_cl_msg(client)
        print('Сообщение: ', inp_mes, ', было отправлено клиентом: ', addr)
        send_msg(client, form_cl_msg(inp_mes))
        client.close()
