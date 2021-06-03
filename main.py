import re
import csv
import json
import yaml

# Задание 1
def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for inp_file in ['info_1.txt', 'info_1.txt', 'info_1.txt']:
        with open(inp_file) as f:
            for inp_str in f:
                if re.search('^Изготовитель системы:\s+', inp_str):
                    os_prod_list.append(re.sub('^Изготовитель системы:\s+|\n', '', inp_str))
                if re.search('^Название ОС:\s+', inp_str):
                    os_name_list.append(re.sub('^Название ОС:\s+|\n', '', inp_str))
                if re.search('^Код продукта:\s+', inp_str):
                    os_code_list.append(re.sub('^Код продукта:\s+|\n', '', inp_str))
                if re.search('^Тип системы:\s+', inp_str):
                    os_type_list.append(re.sub('^Тип системы:\s+|\n', '', inp_str))
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for i in range(len(os_prod_list)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])
    return main_data

def write_to_csv(csv_file_name):
    with open(csv_file_name, 'w') as f:
        f_n_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in get_data():
            f_n_writer.writerow(row)

# Задание 2
def write_order_to_json(item, quantity, price, buyer, date):
    cur_orders = []
    with open('orders.json') as json_f:
        for el in json.load(json_f)['orders']:
            cur_orders.append(el)
    cur_orders.append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})

    with open('orders.json', 'w') as output_f:
        json.dump({'orders': cur_orders}, output_f, indent=4)
# Задание 3


if __name__ == '__main__':
    # Задание 1
    print('Задание 1\n\n')
    write_to_csv('my_csv_file.csv')

    with open('my_csv_file.csv') as f:
        print(f.read())

    with open('my_csv_file.csv') as f:
        f_n_reader = csv.reader(f)
        print(list(f_n_reader))

    # Задание 2
    print('\n\n\n\n\n\n\nЗадание 2\n\n')
    #Приводим файл в исходное состояние, чтобы не копились данные при перезапуске программы
    with open('orders.json', 'w') as output_f:
        json.dump({'orders': []}, output_f, indent=4)

    write_order_to_json('phone', 2, 35000, 'Nikolay', '10-11-2020')
    write_order_to_json('notebook', 1, 155000, 'Evgeny', '15-05-2021')
    write_order_to_json('bike', 1, 230000, 'Leonid', '20-07-2020')

    with open('orders.json') as json_f:
        print(json.load(json_f)['orders'])

    # Задание 3
    print('\n\n\n\n\n\n\nЗадание 3\n\n')
    task3_data = {
        'data1': ['data1.1', 'data1.2', 'data1.3', 'data1.4'],
        'data2': 1234,
        'data3': {'key3.1': '\u20ac', 'key3.2': '\u20e4', 'key3.3': '\u00df'}
    }

    print(task3_data)
    with open('file.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(task3_data, f, default_flow_style=False, allow_unicode=True)

    with open('file.yaml', 'r', encoding='utf-8') as f:
        inp_data = yaml.load(f, Loader=yaml.FullLoader)
        print(inp_data)


