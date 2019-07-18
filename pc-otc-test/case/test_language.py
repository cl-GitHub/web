# coding:utf-8
from page.set_language import set_languagePage,URL
from common.base import set_options
from common.log import Log
import unittest


class test_language(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.maximize_window()
        cls.log = Log()
        cls.language_driver = set_languagePage(cls.driver)
        cls.language_driver.open(URL)


    def test_01(self):
        self.log.info("设置语言为：简体中文")
        self.language_driver.select_luanguage("简体中文")

    def test_02(self):
        self.log.info("设置语言为：繁體中文")
        self.language_driver.select_luanguage("繁體中文")

    def test_03(self):
        self.log.info("设置语言为：English")
        self.language_driver.select_luanguage("English")

    def tearDown(self):
        self.driver.delete_all_cookies()
        self.driver.refresh()




    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
   unittest.main()
