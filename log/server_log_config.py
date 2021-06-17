import logging
import sys
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('app.server')

out_file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")
out_stream_formater = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")

my_file_handler = TimedRotatingFileHandler("app.server.log", when='d', interval=1, backupCount=0, encoding='utf-8')
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