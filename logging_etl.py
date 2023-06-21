import logging
from datetime import datetime
#setup logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def log_etl(func):
    """decorator to log function name, arguments and time of execution
    :param func: function to be decorated
    :return: wrapper"""

    def wrapper(*args, **kwargs):
        logging.info('-----------------------------------')
        logging.info(f'Function {func.__name__} was called at {datetime.now()}')
        if len(args) !=0 or len(kwargs)!=0 : #if function has arguments log them
            logging.info('Function arguments:')
            logging.info(f'Arguments {args} and {kwargs}')
        return func(*args, **kwargs)
    return wrapper