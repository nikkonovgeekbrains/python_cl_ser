import subprocess

def print_var_info(var, name):
    print(f"Type of {name} ({var}): {type(var)}, len: {len(var)}")


if __name__ == '__main__':

    # Задание 1
    print("task1:")

    str1 = "разработка"
    str2 = "сокет"
    str3 = "декоратор"

    print(f"Type of str1 ({str1}): {type(str1)}")
    print(f"Type of str2 ({str2}): {type(str2)}")
    print(f"Type of str3 ({str3}): {type(str3)}")

    # Используем онлайн-конвертер для преобразования
    # разработка: \xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0
    # сокет: \xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82
    # декоратор: \xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80
    # Формат явно похож на bytes, но если определить просто в ковычках, то все равно получим конвертацию в строку

    # Проверим:
    str1_uni = str1.encode('utf-8')
    str2_uni = str2.encode('utf-8')
    str3_uni = str3.encode('utf-8')

    print(f"Type of str1 ({str1_uni}): {type(str1_uni)}")
    print(f"Type of str2 ({str2_uni}): {type(str2_uni)}")
    print(f"Type of str3 ({str3_uni}): {type(str3_uni)}")

    # Задание 2
    print("\n\n\ntask2:")
    bytes1 = bytes("class", 'utf-8')
    bytes2 = bytes("function", 'utf-8')
    bytes3 = bytes("method", 'utf-8')

    # В содержании переменных выведет все равно символы, так как они есть в стандартном алфавите ASCII
    print_var_info(bytes1, "bytes1")
    print_var_info(bytes2, "bytes2")
    print_var_info(bytes3, "bytes3")

    # Задание 3
    print("\n\n\ntask3:")

    # Напрямую в байтовом типе можно задать только слова attribute и type, так как кирилица
    # не входит в ASCII, закодировать в байты слова класс и функция можно только с помощью bytes() или encode(),
    # указав кодировку, но это уже будет не ASCII (в UTF-8 каждый символ займет два байта)
    bytes_s_1 = b'attribute'
    #bytes_s_2 = b'класс'  --выдаст ошибку
    # bytes_s_3 = b'функция' -- выдаст ошибку
    bytes_s_2 = bytes("класс", 'utf-8')
    bytes_s_3 = bytes("функция", 'utf-8')
    bytes_s_4 = b'type'

    print_var_info(bytes_s_1, "bytes_s_1")
    print_var_info(bytes_s_2, "bytes_s_2")
    print_var_info(bytes_s_3, "bytes_s_3")
    print_var_info(bytes_s_4, "bytes_s_4")

    # Задание 4
    print("\n\n\ntask4:")

    enc_str_bytes_1 = "разработка".encode('utf-8')
    enc_str_bytes_2 = "администрирование".encode('utf-8')
    enc_str_bytes_3 = "protocol".encode('utf-8')
    enc_str_bytes_4 = "standard".encode('utf-8')

    dec_str_bytes_1 = enc_str_bytes_1.decode('utf-8')
    dec_str_bytes_2 = enc_str_bytes_2.decode('utf-8')
    dec_str_bytes_3 = enc_str_bytes_3.decode('utf-8')
    dec_str_bytes_4 = enc_str_bytes_4.decode('utf-8')

    print_var_info(enc_str_bytes_1, "enc_str_bytes_1")
    print_var_info(enc_str_bytes_2, "enc_str_bytes_2")
    print_var_info(enc_str_bytes_3, "enc_str_bytes_3")
    print_var_info(enc_str_bytes_4, "enc_str_bytes_4")

    print_var_info(dec_str_bytes_1, "dec_str_bytes_1")
    print_var_info(dec_str_bytes_2, "dec_str_bytes_1")
    print_var_info(dec_str_bytes_3, "dec_str_bytes_1")
    print_var_info(dec_str_bytes_4, "dec_str_bytes_1")

    # Задание 5
    print("\n\n\ntask5:")

    def ping_resource(res_name):
        my_subproc = subprocess.Popen(['ping', res_name], stdout=subprocess.PIPE)
        for outp_str in my_subproc.stdout:
            outp_str = outp_str.decode('cp866').encode('utf-8')
            print(outp_str.decode('utf-8'))


    ping_resource("yandex.ru")
    ping_resource("youtube.com")

    # Задание 6
    print("\n\n\ntask6:")

    with open("test_file.txt", "w") as myfile:
        myfile.write("сетевое программирование\nсокет\nдекоратор\n")

    print(myfile)

    #with open('test_file.txt', encoding='cp1251') as read_file:        # --будет работать, так как у меня по умолчанию 1251 формат
    with open('test_file.txt', encoding='utf-8') as read_file:          # --выдаст ошибку
        try:
            for new_str in read_file:
                print(new_str)
        except Exception as exc:
            print(exc)



