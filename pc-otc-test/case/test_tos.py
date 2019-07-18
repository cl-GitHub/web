# coding:utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from page.login_page import LoginPage
from page.tos import TOSpage
from common.base import set_options
from common.log import Log
import unittest
import time
'''服务条款'''
class TestTos(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.driver = set_options(False)
            cls.driver.maximize_window()
            cls.login_driver = LoginPage(cls.driver)
            cls.log = Log()
            cls.tos_driver = TOSpage(cls.driver)

        def test_tos(self):
            self.login_driver.user_login(self.login_driver,'test01@qq.com','a63081244')
            time.sleep(5)
            self.tos_driver.js()
            self.tos_driver.elements()[1].click()
            time.sleep(5)
            about_windows = self.driver.current_window_handle
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != about_windows:
                    self.driver.close()
                    self.driver.switch_to_window(handle)
                    try:
                        text = self.tos_driver.get_tip()
                        self.log.info("打印文本:%s" % text)
                        if "Terms and Conditions" in text:
                            self.log.info('\033[32;0m%s' % "测试通过")
                        else:
                            self.log.info('\033[32;0m%s' % "测试失败")
                    except NoSuchWindowException as msg:
                        self.log.info(u"查找元素异常:%s" % msg)
                    else:
                        self.driver.quit()
        @classmethod
        def tearDownClass(cls):
            cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
