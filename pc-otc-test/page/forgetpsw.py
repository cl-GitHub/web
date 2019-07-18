# coding:utf-8
from common.base import BasePage
from selenium import webdriver
from common.base import browser
import time

find_url = "http://wex.test.tigerft.com/user/find_pwd/"


class FindPage(BasePage):
    """找回密码页面"""
    # 找回密码
    find_loc = ("xpath", "//*[@id='app']/main/div/div/h1")
    # 重置成功密码界面title
    find_resetting = ("xpath", '//*[@id="app"]/main/div/div/div')
    # 电子邮箱文本输入框
    email_address = ("xpath", "//*[@id='app']/main/div/div/div/div/div/form/div[1]/div/div[1]/input")
    # 获取验证码
    button_get_verification_code = ("xpath", '//*[@id="app"]/main/div/div/div/div/div/form/div[2]/div/div/div/div')
    # 验证码文本输入框
    verification = ("xpath", '//*[@id="app"]/main/div/div/div/div/div/form/div[2]/div/div[1]/input')
    # 重置
    button_resetting = ("xpath", '//*[@id="app"]/main/div/div/div/button')
    # vue弹窗提示组件-失败
    vue_alert = ("class name", "ivu-message-error")
    # 邮箱错误提示文本
    error_email_address_tips = ("xpath", '//*[@id="app"]/main/div/div/div/div/div/form/div[1]/div/div[2]')
    # 验证码错误提示文本
    error_verification_tips = ("xpath", '//*[@id="app"]/main/div/div/div/div/div/form/div[2]/div/div[2]')

    def get_find_text(self, locator):
        t = self.get_text(locator)
        return t

    def input_email_address(self, text):
        self.send_keys(self.email_address, text)

    def input_verification(self, text):
        self.send_keys(self.verification, text)

    def click_button_get_verfication_code(self):
        self.click(self.button_get_verification_code)

    def click_button_button_resetting(self):
        self.click(self.button_resetting)

    def find_password(self, find_password_driver, email_address, verification, isClick = True):
        """忘记密码"""
        if isClick:
            find_password_driver.open(find_url)
            self.input_email_address(email_address)
            self.input_verification(verification)
            self.click_button_button_resetting()
        else:
            find_password_driver.open(find_url)
            self.input_email_address(email_address)
            self.input_verification(verification)


if __name__ == "__main__":
    driver = browser()
    find_driver = FindPage(driver)
    find_driver.open(find_url)
    t = find_driver.get_find_text()
    print(t)
    driver.quit()
