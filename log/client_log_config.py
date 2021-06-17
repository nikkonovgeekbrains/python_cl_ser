import logging
import sys

logger = logging.getLogger('app.client')

out_file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")
out_stream_formater = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")

my_file_handler = logging.FileHandler("app.client.log", encoding='utf-8')
my_file_handler.setLevel(logging.DEBUG)
my_file_handler.setFormatter(out_file_formatter)

my_stream_handler = logging.StreamHandler(sys.stdout)
my_stream_handler.setLevel(logging.DEBUG)
my_stream_handler.setFormatter(out_stream_formater)

logger.addHandler(my_file_handler)
logger.addHandler(my_stream_handler)

logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('Тестовый запуск логирования')