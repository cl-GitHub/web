# coding:utf-8
import os
from common.excelutil import Excel
from common.opmysql import MysqlPool
import unittest
import ddt
from common.base import set_options
from page.myorders import MyOrdersPage, my_order_url
from page.login_page import LoginPage, login_url
from common.log import Log
import time
import random
from selenium.common.exceptions import NoSuchWindowException
import urllib.parse

"""
初始化数据表 查询订单条件数据表
"""
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
excelPath = os.path.join(os.path.join(project_dir, 'data'), "login.xlsx")
myOrdersSheetName = "商家订单查询条件数据表"
my_orders_excel = Excel(excelPath)
my_orders_data = my_orders_excel.get_list(myOrdersSheetName, False)


@ddt.ddt
class TestMyOrders(unittest.TestCase):
    """测试用户订单"""

    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.login_driver = LoginPage(cls.driver)
        cls.login_driver.open(login_url)
        cls.login_driver.user_login(cls.login_driver, "lifq_user26@qq.com", "ab1234567")
        cls.my_orders_driver = MyOrdersPage(cls.driver)
        cls.log = Log()
        try:
            cls.my_orders_mysql = MysqlPool("mysql")
            cls.get_member_id_sql = "select member_id from member.tm_member_identity where IDENTITY = %s;"
            cls.member_id = cls.my_orders_mysql.getOne(cls.get_member_id_sql, ("lifq_user26@qq.com",))
        except Exception as e:
            cls.log.info("setUP数据库错误:{}".format(repr(e)))

    def test_default_orders_info(self):
        """校验用户订单页面的默认数据"""
        self.my_orders_driver.open(my_order_url)
        try:
            get_orders_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID != %s order by ID DESC limit 0,20;"
            orders_info_list = self.my_orders_mysql.getAll(get_orders_info_sql, (
                self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id']))
        except Exception as e:
            self.log.info("default数据库错误:{}".format(repr(e)))
        # 获取页面数据
        my_order_list = self.my_orders_driver.find_elements(self.my_orders_driver.div_orders)
        for my_order_list_position in range(len(my_order_list)):
            # 页面数据，类型：列表
            my_order_web_info = my_order_list[my_order_list_position].text.split('\n')
            # 数据库数据，类型：字典
            my_order_sql_info = orders_info_list[my_order_list_position]
            self.log.info("索引:{}".format(my_order_list_position))
            self.log.info("数据库广告:{}\n页面广告:{}".format(my_order_sql_info,
                                                     my_order_web_info))
            self.my_orders_driver.check_data(my_order_web_info, my_order_sql_info)
        time.sleep(10)

    @ddt.data(*my_orders_data)
    def test_condition_orders_info(self, data):
        """校验用户订单页面的筛选数据"""
        self.my_orders_driver.open(my_order_url)
        # select_sql = ''
        orders_info_list = []
        try:
            if data['Type'] == 'Buy':
                if data['Status'] == 'Progressing':
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID != %s and SIDE =2 and TARGET_COIN=%s and STANDARD_COIN=%s and STATE in (10,20,30) order by ID DESC limit 0,20;"
                    orders_info_list = self.my_orders_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                        data['Fiat'], data['Crypto']))
                elif data['Status'] == 'Canceled':
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID != %s and SIDE =2 and TARGET_COIN=%s and STANDARD_COIN=%s and STATE = 90 order by ID DESC limit 0,20;"
                    orders_info_list = self.my_orders_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                        data['Fiat'], data['Crypto']))
                else:
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID != %s and SIDE =2 and TARGET_COIN=%s and STANDARD_COIN=%s and STATE in (40,50) order by ID DESC limit 0,20;"
                    orders_info_list = self.my_orders_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                        data['Fiat'], data['Crypto']))
            elif data['Type'] == 'Sell':
                if data['Status'] == 'Progressing':
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID != %s and SIDE =1 and TARGET_COIN=%s and STANDARD_COIN=%s and STATE in (10,20,30) order by ID DESC limit 0,20;"
                    orders_info_list = self.my_orders_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                        data['Fiat'], data['Crypto']))
                elif data['Status'] == 'Canceled':
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID != %s and SIDE =1 and TARGET_COIN=%s and STANDARD_COIN=%s and STATE = 90 order by ID DESC limit 0,20;"
                    orders_info_list = self.my_orders_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                        data['Fiat'], data['Crypto']))
                else:
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID != %s and SIDE =1 and TARGET_COIN=%s and STANDARD_COIN=%s and STATE in (40,50) order by ID DESC limit 0,20;"
                    orders_info_list = self.my_orders_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                        data['Fiat'], data['Crypto']))
        except Exception as e:
            self.log.info("condition数据库错误:{}".format(repr(e)))
        if data['Type'] == 'Buy':
            self.my_orders_driver.click(self.my_orders_driver.span_buy)
        elif data['Type'] == 'Sell':
            self.my_orders_driver.click(self.my_orders_driver.span_sell)
        time.sleep(1)
        if data['Status'] == 'Progressing':
            self.my_orders_driver.click(self.my_orders_driver.span_progressing)
        elif data['Status'] == 'Completed':
            self.my_orders_driver.click(self.my_orders_driver.span_completed)
        elif data['Status'] == 'Canceled':
            self.my_orders_driver.click(self.my_orders_driver.span_canceled)
        time.sleep(1)
        if data['Crypto'] == 'USDT':
            self.my_orders_driver.click(self.my_orders_driver.span__usdt)
        elif data['Crypto'] == 'USDC':
            self.my_orders_driver.click(self.my_orders_driver.span__usdc)
        elif data['Crypto'] == 'TUSD':
            self.my_orders_driver.click(self.my_orders_driver.span__tusd)
        time.sleep(1)
        if data['Fiat'] == 'HKD':
            self.my_orders_driver.click(self.my_orders_driver.span__hkd)
        elif data['Fiat'] == 'TWD':
            self.my_orders_driver.click(self.my_orders_driver.span__twd)
        elif data['Fiat'] == 'USD':
            self.my_orders_driver.click(self.my_orders_driver.span__usd)
        elif data['Fiat'] == 'IDR':
            self.my_orders_driver.click(self.my_orders_driver.span__idr)
        elif data['Fiat'] == 'VND':
            self.my_orders_driver.click(self.my_orders_driver.span__vnd)
        elif data['Fiat'] == 'KHR':
            self.my_orders_driver.click(self.my_orders_driver.span__khr)
        time.sleep(1)
        self.my_orders_driver.click(self.my_orders_driver.button_search)
        time.sleep(1)
        if orders_info_list:
            self.log.info(orders_info_list)
            # 获取页面数据
            my_order_list = self.my_orders_driver.find_elements(self.my_orders_driver.div_orders)
            for my_order_list_position in range(len(my_order_list)):
                # 页面数据，类型：列表
                my_order_web_info = my_order_list[my_order_list_position].text.split('\n')
                # 数据库数据，类型：字典
                my_order_sql_info = orders_info_list[my_order_list_position]
                self.log.info("索引:{}".format(my_order_list_position))
                self.log.info("数据库广告:{}\n页面广告:{}".format(my_order_sql_info,
                                                         my_order_web_info))
                self.my_orders_driver.check_data(my_order_web_info, my_order_sql_info)
        else:
            assert self.my_orders_driver.get_text(self.my_orders_driver.div_no_records) in (
                '暂无数据', 'No Records.', '暫無數據')

    def test_my_order_no_success_info(self):
        """随机获取订单编号筛选订单测试"""
        self.my_orders_driver.open(my_order_url)
        try:
            select_id_sql = "select ID from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and ADVERTISER_MEMBER_ID != %s"
            orders_id_list = self.my_orders_mysql.getAll(select_id_sql,
                                                         (self.member_id['member_id'], self.member_id['member_id'],
                                                          self.member_id['member_id']))
            self.log.info("orders_id_list:{}".format(orders_id_list))
            # 随机获取一条订单ID
            orders_id_position = random.randint(0, len(orders_id_list) - 1)
            self.log.info("orders_id_position{}".format(orders_id_position))
            select_order_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and ADVERTISER_MEMBER_ID != %s and ID = %s;"
            orders_info = self.my_orders_mysql.getOne(select_order_info_sql,
                                                      (self.member_id['member_id'], self.member_id['member_id'],
                                                       self.member_id['member_id'],
                                                       orders_id_list[orders_id_position]['ID']))
            self.log.info("orders_info:{}".format(orders_info))
        except Exception as e:
            self.log.info("数据库错误:{}".format(repr(e)))
        self.my_orders_driver.send_keys(self.my_orders_driver.input_order_no,
                                        orders_id_list[orders_id_position]['ID'])
        time.sleep(1)
        self.log.info("ID:{}".format(orders_id_list[orders_id_position]['ID']))
        self.my_orders_driver.click(self.my_orders_driver.button_search)
        # 获取页面数据
        my_order_list = self.my_orders_driver.find_elements(self.my_orders_driver.div_orders)
        # 页面数据，类型：列表
        my_order_web_info = my_order_list[0].text.split('\n')
        self.log.info(my_order_web_info)
        self.my_orders_driver.check_data(my_order_web_info, orders_info)

    def test_my_order_no_fail_info(self):
        """错误订单编号筛选订单测试"""
        self.my_orders_driver.open(my_order_url)
        self.my_orders_driver.send_keys(self.my_orders_driver.input_order_no, '1')
        time.sleep(1)
        self.my_orders_driver.click(self.my_orders_driver.button_search)
        assert self.my_orders_driver.get_text(self.my_orders_driver.div_no_records) in (
            '暂无数据', 'No Records.', '暫無數據'), self.my_orders_driver.get_text(
            self.my_orders_driver.div_no_records)

    def test_reset(self):
        """测试重置按钮功能"""
        self.my_orders_driver.open(my_order_url)
        self.my_orders_driver.click(self.my_orders_driver.span_buy)
        time.sleep(1)
        self.my_orders_driver.click(self.my_orders_driver.span_completed)
        time.sleep(1)
        self.my_orders_driver.click(self.my_orders_driver.span__usdt)
        time.sleep(1)
        self.my_orders_driver.click(self.my_orders_driver.span__hkd)
        time.sleep(1)
        self.my_orders_driver.click(self.my_orders_driver.button_reset)
        assert self.my_orders_driver.get_attribute(self.my_orders_driver.span_all_type, "class") == 'active'
        assert self.my_orders_driver.get_attribute(self.my_orders_driver.span_all_status,
                                                   "class") == 'active'
        assert self.my_orders_driver.get_attribute(self.my_orders_driver.span_all_crypto,
                                                   "class") == 'active'
        assert self.my_orders_driver.get_attribute(self.my_orders_driver.span_all_fiat, "class") == 'active'
        # 获取数据库数据
        orders_info_list = []
        try:
            get_orders_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID!=%s order by ID DESC limit 0,20;"
            orders_info_list = self.my_orders_mysql.getAll(get_orders_info_sql, (
                self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id']))
        except Exception as e:
            self.log.info(e)
        # 获取页面数据
        my_order_list = self.my_orders_driver.find_elements(self.my_orders_driver.div_orders)
        for my_order_list_position in range(len(my_order_list)):
            # 页面数据，类型：列表
            my_order_web_info = my_order_list[my_order_list_position].text.split('\n')
            # 数据库数据，类型：字典
            my_order_sql_info = orders_info_list[my_order_list_position]
            self.log.info("索引:{}".format(my_order_list_position))
            self.log.info("数据库广告:{}\n页面广告:{}".format(my_order_sql_info,
                                                     my_order_web_info))
            self.my_orders_driver.check_data(my_order_web_info, my_order_sql_info)
        time.sleep(1)

    def test_my_orders_click_next_page_success(self):
        """测试点击下一页|上一页功能"""
        # 登陆成功后跳转到广告列表页面
        self.my_orders_driver.open(my_order_url)
        # 设置页面锚点为底端
        self.my_orders_driver.js_scroll_end()
        # 获得所有分页的数量
        elements = self.my_orders_driver.find_elements(self.my_orders_driver.li_page_item)
        page_account = int(elements[len(elements) - 1].text)
        self.log.info("页码数量为:{}".format(page_account))
        # 获得上一页按钮
        prev_element = self.my_orders_driver.find_element(self.my_orders_driver.li_page_prev)
        # 获得下一页按钮
        next_element = self.my_orders_driver.find_element(self.my_orders_driver.li_page_next)
        # 获得不可点击按钮
        disabled_element = self.my_orders_driver.find_elements(self.my_orders_driver.li_page_disabled)
        if page_account == 1:
            assert prev_element in disabled_element, "上一页不是不可点击标签"
            assert next_element in disabled_element, "下一页不是不可点击标签"
        else:
            for page_position in range(page_account - 1):
                next_element.click()
                assert self.my_orders_driver.find_element(
                    self.my_orders_driver.li_page_item_active).text == str(
                    page_position + 2), "当前选中标签为:{},页码应为:{}".format(
                    self.my_orders_driver.find_element(self.my_orders_driver.li_page_item_active).text,
                    page_position + 2)
            # 判断不可点击按钮是否为下一页
            assert next_element in self.my_orders_driver.find_elements(
                self.my_orders_driver.li_page_disabled), "下一页不是不可点击标签"
            for page_position in range(page_account - 1)[::-1]:
                prev_element.click()
                assert self.my_orders_driver.find_element(
                    self.my_orders_driver.li_page_item_active).text == str(
                    page_position + 1), "当前选中标签为:{},页码应为:{}".format(
                    self.my_orders_driver.find_element(self.my_orders_driver.li_page_item_active).text,
                    page_position + 1)
            # 判断不可点击按钮是否为上一页
            assert prev_element in self.my_orders_driver.find_elements(
                self.my_orders_driver.li_page_disabled), "上一页不是不可点击标签"

    def test_my_orders_click_page_success(self):
        """测试点击页码（第二页、第三页）功能"""
        # 登陆成功后跳转到广告列表页面
        self.my_orders_driver.open(my_order_url)
        # 设置页面锚点为底端
        self.my_orders_driver.js_scroll_end()
        # 获得所有分页的数量
        elements = self.my_orders_driver.find_elements(self.my_orders_driver.li_page_item)
        page_account = int(elements[len(elements) - 1].text)
        self.log.info("页码数量为:{}".format(page_account))
        # 获得上一页按钮
        prev_element = self.my_orders_driver.find_element(self.my_orders_driver.li_page_prev)
        # 获得下一页按钮
        next_element = self.my_orders_driver.find_element(self.my_orders_driver.li_page_next)
        # 获得不可点击按钮
        disabled_element = self.my_orders_driver.find_elements(self.my_orders_driver.li_page_disabled)
        orders_info_list = []
        if page_account == 1:
            assert prev_element in disabled_element, "上一页不是不可点击标签"
            assert next_element in disabled_element, "下一页不是不可点击标签"
        else:
            # 点击页码二
            elements[1].click()
            # 获取数据库数据
            try:
                select_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and ADVERTISER_MEMBER_ID != %s order by ID DESC limit %s,%s"
                orders_info_list = self.my_orders_mysql.getAll(select_info_sql, (
                    self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                    20, 40))
                self.log.info("orders_info_list:{}".format(orders_info_list))
            except Exception as e:
                self.log.info("数据库异常:{}".format(e))
            # 获取页面数据
            my_order_list = self.my_orders_driver.find_elements(self.my_orders_driver.div_orders)
            for my_order_list_position in range(len(my_order_list)):
                # 页面数据，类型：列表
                my_order_web_info = my_order_list[my_order_list_position].text.split('\n')
                # 数据库数据，类型：字典
                my_order_sql_info = orders_info_list[my_order_list_position]
                self.log.info("索引:{}".format(my_order_list_position))
                self.log.info("数据库广告:{}\n页面广告:{}".format(my_order_sql_info,
                                                         my_order_web_info))
                self.my_orders_driver.check_data(my_order_web_info, my_order_sql_info)
            # 校验数据

    def test_my_orders_detail(self):
        """查看订单详情测试"""
        # 登陆成功后跳转到广告列表页面
        self.my_orders_driver.open(my_order_url)
        # 获取页面数据
        my_order_elements = self.my_orders_driver.find_elements(self.my_orders_driver.div_orders)
        # 随机获取任一订单
        detail__order_element_position = random.randint(0, len(my_order_elements) - 1)
        # 获取数据库数据
        orders_info_list = []
        try:
            get_orders_info_sql = "select ID,SIDE,CREATE_TIME,ADVERT_ID,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID!=%s order by ID DESC limit 0,20;"
            orders_info_list = self.my_orders_mysql.getAll(get_orders_info_sql, (
                self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id']))
        except Exception as e:
            self.log.info(e)
        my_order_web_info = my_order_elements[detail__order_element_position].text.split('\n')
        my_order_sql_info = orders_info_list[detail__order_element_position]
        self.log.info("数据库广告:{}\n页面广告:{}".format(my_order_sql_info,
                                                 my_order_web_info))
        # 获取所有查看按钮
        my_order_detail_elements = self.my_orders_driver.find_elements(
            self.my_orders_driver.span_detail)
        # 获取随机订单的查看按钮并点击
        # webelement模块中可以获取到子元素获取订单详情span元素下的a标签
        my_order_detail_elements[detail__order_element_position].find_element_by_link_text('Detail').click()
        # 断言跳转页面URL是否正确(订单、状态）
        self.log.info(self.driver.current_url)
        assert str(my_order_sql_info['ID']) in self.driver.current_url, "数据库订单ID:{},页面URL:{}".format(
            my_order_sql_info['ID'], self.driver.current_url)
        if my_order_sql_info['SIDE'] == 1:
            assert "sell" in self.driver.current_url, "数据库订单方向:1,页面URL:{}".format(
                my_order_sql_info['ID'], self.driver.current_url)
        elif my_order_sql_info['SIDE'] == 2:
            assert "buy" in self.driver.current_url, "数据库订单方向:2,页面URL:{}".format(
                my_order_sql_info['ID'], self.driver.current_url)
        assert str(my_order_sql_info[
                       'ADVERT_ID']) in self.driver.current_url, "数据库广告ID:{},页面URL:{}".format(
            my_order_sql_info['ADVERT_ID'], self.driver.current_url)

    def test_merchant_info(self):
        """测试商家详情跳转功能"""
        # 登陆成功后跳转到广告列表页面
        self.my_orders_driver.open(my_order_url)
        # 获取页面数据
        my_order_elements = self.my_orders_driver.find_elements(self.my_orders_driver.div_orders)
        # 随机获取任一订单
        detail__order_element_position = random.randint(0, len(my_order_elements) - 1)
        # 获取所有广告主按钮
        my_order_detail_elements = self.my_orders_driver.find_elements(self.my_orders_driver.a_advert)
        # 获取广告主的名称
        advert_username = my_order_detail_elements[detail__order_element_position].text
        self.log.info('\033[32;0m%s' % advert_username)
        # 获得当前页面句柄
        my_order_windows = self.driver.current_window_handle
        # 点击广告主名称
        my_order_detail_elements[detail__order_element_position].click()
        # 跳转到打开的新页面
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != my_order_windows:
                self.driver.close()
                self.driver.switch_to.window(handle)
                try:
                    text = urllib.parse.unquote(self.driver.current_url, encoding="utf-8")
                    if advert_username in text:
                        self.log.info('\033[0;32m%s' % "测试通过")
                    else:
                        self.log.info('\033[1;31m%s' % "测试失败")
                except NoSuchWindowException as msg:
                    self.log.info(u"查找元素异常:%s" % msg)
                else:
                    self.driver.quit()

    def test_my_appointment(self):
        """测试跳转大额预约界面功能"""
        # 登陆成功后跳转到广告列表页面
        self.my_orders_driver.open(my_order_url)
        # 获取查看我的预约按钮并点击
        self.my_orders_driver.find_element(self.my_orders_driver.span_check_my_reservation).click()
        # 获取跳转后的url并断言
        text = urllib.parse.unquote(self.driver.current_url, encoding="utf-8")
        if 'business/order-list/my-appointment' in text:
            self.log.info('\033[0;32m%s' % "测试通过")
        else:
            self.log.info('\033[1;31m%s' % "测试失败")

    @classmethod
    def tearDownClass(cls):
        cls.my_orders_mysql.dispose()
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
