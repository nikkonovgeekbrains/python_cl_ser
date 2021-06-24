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
import select

logger = logging.getLogger('app.server')

def log(func):
    def callf(*args,**kwargs):
        logger.debug(f"Вызвана функция: {func.__name__} c позиционными аргументами {args} и имнованными аргументами {kwargs}")
        r = func(*args,**kwargs)
        return r
    return callf

@log
def init_socket(addr='', port=7777):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    #s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.settimeout(0.2)  # Таймаут для операций с сокетом
    return s

@log
def rx_cl_msg(client):
    data = client.recv(1000000)
    #return data.decode('utf-8')
    return data

@log
def form_cl_msg(input_mes):
    logger.debug(f"json:{input_mes}")
    logger.debug(f"pikle:{pickle.loads(input_mes)}")
    if pickle.loads(input_mes)["action"] == "presence":
        out_pack = pickle.dumps({
            "response": 100,
            #"time": time.ctime(datetime.now().timestamp()),
            "time": time.time(),
            "alert": "Hi, Client!"
        },)
        logger.info(f"Отправлен пакет {out_pack}")
        return out_pack

@log
def form_probe_msg():
    return pickle.dumps({
        "action": "probe",
        "time": time.time()
    }, )

@log
def send_msg(cl, msg):
    logger.info(f"Отправляется сообщение: {pickle.loads(msg)}")
    #print("Отправляется сообщение:", pickle.loads(msg))
    cl.send(msg)

def read_requests(r_clients, all_clients):
   """ Чтение запросов из списка клиентов
   """
   responses = {}  # Словарь ответов сервера вида {сокет: запрос}

   for sock in r_clients:
       try:
           #data = sock.recv(1024).decode('utf-8')
           data = pickle.loads(sock.recv(1024))
           if data:
            print(data)
           responses[sock] = data
       except:
           print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
           all_clients.remove(sock)
   return responses


def write_responses(requests, w_clients, all_clients):
   """ Эхо-ответ сервера клиентам, от которых были запросы
   """

   for sock in w_clients:
       if sock in requests:
           try:
               # Подготовить и отправить ответ сервера
               resp = pickle.dumps(requests[sock])
               print(f"resp!!!:{resp}")
               for outp_soc in all_clients:
                   print(f"soc: {outp_soc}")
                   outp_soc.send(resp)
           except:  # Сокет недоступен, клиент отключился
               print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
               sock.close()
               all_clients.remove(sock)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Server App')
    parser.add_argument('-a', '--addr', default='')
    parser.add_argument('-p', '--port', default=7777, type=int)


    serv_soc = init_socket(parser.parse_args().addr, parser.parse_args().port)
    clients = []

    print(serv_soc)

    while True:
        # client, addr = serv_soc.accept()
        # inp_mes = rx_cl_msg(client)
        # print(f'Сообщение: {pickle.loads(inp_mes)} было отправлено клиентом: {addr}')
        # print(type(pickle.loads(inp_mes)))
        # #for i in range(3):
        # #    send_msg(client, form_cl_msg(inp_mes))
        # client.close()
        try:
            conn, addr = serv_soc.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
                # print(r)
                # print(w)
                # print(e)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            #print(requests)
            if requests:
                write_responses(requests, w, clients)  # Выполним отправку ответов клиентам


