from common.base import BasePage
from common.base import browser
from page.login_page import LoginPage
import time


'''个人中心'''

url = "http://wex.test.tigerft.com/new-user/"
class PersonalPage(BasePage):
    drop_up = ("class name", "margin-right-15")  # 一级菜单
    drop_down = ("class name", "ivu-dropdown-item")  # 二级菜单
    nickname = ("class name","c-title") #账户昵称
    account = ("class name","c-gray") # 账号
    last_login = ("xpath","//*[@id='app']/main/div/div/div[1]/div[1]/div[2]/span") #上次登录
    account_register =("xpath","//*[@id='app']/main/div/div/div[1]/div[1]/div[3]/span") # 账户注册于
    phone = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[1]/div[1]/span") # 手机
    mail = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[1]/div[3]/span") # 邮箱
    sec_verification = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[1]/div[5]/span") # 二次验证
    login_pwd = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[1]/div[7]/span") # 登录密码
    certification = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[2]/div[3]/div[2]/button/span") # 实名认证
    Advanced = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[2]/div[3]/span") # 进阶认证
    t1 = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[2]/div[1]/span") # 认证状态
    t2 = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[2]/div[3]/div[2]/button")
    bank_account = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[3]/ul/li/span[2]") # 银行账号
    bank_account2 = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[3]/ul/li[2]/span[2]")
    new_account = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[3]/ul/li[1]/span[2]")

    # 我的钱包
    wallet = ("class name","list-flag")
    balance = ("class name","two")
    available_balance = ("class name","three")
    blocked_balances = ("class name","four")

    # 商家中心
    order_center = ("xpath","//*[@id='app']/main/div/div/div[1]/div[2]/div/a[1]/div/span")
    adv_loc = ("xpath","//*[@id='app']/main/div/div/div[1]/div[2]/div/a[2]/div/span")

    # 我的消息
    message = ("class name","message-list")

    # 邀请返利
    Number_of_invitations = ("xpath","//*[@id='app']/main/div/div/div/div[1]/div/div[3]/div[2]/div[1]/h4")
    commission = ("xpath","//*[@id='app']/main/div/div/div/div[1]/div/div[3]/div[2]/div[3]/h4")


    # 添加银行账号
    add = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[3]/div/div/span")
    location = ("class name","ivu-select-placeholder")
    bank_country = ("class name","ivu-select-item")
    bank_card = ("xpath","//*[@id='app']/main/div/div/div/div/div/form/div[4]/div/div/input")
    bank = ("xpath","//*[@id='app']/main/div/div/div/div/div/form/div[5]/div/div/input")
    bank_branch = ("xpath","//*[@id='app']/main/div/div/div/div/div/form/div[6]/div/div/input")
    add_button = ("class name","ivu-btn-primary")
    add_edit = ("xpath","/html/body/div[8]/div[2]/div/div/div/div/div[3]/button[2]")

    #删除银行账号
    delete = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[3]/ul/li/div/button/span")
    new_delete = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[3]/ul/li[1]/div/button")
    delete2 = ("xpath","//*[@id='app']/main/div/div/div[2]/div/div[3]/ul/li[2]/div/button")
    delete_fail = ("xpath","/html/body/div[8]/div/div/div[1]/div/span")
    delete_sucess = ("xpath","/html/body/div[8]/div[2]/div/div/div/div/div[2]/div")
    delete_edit = ("xpath","/html/body/div[8]/div[2]/div/div/div/div/div[3]/button")

    # 修改昵称
    edit = ("xpath","//*[@id='app']/main/div/div/div[1]/div[1]/div[1]/div[3]/img")
    username = ("xpath","//*[@id='app']/main/div/div/div/div/div/form/div/div/div/input")
    submit = ("xpath","//*[@id='app']/main/div/div/div/div/div/button[1]")
    success_tip = ("xpath", "/html/body/div[4]/div[2]/div/div/div[2]/div")
    fail_text = ("class name", "ivu-form-item-error-tip")
    define = ("class name","ivu-btn-small")
    go_blck = ("xpath","//*[@id='app']/main/div/div/div/div/div/button[2]")


    def elements(self):
        elements = self.find_elements(self.drop_down)
        return elements

    def click_drop_down(self):
        self.elements()[0].click()

    def click_personal(self):
        self.click_mouse(self.drop_up)

