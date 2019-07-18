# coding:utf-8
import os
from common.excelutil import Excel
from common.opmysql import MysqlPool
import unittest
import ddt
from common.base import set_options
from page.merchantorders import MerchantOrdersPage, merchant_order_url
from page.login_page import LoginPage, login_url
from common.log import Log
import time
import random

"""
初始化数据表 查询订单条件数据表
"""
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
excelPath = os.path.join(os.path.join(project_dir, 'data'), "login.xlsx")
MerchantOrdersSheetName = "商家订单查询条件数据表"
merchant_orders_excel = Excel(excelPath)
merchant_orders_data = merchant_orders_excel.get_list(MerchantOrdersSheetName, False)


@ddt.ddt
class TestMerchantOrders(unittest.TestCase):
    """测试商家订单"""

    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.login_driver = LoginPage(cls.driver)
        cls.login_driver.open(login_url)
        cls.login_driver.user_login(cls.login_driver, "lifq_user26@qq.com", "ab1234567")
        cls.merchant_orders_driver = MerchantOrdersPage(cls.driver)
        cls.log = Log()
        try:
            cls.merchant_mysql = MysqlPool("mysql")
            cls.get_member_id_sql = "select member_id from member.tm_member_identity where IDENTITY = %s;"
            cls.member_id = cls.merchant_mysql.getOne(cls.get_member_id_sql, ("lifq_user26@qq.com",))
        except Exception as e:
            cls.log.info("数据库错误:{}".format(e))

    def test_default_orders_info(self):
        """校验商家订单页面的默认数据"""
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        time.sleep(5)
        try:
            get_orders_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s order by ID DESC limit 0,20;"
            orders_info_list = self.merchant_mysql.getAll(get_orders_info_sql, (
                self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id']))
        except Exception as e:
            self.log.info(e)
        # 获取页面数据
        merchant_order_list = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.div_orders)
        for merchant_order_list_position in range(len(merchant_order_list)):
            # 页面数据，类型：列表
            merchant_order_web_info = merchant_order_list[merchant_order_list_position].text.split('\n')
            # 数据库数据，类型：字典
            merchant_order_sql_info = orders_info_list[merchant_order_list_position]
            self.log.info("索引:{}".format(merchant_order_list_position))
            self.log.info("数据库广告:{}\n页面广告:{}".format(merchant_order_sql_info,
                                                     merchant_order_web_info))
            self.merchant_orders_driver.check_data(merchant_order_web_info, merchant_order_sql_info)
        time.sleep(10)

    @ddt.data(*merchant_orders_data)
    def test_condition_orders_info(self, data):
        """校验商家订单页面的筛选数据"""
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        time.sleep(5)
        orders_info_list = []
        try:
            if data['Type'] == 'Buy':
                if data['Status'] == 'Progressing':
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s and SIDE =%s and TARGET_COIN=%s and STANDARD_COIN=%s and STATE in (10,20,30) order by ID DESC limit 0,20;"
                    orders_info_list = self.merchant_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'], 1,
                        data['Fiat'], data['Crypto']))
                elif data['Status'] == 'Canceled':
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s and SIDE =%s and TARGET_COIN=%s and STANDARD_COIN=%s and STATE =90 order by ID DESC limit 0,20;"
                    orders_info_list = self.merchant_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'], 1,
                        data['Fiat'], data['Crypto']))
                else:
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s and SIDE =%s and TARGET_COIN=%s and STANDARD_COIN=%s and STATE in (40,50) order by ID DESC limit 0,20;"
                    orders_info_list = self.merchant_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'], 1,
                        data['Fiat'], data['Crypto']))
            elif data['Type'] == 'Sell':
                if data['Status'] == 'Progressing':
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s and SIDE =%s and TARGET_COIN=%s and STANDARD_COIN=%s and STATE in (10,20,30) order by ID DESC limit 0,20;"
                    orders_info_list = self.merchant_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'], 2,
                        data['Fiat'], data['Crypto']))
                elif data['Status'] == 'Canceled':
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s and SIDE =%s and TARGET_COIN=%s and STANDARD_COIN=%s and STATE = 90 order by ID DESC limit 0,20;"
                    orders_info_list = self.merchant_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'], 2,
                        data['Fiat'], data['Crypto']))
                else:
                    select_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s and SIDE =%s and TARGET_COIN=%s and STANDARD_COIN=%s and STATE in (40,50) order by ID DESC limit 0,20;"
                    orders_info_list = self.merchant_mysql.getAll(select_sql, (
                        self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'], 2,
                        data['Fiat'], data['Crypto']))
        except Exception as e:
            self.log.info(e)
        if data['Type'] == 'Buy':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span_buy)
        elif data['Type'] == 'Sell':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span_sell)
        time.sleep(1)
        if data['Status'] == 'Progressing':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span_progressing)
        elif data['Status'] == 'Completed':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span_completed)
        elif data['Status'] == 'Canceled':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span_canceled)
        time.sleep(1)
        if data['Crypto'] == 'USDT':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__usdt)
        elif data['Crypto'] == 'USDC':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__usdc)
        elif data['Crypto'] == 'TUSD':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__tusd)
        time.sleep(1)
        if data['Fiat'] == 'HKD':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__hkd)
        elif data['Fiat'] == 'TWD':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__twd)
        elif data['Fiat'] == 'USD':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__usd)
        elif data['Fiat'] == 'IDR':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__idr)
        elif data['Fiat'] == 'VND':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__vnd)
        elif data['Fiat'] == 'KHR':
            self.merchant_orders_driver.click(self.merchant_orders_driver.span__khr)
        time.sleep(1)
        self.merchant_orders_driver.click(self.merchant_orders_driver.button_search)
        time.sleep(1)
        if orders_info_list:
            self.log.info(orders_info_list)
            # 获取页面数据
            merchant_order_list = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.div_orders)
            for merchant_order_list_position in range(len(merchant_order_list)):
                # 页面数据，类型：列表
                merchant_order_web_info = merchant_order_list[merchant_order_list_position].text.split('\n')
                # 数据库数据，类型：字典
                merchant_order_sql_info = orders_info_list[merchant_order_list_position]
                self.log.info("索引:{}".format(merchant_order_list_position))
                self.log.info("数据库广告:{}\n页面广告:{}".format(merchant_order_sql_info,
                                                         merchant_order_web_info))
                self.merchant_orders_driver.check_data(merchant_order_web_info, merchant_order_sql_info)
        else:
            assert self.merchant_orders_driver.get_text(self.merchant_orders_driver.div_no_records) in (
                '暂无数据', 'No Records.', '暫無數據')

    def test_order_no_success_info(self):
        """随机获取订单编号筛选订单测试"""
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        time.sleep(5)
        try:
            select_id_sql = "select ID from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and ADVERTISER_MEMBER_ID = %s"
            orders_id_list = self.merchant_mysql.getAll(select_id_sql,
                                                        (self.member_id['member_id'], self.member_id['member_id'],
                                                         self.member_id['member_id']))
            self.log.info("orders_id_list:{}".format(orders_id_list))
            # 随机获取一条订单ID
            orders_id_position = random.randint(0, len(orders_id_list) - 1)
            select_order_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and ADVERTISER_MEMBER_ID = %s and ID = %s;"
            orders_info = self.merchant_mysql.getOne(select_order_info_sql,
                                                     (self.member_id['member_id'], self.member_id['member_id'],
                                                      self.member_id['member_id'],
                                                      orders_id_list[orders_id_position]['ID']))
            self.log.info("orders_info:{}".format(orders_info))
        except Exception as e:
            self.log.info(e)
        self.merchant_orders_driver.send_keys(self.merchant_orders_driver.input_order_no,
                                              orders_id_list[orders_id_position]['ID'])
        time.sleep(5)
        self.merchant_orders_driver.click(self.merchant_orders_driver.button_search)
        # 获取页面数据
        merchant_order_list = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.div_orders)
        # 页面数据，类型：列表
        merchant_order_web_info = merchant_order_list[0].text.split('\n')
        self.merchant_orders_driver.check_data(merchant_order_web_info, orders_info)

    def test_order_no_fail_info(self):
        """错误订单编号筛选订单测试"""
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        time.sleep(5)
        self.merchant_orders_driver.send_keys(self.merchant_orders_driver.input_order_no, '1')
        time.sleep(5)
        self.merchant_orders_driver.click(self.merchant_orders_driver.button_search)
        time.sleep(5)
        assert self.merchant_orders_driver.get_text(self.merchant_orders_driver.div_no_records) in (
            '暂无数据', 'No Records.', '暫無數據'), self.merchant_orders_driver.get_text(
            self.merchant_orders_driver.div_no_records)
        time.sleep(5)

    @unittest.skip
    def test_trade_date_info(self):
        """根据时间筛选订单测试"""
        """页面不支持输入，等待完善"""
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        time.sleep(5)
        self.merchant_orders_driver.send_keys(self.merchant_orders_driver.input_start_date, '2019-06-01')
        self.merchant_orders_driver.send_keys(self.merchant_orders_driver.input_end_date, '2019-06-30')
        time.sleep(5)
        self.merchant_orders_driver.click(self.merchant_orders_driver.button_search)
        try:
            select_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and ADVERTISER_MEMBER_ID = %s and  (CREATE_TIME between %s and %s)"
            orders_info_list = self.merchant_mysql.getAll(select_info_sql, (
                self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                '2019-06-01 {}'.format('00:00:00'),
                '2019-06-30 {}'.format('23:59:59')))
            self.log.info("orders_info_list:{}".format(orders_info_list))
            if orders_info_list:
                # 获取页面数据
                merchant_order_list = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.div_orders)
                for merchant_order_list_position in range(len(merchant_order_list)):
                    # 页面数据，类型：列表
                    merchant_order_web_info = merchant_order_list[merchant_order_list_position].text.split('\n')
                    # 数据库数据，类型：字典
                    merchant_order_sql_info = orders_info_list[merchant_order_list_position]
                    self.log.info("索引:{}".format(merchant_order_list_position))
                    self.log.info("数据库广告:{}\n页面广告:{}".format(merchant_order_sql_info,
                                                             merchant_order_web_info))
                    self.merchant_orders_driver.check_data(merchant_order_web_info, merchant_order_sql_info)
            else:
                assert self.merchant_orders_driver.get_text(self.merchant_orders_driver.div_no_records) in (
                    '暂无数据', 'No Records.', '暫無數據')
        except Exception as e:
            self.log.info("数据错误:{}".format(e))
        time.sleep(5)

    def test_reset(self):
        """测试重置按钮功能"""
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        time.sleep(5)
        self.merchant_orders_driver.click(self.merchant_orders_driver.span_buy)
        time.sleep(1)
        self.merchant_orders_driver.click(self.merchant_orders_driver.span_completed)
        time.sleep(1)
        self.merchant_orders_driver.click(self.merchant_orders_driver.span__usdt)
        time.sleep(1)
        self.merchant_orders_driver.click(self.merchant_orders_driver.span__hkd)
        time.sleep(1)
        self.merchant_orders_driver.click(self.merchant_orders_driver.button_reset)
        assert self.merchant_orders_driver.get_attribute(self.merchant_orders_driver.span_all_type, "class") == 'active'
        assert self.merchant_orders_driver.get_attribute(self.merchant_orders_driver.span_all_status,
                                                         "class") == 'active'
        assert self.merchant_orders_driver.get_attribute(self.merchant_orders_driver.span_all_crypto,
                                                         "class") == 'active'
        assert self.merchant_orders_driver.get_attribute(self.merchant_orders_driver.span_all_fiat, "class") == 'active'
        # 获取数据库数据
        try:
            get_orders_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s order by ID DESC limit 0,20;"
            orders_info_list = self.merchant_mysql.getAll(get_orders_info_sql, (
                self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id']))
        except Exception as e:
            self.log.info(e)
        # 获取页面数据
        merchant_order_list = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.div_orders)
        for merchant_order_list_position in range(len(merchant_order_list)):
            # 页面数据，类型：列表
            merchant_order_web_info = merchant_order_list[merchant_order_list_position].text.split('\n')
            # 数据库数据，类型：字典
            merchant_order_sql_info = orders_info_list[merchant_order_list_position]
            self.log.info("索引:{}".format(merchant_order_list_position))
            self.log.info("数据库广告:{}\n页面广告:{}".format(merchant_order_sql_info,
                                                     merchant_order_web_info))
            self.merchant_orders_driver.check_data(merchant_order_web_info, merchant_order_sql_info)
        time.sleep(1)

    def test_merchant_orders_click_next_page_success(self):
        """测试点击下一页|上一页功能"""
        # 登陆成功后跳转到广告列表页面
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        # 设置页面锚点为底端
        self.merchant_orders_driver.js_scroll_end()
        time.sleep(5)
        # 获得所有分页的数量
        elements = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.li_page_item)
        page_account = int(elements[len(elements) - 1].text)
        self.log.info("页码数量为:{}".format(page_account))
        # 获得上一页按钮
        prev_element = self.merchant_orders_driver.find_element(self.merchant_orders_driver.li_page_prev)
        # 获得下一页按钮
        next_element = self.merchant_orders_driver.find_element(self.merchant_orders_driver.li_page_next)
        # 获得不可点击按钮
        disabled_element = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.li_page_disabled)
        if page_account == 1:
            assert prev_element in disabled_element, "上一页不是不可点击标签"
            assert next_element in disabled_element, "下一页不是不可点击标签"
        else:
            for page_position in range(page_account - 1):
                next_element.click()
                assert self.merchant_orders_driver.find_element(
                    self.merchant_orders_driver.li_page_item_active).text == str(
                    page_position + 2), "当前选中标签为:{},页码应为:{}".format(
                    self.merchant_orders_driver.find_element(self.merchant_orders_driver.li_page_item_active).text,
                    page_position + 2)
            time.sleep(5)
            # 判断不可点击按钮是否为下一页
            assert next_element in self.merchant_orders_driver.find_elements(
                self.merchant_orders_driver.li_page_disabled), "下一页不是不可点击标签"
            for page_position in range(page_account - 1)[::-1]:
                prev_element.click()
                assert self.merchant_orders_driver.find_element(
                    self.merchant_orders_driver.li_page_item_active).text == str(
                    page_position + 1), "当前选中标签为:{},页码应为:{}".format(
                    self.merchant_orders_driver.find_element(self.merchant_orders_driver.li_page_item_active).text,
                    page_position + 1)
            time.sleep(5)
            # 判断不可点击按钮是否为上一页
            assert prev_element in self.merchant_orders_driver.find_elements(
                self.merchant_orders_driver.li_page_disabled), "上一页不是不可点击标签"
        time.sleep(5)

    def test_merchant_orders_click_page_success(self):
        """测试点击页码（第二页、第三页）功能"""
        # 登陆成功后跳转到广告列表页面
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        # 设置页面锚点为底端
        self.merchant_orders_driver.js_scroll_end()
        time.sleep(5)
        # 获得所有分页的数量
        elements = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.li_page_item)
        page_account = int(elements[len(elements) - 1].text)
        self.log.info("页码数量为:{}".format(page_account))
        # 获得上一页按钮
        prev_element = self.merchant_orders_driver.find_element(self.merchant_orders_driver.li_page_prev)
        # 获得下一页按钮
        next_element = self.merchant_orders_driver.find_element(self.merchant_orders_driver.li_page_next)
        # 获得不可点击按钮
        disabled_element = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.li_page_disabled)
        if page_account == 1:
            assert prev_element in disabled_element, "上一页不是不可点击标签"
            assert next_element in disabled_element, "下一页不是不可点击标签"
        else:
            # 点击页码二
            elements[1].click()
            time.sleep(5)
            # 获取数据库数据
            try:
                select_info_sql = "select ID,SIDE,CREATE_TIME,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and ADVERTISER_MEMBER_ID = %s order by ID DESC limit %s,%s"
                orders_info_list = self.merchant_mysql.getAll(select_info_sql, (
                    self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id'],
                    20, 40))
                self.log.info("orders_info_list:{}".format(orders_info_list))
            except Exception as e:
                self.log.info("数据库异常:{}".format(e))
            # 获取页面数据
            merchant_order_list = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.div_orders)
            for merchant_order_list_position in range(len(merchant_order_list)):
                # 页面数据，类型：列表
                merchant_order_web_info = merchant_order_list[merchant_order_list_position].text.split('\n')
                # 数据库数据，类型：字典
                merchant_order_sql_info = orders_info_list[merchant_order_list_position]
                self.log.info("索引:{}".format(merchant_order_list_position))
                self.log.info("数据库广告:{}\n页面广告:{}".format(merchant_order_sql_info,
                                                         merchant_order_web_info))
                self.merchant_orders_driver.check_data(merchant_order_web_info, merchant_order_sql_info)
            # 校验数据
        time.sleep(5)

    def test_merchant_orders_detail(self):
        """查看订单详情测试"""
        # 登陆成功后跳转到广告列表页面
        time.sleep(5)
        self.merchant_orders_driver.open(merchant_order_url)
        time.sleep(5)
        # 获取页面数据
        merchant_order_elements = self.merchant_orders_driver.find_elements(self.merchant_orders_driver.div_orders)
        # 随机获取任一订单
        detail__order_element_position = random.randint(0, len(merchant_order_elements) - 1)
        # 获取数据库数据
        try:
            get_orders_info_sql = "select ID,SIDE,CREATE_TIME,ADVERT_ID,TARGET_VOLUME,TARGET_COIN,EXCHANGE_RATE,STANDARD_COIN,FEE_VOLUME,STATE from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and EXCHANGE_SWAP_ORDER = 0 and  ADVERTISER_MEMBER_ID=%s order by ID DESC limit 0,20;"
            orders_info_list = self.merchant_mysql.getAll(get_orders_info_sql, (
                self.member_id['member_id'], self.member_id['member_id'], self.member_id['member_id']))
        except Exception as e:
            self.log.info(e)
        merchant_order_web_info = merchant_order_elements[detail__order_element_position].text.split('\n')
        merchant_order_sql_info = orders_info_list[detail__order_element_position]
        self.log.info("数据库广告:{}\n页面广告:{}".format(merchant_order_sql_info,
                                                 merchant_order_web_info))
        # 获取所有查看按钮
        merchant_order_detail_elements = self.merchant_orders_driver.find_elements(
            self.merchant_orders_driver.span_detail)
        # 获取随机订单的查看按钮并点击
        merchant_order_detail_elements[detail__order_element_position + 1].click()
        time.sleep(5)
        # 断言跳转页面URL是否正确(订单、状态）
        self.log.info(self.driver.current_url)
        assert str(merchant_order_sql_info['ID']) in self.driver.current_url, "数据库订单ID:{},页面URL:{}".format(
            merchant_order_sql_info['ID'], self.driver.current_url)
        if merchant_order_sql_info['SIDE'] == 1:
            assert "buy" in self.driver.current_url, "数据库订单方向:1,页面URL:{}".format(
                merchant_order_sql_info['ID'], self.driver.current_url)
        elif merchant_order_sql_info['SIDE'] == 2:
            assert "sell" in self.driver.current_url, "数据库订单方向:2,页面URL:{}".format(
                merchant_order_sql_info['ID'], self.driver.current_url)
        assert str(merchant_order_sql_info[
                       'ADVERT_ID']) in self.driver.current_url, "数据库广告ID:{},页面URL:{}".format(
            merchant_order_sql_info['ADVERT_ID'], self.driver.current_url)

    @classmethod
    def tearDownClass(cls):
        cls.merchant_mysql.dispose()
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
