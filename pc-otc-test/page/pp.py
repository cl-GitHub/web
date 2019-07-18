from common.base import BasePage
from selenium import webdriver
from common.base import browser
from selenium.common.exceptions import NoSuchWindowException

import time
url = "http://wex.test.tigerft.com/pp"

'''隐私政策'''
class PPpage(BasePage):

    pp_loc = ("class name","about-info")
    pp_tip = ("xpath","//*[@id='app']/main/div/div/h1")

    def elements(self):
        elements = self.find_elements(self.pp_loc)
        return elements



    def js(self):
        self.js_scroll_end()

    def get_tip(self):
        t = self.get_text(self.pp_tip)
        return t