# 账户信息
    def get_accountinfo(self):
        list = []
        nickname = self.get_text(self.nickname)
        account = self.get_text(self.account)
        last_login = self.get_text(self.last_login)
        account_regiseter = self.get_text(self.account_register)
        list.append("昵称:%s" % nickname)
        list.append("账号：%s" % account)
        list.append("上次登录：%s" % last_login)
        list.append("账户注册于：%s" % account_regiseter)
        return list


# 修改账户昵称
    def edit_nickname(self, name):
        list = []
        old_nickname = self.get_text(self.nickname)
        list.append("修改前的昵称:%s" % old_nickname)
        self.click(self.edit)
        time.sleep(2)
        self.send_keys(self.username, name, is_clear=True)
        if name != old_nickname:
            try:
                self.click(self.submit)
                time.sleep(5)
                text = self.get_text(self.success_tip)
                list.append("提示:%s" % text)
                self.click(self.define)
                time.sleep(5)
                new_nickname = self.get_text(self.nickname)
                list.append("修改后的昵称：%s" % new_nickname)
            except:
                fail_text = self.get_text(self.fail_text)
                list.append("修改昵称失败;%s" % fail_text)
        elif name == old_nickname:
            print("昵称未做任何修改")
        else:
            text = self.get_text(self.fail_text)
            list.append("修改昵称失败：%s" % text)
        return list

    # 我的钱包
    def get_my_wallet(self,currency):
        list = []
        # 去除target属性
        js = 'document.getElementsByClassName("list-flag")[0].target="";'
        driver.execute_script(js)
        driver.find_element_by_link_text("我的钱包").click()
        time.sleep(2)
        if currency == "USDT":
            balance_button = self.find_elements(self.balance)
            available_balance_button = self.find_elements(self.available_balance)
            blocked_balances_button = self.find_elements(self.blocked_balances)
            blocked_balances = blocked_balances_button[1].text
            available_balance = available_balance_button[1].text
            balance = balance_button[1].text
            list.append("USDT余额:%s" % balance)
            list.append("USDT可用余额：%s" % available_balance)
            list.append("USDT托管余额：%s" % blocked_balances)
            print(list)
        elif currency == "USDC":
            balance_button = self.find_elements(self.balance)
            available_balance_button = self.find_elements(self.available_balance)
            blocked_balances_button = self.find_elements(self.blocked_balances)
            blocked_balances = blocked_balances_button[2].text
            available_balance = available_balance_button[2].text
            balance = balance_button[2].text
            list.append("USDC余额:%s" % balance)
            list.append("USDC可用余额：%s" % available_balance)
            list.append("USDC托管余额：%s" % blocked_balances)
            print(list)
        elif currency == "TUSD":
            balance_button = self.find_elements(self.balance)
            available_balance_button = self.find_elements(self.available_balance)
            blocked_balances_button = self.find_elements(self.blocked_balances)
            blocked_balances = blocked_balances_button[3].text
            available_balance = available_balance_button[3].text
            balance = balance_button[3].text
            list.append("TUSD余额:%s" % balance)
            list.append("TUSD可用余额：%s" % available_balance)
            list.append("TUSD托管余额：%s" % blocked_balances)
            print(list)
        else:
            print("没有该币种")
        return list


# 点击订单管理
    def click_order(self):
        js = 'document.getElementsByClassName("list-flag")[1].target="";'
        driver.execute_script(js)
        driver.find_element_by_link_text("订单管理").click()
        time.sleep(2)


# 点击我的消息
    def get_my_message(self):
        list = []
        js = 'document.getElementsByClassName("list-flag")[2].target="";'
        driver.execute_script(js)
        driver.find_element_by_link_text("我的消息").click()
        time.sleep(2)
        message = self.get_text(self.message)
        list.append("全部通知：{}".format(message))
        return list



# 点击邀请返利
    def get_Invitation_rebate(self):
        list = []
        js = 'document.getElementsByClassName("list-flag")[3].target="";'
        driver.execute_script(js)
        driver.find_element_by_link_text("邀请返利").click()
        time.sleep(2)
        number_invitations = self.get_text(self.Number_of_invitations)
        commussion = self.get_text(self.commission)
        list.append("邀请人数：%s/人" % number_invitations)
        list.append("获得佣金：%s/USDT" % commussion)
        return list



