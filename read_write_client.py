from socket import *
from select import select
import sys
import time
import pickle

MY_ACCOUNT_NAME = "Nikolay"

def msg_read_loop(my_socket):
    while True:
        data = pickle.loads(my_socket.recv(1024))
        print(f'Получено сообщение: {data}')

def form_user_user_text_msg(recipient, msg_text):
    return pickle.dumps({
        "action": "msg",
        "time": time.time(),
        "to": recipient,
        "from": MY_ACCOUNT_NAME,
        "encoding": "ascii",
        "message": msg_text
    })

def form_user_chat_text_msg(recipient, msg_text):
    return pickle.dumps({
        "action": "msg",
        "time": time.time(),
        "to": recipient,
        "from": MY_ACCOUNT_NAME,
        "message": msg_text
    })

def form_join_chat_msg(recipient):
    return pickle.dumps({
        "action": "join",
        "time": time.time(),
        "room": recipient
    })

def form_leave_chat_msg(recipient):
    return pickle.dumps({
        "action": "leave",
        "time": time.time(),
        "room": recipient
    })



def msg_write_loop(my_socket):
    while True:
        msg_type = input('Ведите тип отправляемого сообщения: (ut)- текстовое use-user, (ct)- текстовое user-chat, (j)- присоединиться к чату:\n')
        if msg_type == 'ut':
            msg_to = input('Введите имя пользователя:\n')
            msg_text = input('Введите текст сообщения:\n')
            my_socket.send(form_user_user_text_msg(msg_to, msg_text))
        elif msg_type == 'ct':
            msg_to = input('Введите имя пользователя:\n')
            msg_text = input('Введите текст сообщения:\n')
            my_socket.send(form_user_chat_text_msg(msg_to, msg_text))
        elif msg_type == 'j':
            msg_to = input('Введите имя беседы:\n')
            my_socket.send(form_join_chat_msg(msg_to))
        elif msg_type == 'l':
            msg_to = input('Введите имя беседы:\n')
            my_socket.send(form_leave_chat_msg(msg_to))
        elif msg_type == 'exit':
            break
        else:
            print("Некорректный ввод, попробуйте еще раз")


def echo_client(ADDRESS, ctype:str):
    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет автоматически закрыт
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(ADDRESS)  # Соединиться с сервером

        if ctype == 'r':
            msg_read_loop(sock)
        elif ctype == 'w':
            msg_write_loop(sock)
        else:
            print('Выбран некорректный режим работы!')


if __name__ == '__main__':
    ADDRESS = ('localhost', 7777)
    cl_type = input('Введите (w) для выбора пишущего или (r) для выбора читающего клиента:\n')
    echo_client(ADDRESS, cl_type)