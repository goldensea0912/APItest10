import logging
import unittest
import requests

from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from utils import assert_utils


class approve(unittest.TestCase):
    phone1 = '13033447711'
    phone2 = '13033447712'
    realname = '����'
    cardId = '110117199003070995'

    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.approve_api = approveAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # ��֤�ɹ�
    def test01_approve_success(self):
        # 1���û���¼
        response = self.login_api.login(self.session)
        logging.info('login response = {}'.format(response.json()))
        assert_utils(self, response, 200, 200, "��¼�ɹ�")
        # 2��������֤����
        # ׼������
        # ���ýӿڽű��ж���ķ�����������
        response = self.approve_api.approve(self.session, self.realname, self.cardId)
        # �Խ�����ж���
        assert_utils(self, response, 200, 200, "�ύ�ɹ�!")

    # ��֤ʧ�ܡ�������Ϊ��
    def test02_approve_realname_is_null(self):
        # 1���û���¼
        response = self.login_api.login(self.session, self.phone2)
        logging.info('login response = {}'.format(response.json()))
        assert_utils(self, response, 200, 200, "��¼�ɹ�")
        # 2��������֤���� _ ����Ϊ��
        # ׼������
        # ���ýӿڽű��ж���ķ�����������
        response = self.approve_api.approve(self.session, "", self.cardId)
        logging.info('approve response = {}'.format(response.json()))
        # �Խ�����ж���
        assert_utils(self, response, 200, 100, "��������Ϊ��")

    # ��֤ʧ�ܡ������֤��Ϊ��
    def test03_approve_cardId_is_null(self):
        # 1���û���¼
        response = self.login_api.login(self.session, self.phone2)
        logging.info('login response = {}'.format(response.json()))
        assert_utils(self, response, 200, 200, "��¼�ɹ�")
        # 2��������֤���� _ ����Ϊ��
        # ׼������
        # ���ýӿڽű��ж���ķ�����������
        response = self.approve_api.approve(self.session, self.realname, "")
        logging.info('approve response = {}'.format(response.json()))
        # �Խ�����ж���
        assert_utils(self, response, 200, 100, "���֤�Ų���Ϊ��")

    # ��ȡ��֤��Ϣ
    def test04_get_approve(self):
        # 1���û���¼
        response = self.login_api.login(self.session, self.phone1)
        logging.info('login response = {}'.format(response.json()))
        assert_utils(self, response, 200, 200, "��¼�ɹ�")
        # 2����ȡ��֤����
        response = self.approve_api.getApprove(self.session)
        logging.info('approve response = {}'.format(response.json()))
        # �Խ�����ж���
        self.assertEqual(200, response.status_code)
