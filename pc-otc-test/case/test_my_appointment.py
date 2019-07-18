# coding:utf-8
from common.opmysql import MysqlPool
import unittest
from common.base import set_options
from page.myappointment import MyAppointmentPage, my_appointment_url
from page.login_page import LoginPage, login_url
from common.log import Log
import time
from selenium.common.exceptions import NoSuchWindowException
import urllib.parse


class TestMyAppointment(unittest.TestCase):
    """测试大额预约"""

    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.login_driver = LoginPage(cls.driver)
        cls.login_driver.open(login_url)
        cls.login_driver.user_login(cls.login_driver, "lifq_user26@qq.com", "ab1234567")
        cls.my_appointment_driver = MyAppointmentPage(cls.driver)
        cls.log = Log()
        try:
            cls.my_appointment_mysql = MysqlPool("mysql")
            cls.get_member_id_sql = "select member_id from member.tm_member_identity where IDENTITY = %s;"
            cls.member_id = cls.my_appointment_mysql.getOne(cls.get_member_id_sql, ("lifq_user26@qq.com",))
        except Exception as e:
            cls.log.info("setUP数据库错误:{}".format(repr(e)))

    def test_my_appointment_info(self):
        """校验用户大额订单数据"""
        self.my_appointment_driver.open(my_appointment_url)
        try:
            get_appointment_info_sql = "select ID, CREATE_TIME,OFFLINE_VOLUME,OFFLINE_COIN,STATE from otc.tb_otc_appointment where USER_ID =%s order by ID DESC limit 0,10;"
            appointment_info_list = self.my_appointment_mysql.getAll(get_appointment_info_sql,
                                                                     self.member_id['member_id'])
        except Exception as e:
            self.log.info("default数据库错误:{}".format(repr(e)))
        # 获取页面数据
        my_appointment_list = self.my_appointment_driver.find_elements(self.my_appointment_driver.div_order)
        for my_appointment_list_position in range(len(my_appointment_list)):
            # 页面数据，类型：列表
            my_appoint_web_info = my_appointment_list[my_appointment_list_position].text.split('\n')
            # 数据库数据，类型：字典
            my_appoint_sql_info = appointment_info_list[my_appointment_list_position]
            self.log.info("索引:{}".format(my_appointment_list_position))
            self.log.info("数据库广告:{}\n页面广告:{}".format(my_appoint_sql_info,
                                                     my_appoint_web_info))
            self.my_appointment_driver.check_data(my_appoint_web_info, my_appoint_sql_info)
        time.sleep(10)

    def test_details(self):
        """测试查看详情功能"""
        self.my_appointment_driver.open(my_appointment_url)
        try:
            get_appointment_info_sql = "select ID,STATE,ORDER_ID from otc.tb_otc_appointment where USER_ID =%s order by ID DESC limit 0,10;"
            appointment_info_list = self.my_appointment_mysql.getAll(get_appointment_info_sql,
                                                                     self.member_id['member_id'])
        except Exception as e:
            self.log.info("default数据库错误:{}".format(repr(e)))
        # 随机获得一条进行中的订单,即state in (10,20,30,40)
        # 获取页面数据
        my_appointment_list = self.my_appointment_driver.find_elements(self.my_appointment_driver.div_order)
        # # 获取所有操作按钮
        my_appointment_details = self.my_appointment_driver.find_elements(self.my_appointment_driver.div_detail)
        for my_appointment_list_position in range(len(my_appointment_list)):
            # 页面数据，类型：列表
            my_appoint_web_info = my_appointment_list[my_appointment_list_position].text.split('\n')
            # 数据库数据，类型：字典
            my_appoint_sql_info = appointment_info_list[my_appointment_list_position]
            # 获得当前页面句柄
            my_appointment_windows = self.driver.current_window_handle
            if len(my_appoint_web_info) > 4:
                my_appointment_details[my_appointment_list_position].click()
                time.sleep(5)
                # 获取预期URL
                appointment_url = ''
                if my_appoint_sql_info['STATE'] in (10, 20, 30):
                    appointment_url = 'http://wex.test.tigerft.com/market/appointment/' + str(my_appoint_sql_info['ID'])
                    pass
                elif my_appoint_sql_info['STATE'] == 40:
                    appointment_url = 'http://wex.test.tigerft.com/market/buy/detail/1/' + str(
                        my_appoint_sql_info['ORDER_ID'])
                # 跳转到打开的新页面
                all_handles = self.driver.window_handles
                for handle in all_handles:
                    if handle != my_appointment_windows:
                        self.driver.switch_to.window(handle)
                        time.sleep(3)
                        try:
                            text = urllib.parse.unquote(self.driver.current_url, encoding="utf-8")
                            self.log.info("跳转后的链接2:{}".format(text))
                            if appointment_url == text:
                                self.log.info('\033[0;32m%s' % "测试通过")
                            else:
                                self.log.info('\033[1;31m%s' % "测试失败")
                        except NoSuchWindowException as msg:
                            self.log.info(u"查找元素异常:%s" % msg)
                        self.driver.close()
                        time.sleep(3)
                        self.driver.switch_to.window(my_appointment_windows)
                        time.sleep(3)
            time.sleep(5)

    time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        cls.my_appointment_mysql.dispose()
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
