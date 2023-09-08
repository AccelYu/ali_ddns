import logging
from functools import wraps
import traceback

log = logging.getLogger()
log.setLevel(logging.INFO)


class QueueFileHandler(logging.FileHandler):
    """
    继承FileHandler，将日志内容放入队列，使得ui界面能获取日志内容并打印
    """
    def __init__(self, queue, **args):
        super().__init__(**args)
        self.queue = queue

    def emit(self, record):
        super().emit(record)
        self.queue.put(f'[{record.asctime}] [{record.levelname:>5}] {record.message}')


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
