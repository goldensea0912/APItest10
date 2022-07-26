import logging
from logging import handlers
import os, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "http://user-p2p-test.itheima.net"
MOBILE_URL = "http://mobile-p2p-test.itheima.net"
DB_URL = '52.83.144.39'
DB_USERNAME = 'root'
DB_PASSWORD = 'Itcast_p2p_20191228'
DB_MEMBER = 'czbk_member'
DB_FINANCE = 'czbk_finance'


# ��ʼ����־����
def init_log_config():
    # 1����ʼ����־����
    logger = logging.getLogger()
    # 2��������־����
    logger.setLevel(logging.INFO)
    # 3����������̨��־���������ļ���־������
    sh = logging.StreamHandler()

    logfile = BASE_DIR + os.sep + "log" + os.sep + "p2p.log"
    fh = logging.handlers.TimedRotatingFileHandler(logfile, when='M', interval=5, backupCount=5, encoding='UTF-8')
    # 4��������־��ʽ��������ʽ����
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)
    # 5������ʽ�������õ���־����
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 6������־��������ӵ���־����
    logger.addHandler(sh)
    logger.addHandler(fh)
