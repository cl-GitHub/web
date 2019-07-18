# coding:utf-8
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from common.log import Log
import urllib.parse
import time


class LogEventListener(AbstractEventListener):
    def __init__(self):
        self.log = Log()

    def before_navigate_to(self, url, driver):
        self.log.info('\033[0;32m 前往新页面前URL:%s' % urllib.parse.unquote(driver.current_url, encoding="utf-8"))

    def after_navigate_to(self, url, driver):
        self.log.info('\033[0;32m 前往新页面后URL:%s' % urllib.parse.unquote(driver.current_url, encoding="utf-8"))

    def before_navigate_back(self, driver):
        pass

    def after_navigate_back(self, driver):
        pass

    def before_navigate_forward(self, driver):
        pass

    def after_navigate_forward(self, driver):
        pass

    def before_find(self, by, value, driver):
        time.sleep(5)
        # self.log.info('\033[0;32m before_find:{by:%s},{value:%s},{url:%s}' % (by, value, urllib.parse.unquote(driver.current_url, encoding="utf-8")))

    def after_find(self, by, value, driver):
        time.sleep(5)
        # self.log.info('\033[0;32m before_find:{by:%s},{value:%s},{url:%s}' % (by, value, urllib.parse.unquote(driver.current_url, encoding="utf-8")))

    def before_click(self, element, driver):
        self.log.info('\033[0;32m 点击元素文本:%s,跳转前页面:%s' % (
            element.text, urllib.parse.unquote(driver.current_url, encoding="utf-8")))

    def after_click(self, element, driver):
        time.sleep(5)
        self.log.info('\033[0;32m 跳转后页面:%s' % urllib.parse.unquote(driver.current_url, encoding="utf-8"))

    def before_change_value_of(self, element, driver):
        self.log.info('\033[0;32m 改变前元素文本:%s' % element.text)

    def after_change_value_of(self, element, driver):
        time.sleep(1)
        self.log.info('\033[0;32m 改变后元素文本:%s' % element.text)

    def before_execute_script(self, script, driver):
        pass

    def after_execute_script(self, script, driver):
        pass

    def before_close(self, driver):
        pass

    def after_close(self, driver):
        pass

    def before_quit(self, driver):
        pass

    def after_quit(self, driver):
        pass

    def on_exception(self, exception, driver):
        pass
