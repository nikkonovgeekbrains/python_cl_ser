import json
import time
from socket import *

import argparse
import sys
import pickle
import os
import logging

import log.server_log_config
import logging

logger = logging.getLogger('app.server')



def init_socket(addr='', port=7777):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return s


def rx_cl_msg(client):
    data = client.recv(1000000)
    #return data.decode('utf-8')
    return data

def form_cl_msg(input_mes):
    logger.debug(f"json:{input_mes}")
    logger.debug(f"pikle:{pickle.loads(input_mes)}")
    #print(f"json:{input_mes}")
    #print(f"pikle:{pickle.loads(input_mes)}")
    #if json.loads(input_mes)["action"] == "presence":
    #print(f"Отправлен пакет{pickle.loads(input_mes)}")
    if pickle.loads(input_mes)["action"] == "presence":
        out_pack = pickle.dumps({
            "response": 100,
            #"time": time.ctime(datetime.now().timestamp()),
            "time": time.time(),
            "alert": "Hi, Client!"
        },)
        logger.info(f"Отправлен пакет {out_pack}")
        return out_pack

def form_probe_msg():
    return pickle.dumps({
        "action": "probe",
        "time": time.time()
    }, )

def send_msg(cl, msg):
    logger.info(f"Отправляется сообщение: {pickle.loads(msg)}")
    #print("Отправляется сообщение:", pickle.loads(msg))
    cl.send(msg)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Server App')
    parser.add_argument('-a', '--addr', default='')
    parser.add_argument('-p', '--port', default=7777, type=int)


    serv_soc = init_socket(parser.parse_args().addr, parser.parse_args().port)

    print(serv_soc)

    while True:
        client, addr = serv_soc.accept()
        inp_mes = rx_cl_msg(client)
        print(f'Сообщение: {pickle.loads(inp_mes)} было отправлено клиентом: {addr}')
        print(type(pickle.loads(inp_mes)))
        #print('Сообщение: ', pickle.loads(inp_mes), ', было отправлено клиентом: ', addr)
        #print(type(pickle.loads(inp_mes)))
        for i in range(3):
            send_msg(client, form_cl_msg(inp_mes))
        client.close()
