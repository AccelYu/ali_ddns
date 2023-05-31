import time
import traceback
from functools import wraps


def info(msg):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    f = open('./ddns.log', 'a', encoding='utf8')
    f.write('[%s][info]%s\n' % (current_time, msg))
    f.close()


def error(msg):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    f = open('./ddns.log', 'a', encoding='utf8')
    f.write('[%s][error]%s' % (current_time, msg))
    f.close()


def logger_exc(msg):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                info(msg)
                result = func(*args, **kwargs)
                info(msg + '成功')
                return result
            except Exception:
                error('%s失败\n%s' % (msg, traceback.format_exc()))
        return inner
    return wrapper