# 商家中心
    def get_business_center(self):
        list = []
        order_center = self.get_text(self.order_center)
        adv = self.get_text(self.adv_loc)
        list.append("订单中心：%s" %order_center)
        list.append("广告管理：%s" % adv)
        return list


# 账户安全
    def get_account_security(self):
        list = []
        phone = self.get_text(self.phone)
        mail = self.get_text(self.mail)
        sec_verification = self.get_text(self.sec_verification)
        login_pwd = self.get_text(self.login_pwd)
        list.append("手机:%s" % phone)
        list.append("邮箱:%s" % mail)
        list.append("二次验证:%s" % sec_verification)
        list.append("登录密码:%s" % login_pwd)
        return list


# 身份认证
    def get_identity(self):
        list = []
        certification = self.get_text(self.certification)
        t1 = self.get_text(self.t1)
        Advanced = self.get_text(self.Advanced)
        t2 = self.get_text(self.t2)
        list.append("实名认证:{}:{}" .format(t1, certification))
        list.append("进阶认证:{}:{}".format(t2, Advanced))
        return list


# 收款账户
    def get_Payment_account(self):
        list= []
        bank_account = self.get_text(self.bank_account)
        list.append("收款账户：%s"% bank_account)
        return list


# 添加银行账户
    def add_bank_account(self,bank_card,bank,bank_branch):
        list = []
        self.click(self.add)
        self.click(self.location)
        time.sleep(2)
        self.bank_country = self.find_elements(self.bank_country) # 国家
        self.bank_country[2].click() #取第三个国家
        self.send_keys(self.bank_card,bank_card,is_clear=False)
        self.send_keys(self.bank,bank,is_clear=False)
        self.send_keys(self.bank_branch,bank_branch,is_clear=False)
        self.click(self.add_button)
        time.sleep(2)
        self.click(self.add_edit)
        time.sleep(5)
        new_bank = self.get_text(self.new_account)
        try:
            assert bank in new_bank
            list.append("添加银行卡成功：%s" % new_bank)
        except:
            list.append("添加失败")
        return list


# 删除银行账号
    def delete_bank_account(self):
        list = []
        delete = self.find_elements(self.delete)
        print(len(delete))
        # 可能存在多个删除按钮/或无
        if len(delete) == 1:
            self.click(self.delete)
            result_fail = self.get_text(self.delete_fail)
            try:
               assert "支付方式正在使用" in result_fail
               list.append("删除失败：%s"% result_fail)
            except:
                list.append("删除成功")
        elif len(delete) == 2:
            old_bank = self.get_text(self.bank_account2)
            old_bank2 = self.get_text(self.new_account)
            delete[0].click()
            time.sleep(2)
            result_success = self.get_text(self.delete_sucess)
            print(result_success)
            try:
               assert "删除支付方式成功" in result_success
               list.append(result_success)
               self.click(self.delete_edit)
               bank_account = self.get_text(self.bank_account)
               print(list.append("删除前的银行账号:%s:%s" % (old_bank, old_bank2)))
               print("删除后的银行卡账户：%s" % bank_account)
            except:
                list.append("删除失败")
        else:
            list.append("没有可删除的银行账号")
        return list


if __name__ == "__main__":
    driver = browser()
    personal_driver = PersonalPage(driver)
    driver.maximize_window()
    login_driver = LoginPage(driver)
    login_driver.user_login(login_driver,"test01@qq.com",'a63081244')
    personal_driver.click_personal()
    time.sleep(3)
    personal_driver.click_drop_down()
    time.sleep(3)
    # list = PersonalPage.get_accountinfo(personal_driver)
    # print(list)
    list1 = PersonalPage.edit_nickname(personal_driver,'BTC1')
    print(list1)
    # list = PersonalPage.delete_bank_account(personal_driver)
    # print(list)
    # list = PersonalPage.add_bank_account(personal_driver,454454654564654,"建设银行","建设支行")
    # print(list)
    # list = PersonalPage.get_business_center(personal_driver)
    # print(list)
    # # PersonalPage.get_my_wallet(personal_driver,"TUSD")
    # PersonalPage.is_element_exist(personal_driver)
    # list = PersonalPage.get_Invitation_rebate(personal_driver)
    # print(list)
    # list = PersonalPage.get_my_message(personal_driver)
    # print(list)


