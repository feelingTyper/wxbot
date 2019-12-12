# coding: utf-8

import re
import time
import logging
import datetime
from functools import wraps


def logit(func):
    """
    decorator for logging, for aspect oriented programming
    """
    @wraps(func)
    def wrapped_function(self, *args, **kwargs):
        start = time.time()
        try:
            result = func(self, *args, **kwargs)
            logging.info(
                    'running class {} function {} success. time cost: {}'
                    .format(self.__class__, func.__name__, time.time()-start))
            return result
        except Exception:
            logging.exception(
                    'running class {} function {} failed. time cost: {}'
                    .format(self.__class__, func.__name__,  time.time()-start))
            return None

    return wrapped_function


def timestamp2datetime(timestamp):
    try:
        d = datetime.datetime.fromtimestamp(timestamp)
        return d
    except Exception:
        logging.error('parse timestamp fail')


def timestamp2datestring(timestamp):
    try:
        d = datetime.datetime.fromtimestamp(timestamp)
        date_str = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        return date_str
    except Exception:
        logging.error('parse timestamp fail')


def string2timestamp(strValue):
    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")
        t = d.timetuple()
        timestamp = int(time.mktime(t))
        timestamp = float(str(timestamp) + str("%06d" % d.microsecond))/1000000
        return timestamp
    except Exception:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timestamp = int(time.mktime(t))
        timestamp = float(str(timestamp) + str("%06d" % d.microsecond))/1000000
        return timestamp


def datetime2timestamp(d):
    try:
        t = d.timetuple()
        timestamp = int(time.mktime(t))
        return timestamp
    except Exception:
        d = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timestamp = int(time.mktime(t))
        timestamp = float(str(timestamp) + str("%06d" % d.microsecond))/1000000
        return timestamp


def strpdate(datestr, fmt='%Y-%m-%d'):
    return datetime.datetime.strptime(datestr, fmt)


def check_future(date):
    return (date - now()).days >= 0


def now():
    return datetime.datetime.now()


def today():
    return datetime.date.today()


def tomorrow():
    return today() + datetime.timedelta(days=1)


def yesterday():
    return today() - datetime.timedelta(days=1)


def dayafter(days):
    return today() + datetime.timedelta(days=days)


def daybefore(days):
    return today() - datetime.timedelta(days=days)


def retries(retry=2, condition=False):
    """decorator for retry call function

    :param max retry times to recall the function, default 2
    :param condition condition to continue retry,
    general is the upexpected retrun value of the called function,
    default False
    :return object function
    """
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            vretry = retry
            result = condition
            while vretry:
                try:
                    vretry = vretry - 1
                    result = func(*args, **kwargs)
                    if result is not condition:
                        return result
                except Exception:
                    continue
            logging.warning(
                    'running function {func} failed after retry {retry} times'.
                    format(func=func.__name__, retry=retry))
            return result
        return wrapped_function
    return decorator


def message_desc(content):
    result = re.search(r'<des>([\s\S]+?)</des>', content)
    if result:
        return result.group(1)
