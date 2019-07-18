# coding:utf-8
from page.personal import PersonalPage,url
from page.login_page import LoginPage
from common.base import set_options
from common.log import Log
import unittest
import time
import os


class TestPersonal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = set_options(False)
        cls.driver.maximize_window()
        cls.login_driver = LoginPage(cls.driver)
        cls.personal_driver = PersonalPage(cls.driver)
        cls.login_driver.user_login(cls.login_driver,"test01@qq.com","a63081244")
        cls.log = Log()
        cls.personal_driver.click_personal()
        time.sleep(2)
        cls.personal_driver.click_drop_down()
        time.sleep(2)


    def test_get_accountinfo(self):
        self.log.info("测试：获取账户信息")
        account_info = PersonalPage.get_accountinfo(self.personal_driver)
        self.log.info(account_info)

    def test_edit_nickname(self):
        self.log.info("测试：修改昵称")
        nickname = PersonalPage.edit_nickname(self.personal_driver,'btc')
        self.log.info(nickname)

    def test_get_my_wallet(self):
        self.log.info("测试;我的钱包")
        my_wallet = PersonalPage.get_my_wallet(self.personal_driver,"TUSD")
        self.log.info(my_wallet)

    def test_get_my_message(self):
        self.log.info("测试：获取我的消息")
        my_message = PersonalPage.get_my_message(self.personal_driver)
        self.log.info(my_message)

    def test_get_Invitation_rebate(self):
        self.log.info("测试：获取邀请返利")
        info = PersonalPage.get_Invitation_rebate(self.personal_driver)
        self.log.info(info)

    def test_get_business_center(self):
        self.log.info("测试：商家中心")
        business_center = PersonalPage.get_business_center(self.personal_driver)
        self.log.info(business_center)

    def test_get_account_security(self):
        self.log.info("测试：获取账户安全信息")
        account_security = PersonalPage.get_account_security(self.personal_driver)
        self.log.info(account_security)

    def test_get_identity(self):
        self.log.info("测试：获取身份认证信息")
        identity = PersonalPage.get_identity(self.personal_driver)
        self.log.info(identity)

    def test_get_Payment_account(self):
        self.log.info("测试：获取银行账户信息")
        payment_account = PersonalPage.get_Payment_account(self.personal_driver)
        self.log.info(payment_account)

    def test_add_bank_account(self):
        self.log.info("测试：添加银行卡")
        add_bank_account = PersonalPage.add_bank_account(self.personal_driver,454454654564654,"建设银行","建设支行")
        self.log.info(add_bank_account)

    def test_delete_bank_account(self):
        self.log.info("测试：删除银行卡")
        delete_bank_account = PersonalPage.delete_bank_account(self.personal_driver)
        self.log.info(delete_bank_account)

    def tearDown(self):
        self.driver.refresh()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    suit = unittest.TestSuite()
    suit.addTest(TestPersonal("test_get_accountinfo"))
    runner = unittest.TextTestRunner()
    runner.run(suit)
    # suit = unittest.TestSuite()
    # test_case = [TestPersonal("test_get_accountinfo"),TestPersonal("test_edit_nickname"),TestPersonal("test_get_my_wallet"),
    #             TestPersonal("test_get_my_message"),TestPersonal("test_get_Invitation_rebate"),TestPersonal("test_get_business_center")
    #              ,TestPersonal("test_get_account_security"),TestPersonal("test_get_identity"),TestPersonal("test_get_Payment_account")
    #              ,TestPersonal("test_add_bank_account"),TestPersonal("test_delete_bank_account")]
    # suit.addTests(test_case)
    # runner = unittest.TextTestRunner()
    # runner.run(suit)

