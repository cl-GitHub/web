# coding:utf-8
from common.base import BasePage
from selenium import webdriver
import time

register_url = "http://wex.test.tigerft.com/register"

'''注册页面'''
class RegisterPage(BasePage):
    email_loc = ("css selector", "[type='text']") # 邮箱
    psw_loc = ("css selector", "[type='password']") # 密码
    sure_psw_loc = ("xpath", "//*[@id='app']/main/div/div/div/form/div[3]/div/div/input") # 确认密码
    nickname_loc = ("xpath","//*[@id='app']/main/div/div/div/form/div[4]/div/div/input") # 昵称
    yaoqing_loc = ("xpath", "//*[@id='app']/main/div/div/div/form/div[5]/div/div/input")  # 邀请码
    register_loc = ("class name","ivu-btn-primary") #注册
    email_tip = ("xpath","//*[@id='app']/main/div/div/div/form/div[1]/div/div[2]") # 邮箱错误提示语
    psw_tip = ("xpath","//*[@id='app']/main/div/div/div/form/div[2]/div/div[2]") # 密码错误提示语
    sure_psw_tip = ("xpath","//*[@id='app']/main/div/div/div/form/div[3]/div/div[2]") # 确认密码错误提示语
    nickname_tip = ("xpath","//*[@id='app']/main/div/div/div/form/div[4]/div/div[2]") # 昵称被占用提示语
    yaoqing_tip = ("xpath","//*[@id='app']/main/div/div/div/form/div[5]/div/div[2]") # 邀请码有误提示语
    tou_loc = ("class name","ivu-checkbox-input") # 勾选按钮
    tou_tip = ("xpath","//*[@id='app']/main/div/div/div/form/div[6]/div/div") # 请勾选同意使用条款以完成注册
    sucess_loc = ("xpath","//*[@id='app']/main/div/div/p") # 注册成功提示语

    def register(self, email, psw, sure_psw, nickname, yaoqing,is_click = True):
        if is_click:
            self.input_email_name(email)
            self.input_psw(psw)
            self.input_sure_psw(sure_psw)
            self.input_nickname(nickname)
            self.input_yaoqing(yaoqing)
            self.click(self.register_loc)
        else:
            self.input_email_name(email)
            self.input_psw(psw)
            self.input_sure_psw(sure_psw)
            self.input_nickname(nickname)
            self.input_yaoqing(yaoqing)
            self.click(self.tou_loc)
            self.click(self.register_loc)

    def input_email_name(self, text):
        self.send_keys(self.email_loc, text, is_clear=True)


    def input_psw(self, text):
        self.send_keys(self.psw_loc, text, is_clear=True)

    def input_sure_psw(self, text):
        self.send_keys(self.sure_psw_loc, text, is_clear=True)

    def input_nickname(self, text):
        self.send_keys(self.nickname_loc, text, is_clear=True)

    def input_yaoqing(self, text):
        self.send_keys(self.yaoqing_loc, text, is_clear=True)

    def click_register(self):
        self.click(self.register_loc)


    def get_tip(self,loctor):
        result = self.is_text_in_element(loctor,text="")
        return result
    def register_scuess(self):
        text = self.get_text(self.sucess_loc)
        return text



if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    register_driver = RegisterPage(driver)
    register_driver.open(register_url)
    register_driver.register(email='test05@qq.com',psw='a1234567',sure_psw='a1234567',nickname='usd1',yaoqing="")
    time.sleep(5)
    try:
        t = register_driver.register_scuess()

        print("注册成功：%s" % t)
    except:
        print(u"注册失败")
    driver.quit()








