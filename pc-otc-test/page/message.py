from common.base import BasePage
from common.base import browser
from page.login_page import LoginPage, login_url
import time
from selenium.common.exceptions import TimeoutException

'''消息通知'''


class MessagePage(BasePage):
    message_loc = ("class name", "ivu-icon-md-notifications-outline")  # 消息图标
    all_mes_loc = ("class name", "see-all-tips")  # 查看全部消息按钮
    exits_loc = ("xpath", "//*[@id='app']/div/div/div[1]/div/div[3]/div[1]/div[2]/ul/div/span[2]")  # 全部标记已读按钮
    all_mes_text = ("xpath", "/html/body/div[3]/main/div/div/div")  # 全部消息内容
    message_text = ("xpath", "//*[@id='app']/main/div/div/div/ul/li[1]/div/p")  # 消息内容
    message_time = ("xpath", "//*[@id='app']/main/div/div/div/ul/li[1]/div/span")  # 消息时间

    def click_drop_down(self):
        self.click(self.all_mes_loc)

    def click_messages(self):
        self.move_mouse(self.message_loc)

    # 获取全部消息
    def get_allmessage_text(self):
        t = self.get_text(self.all_mes_text)
        return t

    # 全部标记已读
    def exits_message(self):
        self.is_exists(self.exits_loc)

    def __init__(self, driver):
        super().__init__(driver)

    # 获取通知
    # def get_message(self, count):
    #     list = []
    #     for i in range(1, count):
    #         message_text = self.get_allmessage_text()
    #         if message_text == "暂无数据":
    #             print("暂无数据")
    #             break
    #         else:
    #             pass
    #         message = self.get_message_text()
    #         date_time = self.message_data()
    #         list.append("第%s个邮件:" % i)
    #         list.append("邮件内容:%s" % message)
    #         list.append("邮件时间:%s" % date_time)
    #     return list


if __name__ == "__main__":
    driver = browser()
    message_driver = MessagePage(driver)
    driver.maximize_window()
    login_driver = LoginPage(driver)
    login_driver.user_login(LoginPage(driver), 'test01@qq.com', 'a63081244')
    message_driver.click_messages()
    flag = message_driver.is_exists(message_driver.exits_loc)
    try:
        if flag:
            message_driver.click(message_driver.exits_loc)
            print("消息通知：有未读消息，全部标记为已读")
        else:
            print(u"消息通知：暂无未读消息")
    except Exception as msg:
        print("跳转失败：%s" % msg)
        raise TimeoutException
    finally:
        message_driver.click_drop_down()
        time.sleep(2)
        t = message_driver.get_allmessage_text()
        print("查看全部通知:\n%s" % t)
    driver.quit()
