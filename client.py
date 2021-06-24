from socket import *

s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect(('localhost', 8888))  # Соединиться с сервером

while True:  # Постоянный опрос сервера
    tm = s.recv(1024)
    print("Текущее время: %s" % tm.decode('utf-8'))

s.close()