from common.base import BasePage
from selenium import webdriver
from common.base import browser
from selenium.common.exceptions import NoSuchWindowException

import time
url = "http://wex.test.tigerft.com/"

'''费率说明'''
class feespage(BasePage):

    fees_button = ("class name","about-info")
    fees_loc = ("xpath","//*[@id='app']/main/div/div")

    def elements(self):
        elements = self.find_elements(self.fees_button)
        return elements

    def js(self):
        self.js_scroll_end()

    def get_tip(self):
        t = self.get_text(self.fees_loc)
        return t



