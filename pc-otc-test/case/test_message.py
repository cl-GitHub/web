# coding:utf-8
from selenium.common.exceptions import TimeoutException
from page.message import MessagePage
from page.login_page import LoginPage
from common.base import set_options
from common.log import Log
import unittest
import time


class Message(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = set_options(True)
        cls.driver.maximize_window()
        cls.login_driver = LoginPage(cls.driver)
        cls.message_driver = MessagePage(cls.driver)
        cls.log = Log()

    def test_message(self):
        self.log.info("测试消息通知")
        self.login_driver.user_login(self.login_driver,'test01@qq.com','a63081244')
        self.message_driver.click_messages()
        flag = self.message_driver.is_exists(self.message_driver.exits_loc)
        try:
            if flag:
                self.message_driver.click(self.message_driver.exits_loc)
                self.log.info("消息通知：有未读消息，全部标记为已读")
            else:
                self.log.info(u"消息通知：暂无未读消息")
        except Exception as msg:
            self.login.info("跳转失败：%s" % msg)
            raise TimeoutException
        finally:
            self.message_driver.click_drop_down()
            time.sleep(2)
            t = self.message_driver.get_allmessage_text()
            self.log.info(str("查看全部通知:\n%s" % t))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
