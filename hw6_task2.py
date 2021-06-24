import inspect
import logging
import sys

logger = logging.getLogger('app.hw6_task2')

out_stream_formater = logging.Formatter("%(asctime)s - %(message)s ")


my_stream_handler = logging.StreamHandler(sys.stdout)
my_stream_handler.setLevel(logging.DEBUG)
my_stream_handler.setFormatter(out_stream_formater)

logger.addHandler(my_stream_handler)

logger.setLevel(logging.DEBUG)

def log(func):
    def callf(*args,**kwargs):
        current_frame = inspect.currentframe()

        caller_frame = current_frame.f_back
        code_obj = caller_frame.f_code
        code_obj_name = code_obj.co_name
        logger.debug(f"Функция: {func.__name__}{str(args).replace('{','').replace('{','')} вызвана из функции {code_obj_name}")
        r = func(*args, **kwargs)
        return r
    return callf

@log
def func_z():
    pass

def main():
    func_z()

if __name__ == '__main__':
    main()