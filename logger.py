import logging
from functools import wraps
import traceback
from queue import Queue


class QueueFileHandler(logging.FileHandler):
    def __init__(self, queue, **args):
        super().__init__(**args)
        self.queue = queue

    def emit(self, record):
        super().emit(record)
        self.queue.put(f'[{record.asctime}] [{record.levelname:>5}] {record.message}')


mq = Queue()
log = logging.getLogger()
log.setLevel(logging.INFO)
qfh = QueueFileHandler(mq, filename='./ddns.log', encoding='utf8')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)5s] %(message)s')
qfh.setFormatter(formatter)
log.addHandler(qfh)


def log_exc(msg):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                log.info(msg)
                result = func(*args, **kwargs)
                log.info(msg + '成功')
                return result
            except Exception:
                log.error('%s失败\n%s' % (msg, traceback.format_exc()))
        return inner
    return wrapper
