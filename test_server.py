import unittest
import client
import subprocess
import pickle
import time
import socket
import server

def bin_to_dict_wuthout_time_filed(inp_data):
    new_dict = pickle.loads(inp_data)
    new_dict.pop('time')
    return new_dict

class TestSplitFunction(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_socket(self):
        my_soc = server.init_socket(addr='localhost', port=8082)
        self.assertEqual(type(my_soc), type(socket.socket()))


    def test_form_cl_msg(self):
        imp_mes = b'\x80\x03}q\x00(X\x06\x00\x00\x00actionq\x01X\x08\x00\x00\x00presenceq\x02X\x04\x00\x00\x00timeq\x03GA\xd81\xdf]v\xe0\x9bX\x04\x00\x00\x00typeq\x04X\x06\x00\x00\x00statusq\x05X\x04\x00\x00\x00userq\x06}q\x07(X\x0c\x00\x00\x00account_nameq\x08X\x07\x00\x00\x00Nikolayq\th\x05X\x0f\x00\x00\x00Yep, I am here!q\nuu.'
        r = b'\x80\x03}q\x00(X\x08\x00\x00\x00responseq\x01KdX\x04\x00\x00\x00timeq\x02GA\xd81\xe0M\xb1\xf8\xe5X\x05\x00\x00\x00alertq\x03X\x0b\x00\x00\x00Hi, Client!q\x04u.'

        r_dict = bin_to_dict_wuthout_time_filed(r)
        outp_mes_dict = bin_to_dict_wuthout_time_filed(server.form_cl_msg(imp_mes))

        self.assertEqual(r_dict, outp_mes_dict)

    def test_rx_cl_msg(self):
        r_inp_mes = b'\x80\x03}q\x00(X\x06\x00\x00\x00actionq\x01X\x08\x00\x00\x00presenceq\x02X\x04\x00\x00\x00timeq\x03GA\xd81\xe0\xed0\xbdKX\x04\x00\x00\x00typeq\x04X\x06\x00\x00\x00statusq\x05X\x04\x00\x00\x00userq\x06}q\x07(X\x0c\x00\x00\x00account_nameq\x08X\x07\x00\x00\x00Nikolayq\th\x05X\x0f\x00\x00\x00Yep, I am here!q\nuu.'
        r_inp_mes_dict = bin_to_dict_wuthout_time_filed(r_inp_mes)

        sevr_soc = server.init_socket(addr='localhost', port=8083)
        time.sleep(4)
        subprocess.Popen("python client.py -a=localhost -p=8083", shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        while True:
            client, addr = sevr_soc.accept()
            inp_mes_dict = bin_to_dict_wuthout_time_filed(server.rx_cl_msg(client))
            break
        self.assertEqual(r_inp_mes_dict, inp_mes_dict)



if __name__ == '__main__':
    unittest.main()