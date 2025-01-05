import logging
from logging import handlers
import sys

# the filter function need be double checked
# where the info is dict type, it will exit abnormally
# dict type has no find attribute
class ContextFilter(logging.Filter):
    def filter(self, record):
        if record.msg.find('UserWarning') == -1:
            return True
        else:
            return False


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critic': logging.CRITICAL
    }

    # - %(pathname)s[line:%(lineno)d]
    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)

        # set log format
        format_str = logging.Formatter(fmt)

        # set log level
        self.logger.setLevel(self.level_relations.get(level))

        # handler : output to stdout
        to_stdout = logging.StreamHandler(sys.stdout)

        # associate format with handler
        to_stdout.setFormatter(format_str)

        # filter used to
        # to_stdout_filter = ContextFilter()
        # to_stdout.addFilter(to_stdout_filter)

        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        to_file = handlers.TimedRotatingFileHandler(filename=filename, when=when,
                                                    backupCount=backCount,
                                                    encoding='utf-8')

        # associate format with handler
        to_file.setFormatter(format_str)

        # add the handler into logger
        self.logger.addHandler(to_stdout)
        self.logger.addHandler(to_file)
