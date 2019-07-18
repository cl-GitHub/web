from common.base import BasePage
from selenium import webdriver
from common.base import browser
from selenium.common.exceptions import NoSuchWindowException

import time

url = "http://wex.test.tigerft.com/"


class FAQpage(BasePage):
    faq_loc = ("xpath", "//*[@id='app']/main/footer/div[1]/div[2]/div[1]/a[1]")
    about_loc = ("xpath", "//*[@id='app']/main/div/div/div")

    def elements(self):
        elements = self.find_elements(self.faq_loc_loc)
        return elements

    def js(self):
        self.js_scroll_end()

    def get_tip(self):
        t = self.get_text(self.about_loc)
        return t


if __name__ == "__main__":
    driver = browser()
    FAQ_driver = FAQpage(driver)
    driver.maximize_window()
    from page.login_page import LoginPage
    LoginPage(driver).user_login(LoginPage(driver), 'test01@qq.com', 'a63081244')
    time.sleep(3)
    FAQ_driver.js()
    FAQ_driver.elements()[0].click()
    time.sleep(3)
    about_windows = driver.current_window_handle
    all_handles = driver.window_handles
    for handle in all_handles:
        if handle != about_windows:
            driver.close()
            driver.switch_to_window(handle)
            try:
                text = FAQ_driver.get_tip()
                print(text)
            except NoSuchWindowException as msg:
                print(u"查找元素异常:%s" % msg)
            else:
                driver.quit()
