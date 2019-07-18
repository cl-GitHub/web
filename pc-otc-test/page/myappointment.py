# coding:utf-8
my_appointment_url = "http://wex.test.tigerft.com/business/order-list/my-appointment"
from common.base import BasePage
from common.base import browser
from common.logeventlistener import LogEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
import re


class MyAppointmentPage(BasePage):
    """大额预约页面"""
    # 订单列表
    div_order = ("class name", 'item')
    # 操作按钮
    div_detail = ("class name", 'operate')

    @staticmethod
    def check_data(my_appoint_web_info, my_appoint_sql_info):
        """数据校验
        :param my_appoint_web_info:页面数据
        :type my_appoint_web_info:list
        :param my_appoint_sql_info:数据库数据
        :type my_appoint_sql_info:dict
        """
        # 判断订单创建日期
        assert str(my_appoint_sql_info['CREATE_TIME']) in my_appoint_web_info[0]
        # 判断交易法币数量
        # 获取页面法币数量
        web_currency_amount = MyAppointmentPage.get_amount(re.sub('[a-zA-Z]', '', my_appoint_web_info[1]))
        # 获取数据库法币数量
        sql_currency_amount = MyAppointmentPage.get_float(my_appoint_sql_info['OFFLINE_VOLUME'], 2)
        # 获取数据库法币单位
        sql_currency_type = my_appoint_sql_info['OFFLINE_COIN']
        assert web_currency_amount == sql_currency_amount
        assert sql_currency_type in my_appoint_web_info[1]
        # 判断订单状态
        if my_appoint_sql_info['STATE'] in (10, 20, 30):
            assert my_appoint_web_info[3] in ('Reserveing', '预约中')
        elif my_appoint_sql_info['STATE'] in (40, 50):
            assert my_appoint_web_info[3] in ('Completed', '预约成功')
        elif my_appoint_sql_info['STATE'] == 90:
            assert my_appoint_web_info[3] in ('Canceled', '已取消')

    @staticmethod
    def get_float(f_str, n):
        """计算精度
        :param f_str:截取精度的数字
        :param n:精度长度
        """
        f_str = str(f_str)  # f_str = '{}'.format(f_str) 也可以转换为字符串
        a, b, c = f_str.partition('.')
        c = (c + "0" * n)[:n]  # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
        return ".".join([a, c])

    @staticmethod
    def get_amount(amount):
        """去除数量中的千分位"""
        return amount.replace(",", "")

    def __init__(self, driver):
        super().__init__(EventFiringWebDriver(driver, LogEventListener()))
