import unittest, logging, requests
from random import random

from bs4 import BeautifulSoup
from api.loginAPI import loginAPI
from api.trustAPI import trustAPI
from utils import assert_utils, request_third_api


class trust(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.trust_api = trustAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # ��������
    def test01_trust_request(self):
        # 1����֤ͨ�����˺ŵ�¼
        response = self.login_api.login(self.session)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "��¼�ɹ�")
        # 2�� ���Ϳ�������
        response = self.trust_api.trust_register(self.session)
        logging.info("trust register response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 3�� ���͵������Ŀ�������
        form_data = response.json().get("description").get("form")
        logging.info('form response={}'.format(form_data))
        # ���õ������ӿڵ����󷽷�
        response = request_third_api(form_data)
        # ������Ӧ���
        self.assertEqual(200, response.status_code)
        self.assertEqual('UserRegister OK', response.text)

    # ��ֵ�ɹ�
    def test02_recharge(self):
        # 1����¼�ɹ�
        # 1����֤ͨ�����˺ŵ�¼
        response = self.login_api.login(self.session)
        logging.info("login response = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "��¼�ɹ�")
        # 2�� ��ȡ��ֵ��֤��
        r = random()
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        logging.info("get recharge verify code reponse = {}".format(response.text))
        self.assertEqual(200, response.status_code)
        # 3�� ���ͳ�ֵ����
        response = self.trust_api.recharge(self.session, '10000')
        logging.info("recharge response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 4�� ���͵�������ֵ����
        # ��ȡ��Ӧ��form�������ݣ�����ȡΪ��������������Ĳ���
        form_data = response.json().get("description").get("form")
        logging.info('form response={}'.format(form_data))
        # ���õ���������Ľӿ�
        response = request_third_api(form_data)
        logging.info('third recharge response={}'.format(form_data))
        # ����response�Ƿ���ȷ
        self.assertEqual('NetSave OK', response.text)
