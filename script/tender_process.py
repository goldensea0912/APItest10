import logging
import random

import requests, unittest

import app
from api.loginAPI import loginAPI
from api.tenderAPI import tenderAPI
from api.trustAPI import trustAPI
from utils import assert_utils, request_third_api, DButils


class test_tender_process(unittest.TestCase):
    phone = '13033447715'
    tender_id = 697
    imVerifyCode = '8888'

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = loginAPI()
        cls.tender_api = tenderAPI()
        cls.trust_api = trustAPI()
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()
        sql1 = "delete from mb_member_register_log where phone in ('13033447711','13033447712','13033447713','13033447714','13033447715');"
        DButils.delete(app.DB_MEMBER, sql1)
        logging.info("delete sql = {}".format(sql1))
        sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13033447711','13033447712','13033447713','13033447714','13033447715');"
        DButils.delete(app.DB_MEMBER, sql2)
        logging.info("delete sq2 = {}".format(sql2))
        sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ('13033447711','13033447712','13033447713','13033447714','13033447715');"
        DButils.delete(app.DB_MEMBER, sql3)
        logging.info("delete sq2 = {}".format(sql3))
        sql4 = "delete from mb_member WHERE phone in ('13033447711','13033447712','13033447713','13033447714','13033447715');"
        DButils.delete(app.DB_MEMBER, sql4)
        logging.info("delete sq2 = {}".format(sql4))

    def test01_register_success(self):
        # ����ͼƬ��֤��
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # ���������֤��
        response = self.login_api.getSmsCode(self.session, self.phone, self.imVerifyCode)
        logging.info("sms verify response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "���ŷ��ͳɹ�")
        # ����ע������
        response = self.login_api.register(self.session, self.phone, 'test123')
        logging.info("reg response={}".format(response.json()))
        # ����
        assert_utils(self, response, 200, 200, "ע��ɹ�")

    def test02_login_success(self):
        """��¼�ɹ�"""
        # ���͵�¼����
        response = self.login_api.login(self.session, self.phone, 'test123')
        logging.info("login response={}".format(response.json()))
        # ����
        assert_utils(self, response, 200, 200, "��¼�ɹ�")

    def test03_trust_success(self):
        """����"""
        # ��ȡ������Ϣ
        response = self.trust_api.trust_register(self.session)
        logging.info("trust response={}".format(response.json()))
        # ���Ի�ȡ�Ŀ�����Ϣ�Ƿ���ȷ
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # ��ȡ������Ϣ��Ӧ�е�HTML���ݣ�Ϊ��������ĵ�ַ�Ͳ�����
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # ���͵���������������������ӿڽ��п���
        response = request_third_api(form_data)
        logging.info("third-interface response={}".format(response.text))
        # ���Ե������ӿ��������Ƿ�ɹ�
        self.assertEqual('UserRegister OK', response.text)

    def test04_recharge_success(self):
        """��ֵ"""
        # ��ȡ��ֵ��֤��
        r = random.random()
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        logging.info("get_recharge_code response={}".format(response.text))

        # ��ֵ
        amount = '1000'
        response = self.trust_api.recharge(self.session, amount)
        logging.info("recharge response={}".format(response.text))
        # ���Ի�ȡ�Ŀ�����Ϣ�Ƿ���ȷ
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # ��ȡ������Ϣ��Ӧ�е�HTML���ݣ�Ϊ��������ĵ�ַ�Ͳ�����
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # ���͵���������������������ӿڽ��п���
        response = request_third_api(form_data)
        logging.info("third-interface response={}".format(response.text))
        # ���Ե������ӿ��������Ƿ�ɹ�
        self.assertEqual('NetSave OK', response.text)

    def test05_get_loaninfo(self):
        """��ȡͶ�ʲ�Ʒ����"""
        # ����Ͷ�ʲ�Ʒ������
        response = self.tender_api.get_loaninfo(self.session, self.tender_id)
        logging.info("get_tender response = {}".format(response.json()))
        # ����Ͷ�������Ƿ���ȷ
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual('697', response.json().get("data").get("loan_info").get("id"))

    def test06_tender(self):
        # Ͷ��
        # ����Ͷ������
        amount = '100'
        response = self.tender_api.tender(self.session, self.tender_id, amount)
        logging.info("tender response = {}".format(response.json()))
        # ����Ͷ�ʽ���Ƿ���ȷ
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # ��ȡ������Ϣ��Ӧ�е�HTML���ݣ�Ϊ��������ĵ�ַ�Ͳ�����
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # ���͵���������������������ӿڽ��п���
        response = request_third_api(form_data)
        logging.info("third-interface response={}".format(response.text))
        # ���Ե������ӿ��������Ƿ�ɹ�
        self.assertEqual('InitiativeTender OK', response.text)

    def test07_get_tenderlist(self):
        """��ȡ�ҵ�Ͷ���б�"""
        status = "tender"
        # ���ͻ�ȡͶ���б������
        response = self.tender_api.get_tenderlist(self.session, status)
        logging.info("get_tender response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
