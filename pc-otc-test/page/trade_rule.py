from common.base import BasePage
from selenium import webdriver
from common.base import browser
from selenium.common.exceptions import NoSuchWindowException

import time
url = "http://wex.test.tigerft.com/tradingrules"

'''交易规则'''
class TradeRulespage(BasePage):

    rules_loc = ("class name","about-info")
    rules_tip = ("xpath","//*[@id='app']/main/div/div")


    def elements(self):
        elements = self.find_elements(self.rules_loc)
        return elements


    def js(self):
        self.js_scroll_end()

    def get_tip(self):
        t = self.get_text(self.rules_tip)
        return t

if __name__ == "__main__":
    driver = browser()
    tarde_rule_driver = TradeRulespage(driver)
    driver.maximize_window()
    from page.login_page import LoginPage
    LoginPage(driver).user_login(LoginPage(driver), 'test01@qq.com', 'a63081244')
    time.sleep(3)
    tarde_rule_driver.js()
    tarde_rule_driver.elements()[2].click()
    time.sleep(3)
    login_windows = driver.current_window_handle
    all_handles = driver.window_handles
    for handle in all_handles:
        if handle != login_windows:
            driver.close()
            driver.switch_to_window(handle)
            try:
                text = tarde_rule_driver.get_tip()
                print(text)
                if "Trading Rules" in text:
                    print('\033[32;0m%s' % "测试通过")
                else:
                    print('\033[32;0m%s' % "测试失败")
            except NoSuchWindowException as msg:
                print(u"查找元素异常:%s" % msg)
            else:
                driver.quit()


