# coding:utf-8
from common.base import BasePage
from selenium import webdriver
import time

login_url = "http://wex.test.tigerft.com/login?fromPage=login"
# 加载配置项
options = webdriver.ChromeOptions()
options.add_argument('--disable-infobars')
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)


class LoginPage(BasePage):
    user_loc = ("css selector", "[type='text']")
    psw_loc = ("css selector", "[type='password']")
    button_loc = ("class name", "login-action")
    viausd_loc = ("xpath", "//*[@id='app']/div/div/div[1]/div/div[1]/img")
    # 获取提示语
    tip_loc = ("xpath", "//*[@id='root']/div/div/section/section/header/div/div/div/span")
    # 用户名提示语
    username_tips = ("xpath", "//*[@id='app']/main/div/div/div[2]/form/div[1]/div/div[2]")
    # 密码提示语
    password_tips = ("xpath", "//*[@id='app']/main/div/div/div[2]/form/div[2]/div/div[2]")
    # 忘记密码
    find_loc = ("xpath", "//*[@id='app']/main/div/div/div[2]/div/span[2]/a")
    # 昵称
    nickname = ("xpath", "//*[@id='app']/div/div/div[1]/div/div[3]/div[2]/div[1]")
    # vue弹窗提示组件
    vue_alert = ("class name", "ivu-message-error")
    # 快速注册
    button_sign_up = ("xpath", "//*[@id='app']/main/div/div/div[2]/div/span[1]/a")
    # 商家中心
    merchant_center = ("xpath", '//*[@id="app"]/div/div/div[1]/div/div[3]/div[3]/div[1]/div')

    # 二级菜单
    ul_merchant_center = ("xpath", '//*[@id="app"]/div/div/div[1]/div/div[3]/div[3]/div[2]/ul')

    # 发布广告
    li_post_an_offer = ("xpath", '//*[@id="app"]/div/div/div[1]/div/div[3]/div[3]/div[2]/ul/li[1]')

    # 订单管理
    li_order_center = ("xpath", '//*[@id="app"]/div/div/div[1]/div/div[3]/div[3]/div[2]/ul/li[2]')
    # 广告管理
    li_my_offers = ("xpath", '//*[@id="app"]/div/div/div[1]/div/div[3]/div[3]/div[2]/ul/li[3]')

    drop_up = ("class name", "margin-right-15")  # 一级菜单
    drop_down = ("class name", "ivu-dropdown-item")  # 二级菜单
    login_loc = ("class name", "layout-regist")  # 登录按钮

    def click_drop_down(self):
        self.click(self.drop_down)

    def click_drop_up(self):
        self.move_mouse(self.drop_up)

    def get_login_text(self):
        t = self.get_text(self.login_loc)
        return t

    def elements(self):
        elements = self.find_elements(self.drop_down)
        return elements

    def __init__(self, driver):
        super().__init__(driver)

    def input_username(self, text):
        self.send_keys(self.user_loc, text, is_clear=True)

    def input_psw(self, text):
        self.send_keys(self.psw_loc, text, is_clear=True)

    def click_login_button(self):
        self.click(self.button_loc)

    def click_sign_up_button(self):
        self.click(self.button_sign_up)

    '''获取用户昵称'''

    def get_nickname(self):
        result = self.get_text(self.nickname)
        return result

    def click_find(self):
        self.click(self.find_loc)

    def get_tip(self):
        t = self.get_text(self.tip_loc)
        return t

    def click_usd(self):
        self.click(self.viausd_loc)

    def user_login(self, logindriver, username, password):
        """登陆"""
        logindriver.open(login_url)
        self.input_username(username)
        self.input_psw(password)
        logindriver.click_login_button()
        logindriver.click_usd()

    def user_logout(self, login_driver):
        login_driver.click_drop_up()
        time.sleep(2)
        login_driver.elements()[2].click()
        time.sleep(2)
        result_text = login_driver.get_login_text()
        try:
            assert "登录" in result_text
            print("退出成功")
        except Exception as e:
            print("退出失败:%s" % e)

    # 点击商家中心-发布广告
    def user_login_click_post_an_offer(self, logindriver):
        logindriver.click_ul_li(self.merchant_center, self.ul_merchant_center, self.li_post_an_offer)

    # 点击商家中心-广告管理
    def user_login_click_my_offers(self, logindriver):
        logindriver.click_ul_li(self.merchant_center, self.ul_merchant_center, self.li_my_offers)

    # 点击商家中心-订单管理
    def user_login_click_order_center(self, logindriver):
        logindriver.click_ul_li(self.merchant_center, self.ul_merchant_center, self.li_order_center)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    login_driver = LoginPage(driver)
    login_driver.user_login(login_driver, 'test01@qq.com', 'a63081244')
    time.sleep(5)
    result = login_driver.get_nickname()
    print("获取到账户名称：%s" % result)
    except_result = True
    if except_result:
        print(u"登录成功")
    else:
        print(u"登录失败")
    time.sleep(3)
    login_driver.click_drop_up()
    time.sleep(2)
    login_driver.elements()[2].click()
    driver.implicitly_wait(20)
    result = login_driver.get_login_text()
    try:
        assert "登录" in result
        print("退出成功")
    except Exception as e:
        print("退出失败:%s" % e)

driver.quit()
