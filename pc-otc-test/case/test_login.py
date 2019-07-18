# coding:utf-8

from page.login_page import LoginPage, login_url
from page.forgetpsw import FindPage
from common.log import Log
import unittest
import time
import ddt
from common.excelutil import Excel
import os
from common.base import set_options

"""
初始化EXCEL数据
"""

project_dir = os.path.dirname(os.path.abspath('.'))
excelPath = project_dir + '/pc-otc-test/data/login.xlsx'
"""如果测试单个test"""
# excelPath = project_dir + '/data/login.xlsx'
loginSuccessSheetName = "登陆成功数据表"
loginFailSheetName = "登陆失败数据表"
login_excel = Excel(excelPath)
login_success_data = login_excel.get_list(loginSuccessSheetName)
login_fail_data = login_excel.get_list(loginFailSheetName)


@ddt.ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.login_driver = LoginPage(cls.driver)
        cls.login_driver.open(login_url)
        cls.log = Log()
        cls.find_driver = FindPage(cls.driver)

    def setUp(self):
        self.login_driver.open(login_url)

    @ddt.data(*login_success_data)
    def test_login_success(self, data):
        """登录正确用户名密码"""
        self.log.info("---开始测试正确的用户名密码---")
        self.login_driver.user_login(self.login_driver, data['username'], data['password'])
        time.sleep(5)
        self.log.info("获取返回结果")
        result = self.login_driver.is_text_in_element(
            self.login_driver.nickname, data['except'])
        self.log.info("判断结果是否与预期一致:%s" % result)
        self.assertTrue(result)
        if result:
            self.log.info(u"打印:登录成功")
        else:
            self.log.info(u"打印:登录失败")
            self.login_driver.get_screenasbase64()
        self.driver.refresh()

    @ddt.data(*login_fail_data)
    def test_login_fail(self, data):
        """输入错误的用户名密码"""
        self.log.info("---开始测试错误的用户名密码---")
        self.datatype = data['datatype']
        if self.datatype == 'alert':
            self.log.info("测试数据(用户名:{},密码:{},断言:{})".format(data['username'], data['password'], data['except']))
            self.login_driver.user_login(self.login_driver, data['username'], data['password'])
            result = self.login_driver.get_text(self.login_driver.vue_alert)
            print(result)
            try:
                assert data['except'] in result
                print('Test Pass')
            except Exception as e:
                print('Test Fail.', format(e))
            time.sleep(5)
        elif self.datatype == 'user_text':
            self.log.info("测试数据(用户名:{},密码:{},断言:{})".format(data['username'], data['password'], data['except']))
            self.login_driver.user_login(self.login_driver, data['username'], data['password'])
            result = self.login_driver.is_text_in_element(
                self.login_driver.username_tips, data['except']
            )
            self.assertTrue(result)
            time.sleep(5)
            if result:
                self.log.info(u"打印:测试成功")
            else:
                self.log.info(u"打印:测试失败")
        elif self.datatype == 'pwd_text':
            self.log.info("测试数据(用户名:{},密码:{},断言:{})".format(data['username'], data['password'], data['except']))
            self.login_driver.user_login(self.login_driver, data['username'], data['password'])
            result = self.login_driver.is_text_in_element(
                self.login_driver.password_tips, data['except']
            )
            self.assertTrue(result)
            time.sleep(5)
            if result:
                self.log.info(u"打印:测试成功")
            else:
                self.log.info(u"打印:测试失败")

    def test_forget_password(self):
        """忘记密码"""
        self.log.info("---测试开始---")
        self.log.info("第1步：点击‘忘记密码’按钮")
        self.login_driver.click_find()
        self.log.info("第2步：获取页面文本“找回您的密码”")
        t = self.find_driver.get_find_text(self.find_driver.find_loc)
        self.log.info("打印结果：%s" % t)
        self.assertTrue(t == "找回您的密码")
        self.log.info("判断结果是否与预期一致:%s" % t)
        self.log.warning("---pass---")

    def test_sign_up(self):
        """快速注册"""
        self.log.info("---测试开始---")
        self.log.info("第1步：点击‘快速注册’按钮")
        self.login_driver.click_sign_up_button()
        self.log.info("第2步：获取页面文本“注册”")
        t = self.find_driver.get_find_text(self.find_driver.find_loc)
        self.log.info("打印结果：%s" % t)
        self.assertTrue(t == "立即注册成为viaUSD用户")
        self.log.info("判断结果是否与预期一致:%s" % t)
        self.log.warning("---pass---")

    def test_loginout(self):
        self.log.info("测试退出按钮")
        self.log.info("登录账号")
        self.login_driver.user_login(self.login_driver,'test01@qq.com','a63081244')
        time.sleep(2)
        self.login_driver.click_drop_up()
        time.sleep(2)
        self.log.info("点击退出按钮")
        self.login_driver.elements()[2].click()
        self.driver.implicitly_wait(20)
        result = self.login_driver.get_login_text()
        try:
            self.assertEqual("Log in",result)
            self.log.info("退出成功")
        except Exception as e:
            print("退出失败:%s" % e)

    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.refresh()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
