# coding:utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from page.login_page import LoginPage
from page.fees import feespage
from common.base import set_options
from common.log import Log
import unittest
import time
'''费率说明'''
class feesTos(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.driver = set_options(False)
            cls.driver.maximize_window()
            cls.login_driver = LoginPage(cls.driver)
            cls.log = Log()
            cls.fees_driver = feespage(cls.driver)

        def test_fees(self):
            self.login_driver.user_login(self.login_driver,'test01@qq.com','a63081244')
            time.sleep(5)
            self.fees_driver.js()
            self.fees_driver.elements()[4].click()
            time.sleep(5)
            about_windows = self.driver.current_window_handle
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != about_windows:
                    self.driver.close()
                    self.driver.switch_to_window(handle)
                    try:
                        text = self.fees_driver.get_tip()
                        self.log.info("打印文本:%s" % text)
                        except_text = True
                        if except_text:
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
