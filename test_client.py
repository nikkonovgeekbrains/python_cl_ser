import unittest
import client
import subprocess
import pickle
import time
import socket

def bin_to_dict_wuthout_time_filed(inp_data):
    new_dict = pickle.loads(inp_data)
    new_dict.pop('time')
    return new_dict



class TestSplitFunction(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testinitsocket(self):
        #Делаю проверку через запуск сервера как субпроцесс, из-за блокировок потом в сервере вылетает ошибка, но сокет создается
        subprocess.Popen("python server.py -a=localhost -p=8080", shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        print("opening server")
        time.sleep(4)
        print("opening socket")
        my_soc = client.init_socket('localhost', 8080)
        con_type = type(my_soc)
        #Добавил просто чтобы не ругался сервер об отсутствии приветственного сообщения
        client.send_msg(my_soc, client.pres_mes_form("Nikolay"))

        self.assertEqual(con_type, type(socket.socket()))
        pass

    def testpresmesform(self):

        r = b'\x80\x03}q\x00(X\x06\x00\x00\x00actionq\x01X\x08\x00\x00\x00presenceq\x02X\x04\x00\x00\x00timeq\x03GA\xd81\xda$\xb9\xec\xffX\x04\x00\x00\x00typeq\x04X\x06\x00\x00\x00statusq\x05X\x04\x00\x00\x00userq\x06}q\x07(X\x0c\x00\x00\x00account_nameq\x08X\x07\x00\x00\x00Nikolayq\th\x05X\x0f\x00\x00\x00Yep, I am here!q\nuu.'
        #Делаю через словари, чтобы не учитывать метку времени, так как она привязана к текущему времени
        # r_dict = pickle.loads(r)
        # r_dict.pop('time')
        r_dict = bin_to_dict_wuthout_time_filed(r)
        proc_dict = pickle.loads(client.pres_mes_form('Nikolay'))
        proc_dict.pop('time')
        self.assertEqual(r_dict, proc_dict)


    def testrxmes_100(self):
        subprocess.call("exit 1", shell=True)
        r = 1
        self.assertEqual(r, client.proc_rx_mes({'response': 100, 'time': 1623673513.9170556, 'alert': 'Hi, Client!'}))

    def testrxmes_200(self):
        r = 2
        self.assertEqual(r, client.proc_rx_mes({'response': 200, 'time': 1623673513.9170556, 'alert': 'Succes'}))

    def testrxmes_400(self):
        r = 4
        self.assertEqual(r, client.proc_rx_mes({'response': 400, 'time': 1623673513.9170556, 'alert': 'Client ERROR!'}))

    def testrxmes_500(self):
        r = 5
        self.assertEqual(r, client.proc_rx_mes({'response': 500, 'time': 1623673513.9170556, 'alert': 'Server ERROR!'}))

# Запустить тестирование
if __name__ == '__main__':
    unittest.main()
