# coding:utf-8
import unittest
from common.base import set_options
from page.login_page import LoginPage, login_url
from common.log import Log
from common.opmysql import MysqlPool
from page.ordercenter import OrderCenterPage
import time
from decimal import *
import random


class TestOrderCenter(unittest.TestCase):
    """测试订单管理"""

    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.login_driver = LoginPage(cls.driver)
        cls.login_driver.open(login_url)
        cls.login_driver.user_login(cls.login_driver, "lifq_user26@qq.com", "ab1234567")
        cls.order_center_driver = OrderCenterPage(cls.driver)
        cls.log = Log()

    def test_order_center_click_item_page_success(self):
        """测试点击页码功能"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为底端
        self.order_center_driver.js_scroll_end()
        # 获得所有分页的数量
        elements = self.order_center_driver.find_elements(self.order_center_driver.li_page_item)
        page_account = len(elements)
        self.log.info("页码数量为:{}".format(page_account))
        # 获得上一页按钮
        prev_element = self.order_center_driver.find_element(self.order_center_driver.li_page_prev)
        # 获得下一页按钮
        next_element = self.order_center_driver.find_element(self.order_center_driver.li_page_next)
        # 获得不可点击按钮
        disabled_element = self.order_center_driver.find_elements(self.order_center_driver.li_page_disabled)
        # 判断不可点击按钮是否是首页
        assert prev_element in disabled_element
        # 判断当前选中的页码是否是第一页
        assert self.order_center_driver.find_element(
            self.order_center_driver.li_page_item_active).text == '1', "当前选中标签为:{}".format(
            self.order_center_driver.find_element(self.order_center_driver.li_page_item_active).text)
        if page_account == 1:
            assert prev_element in disabled_element
            assert next_element in disabled_element
        else:
            for page_position in range(page_account):
                self.log.info("第{}页".format(page_position + 1))
                elements[page_position].click()
                assert self.order_center_driver.find_element(
                    self.order_center_driver.li_page_item_active).text == str(page_position + 1), "当前选中标签为:{}".format(
                    self.order_center_driver.find_element(self.order_center_driver.li_page_item_active).text)
                time.sleep(5)
            # 判断不可点击按钮是否为下一页
            assert next_element in self.order_center_driver.find_elements(self.order_center_driver.li_page_disabled)
        self.driver.refresh()
        time.sleep(5)

    def test_order_center_click_next_page_success(self):
        """测试点击下一页|上一页功能"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为底端
        self.order_center_driver.js_scroll_end()
        # 获得所有分页的数量
        elements = self.order_center_driver.find_elements(self.order_center_driver.li_page_item)
        page_account = int(elements[len(elements) - 1].text)
        self.log.info("页码数量为:{}".format(page_account))
        # 获得上一页按钮
        prev_element = self.order_center_driver.find_element(self.order_center_driver.li_page_prev)
        # 获得下一页按钮
        next_element = self.order_center_driver.find_element(self.order_center_driver.li_page_next)
        # 获得不可点击按钮
        disabled_element = self.order_center_driver.find_elements(self.order_center_driver.li_page_disabled)
        if page_account == 1:
            assert prev_element in disabled_element, "上一页不是不可点击标签"
            assert next_element in disabled_element, "下一页不是不可点击标签"
        else:
            for page_position in range(page_account - 1):
                next_element.click()
                assert self.order_center_driver.find_element(
                    self.order_center_driver.li_page_item_active).text == str(
                    page_position + 2), "当前选中标签为:{},页码应为:{}".format(
                    self.order_center_driver.find_element(self.order_center_driver.li_page_item_active).text,
                    page_position + 2)
                time.sleep(5)
            # 判断不可点击按钮是否为下一页
            assert next_element in self.order_center_driver.find_elements(
                self.order_center_driver.li_page_disabled), "下一页不是不可点击标签"
            for page_position in range(page_account - 1)[::-1]:
                prev_element.click()
                assert self.order_center_driver.find_element(
                    self.order_center_driver.li_page_item_active).text == str(
                    page_position + 1), "当前选中标签为:{},页码应为:{}".format(
                    self.order_center_driver.find_element(self.order_center_driver.li_page_item_active).text,
                    page_position + 1)
                time.sleep(5)
            # 判断不可点击按钮是否为上一页
            assert prev_element in self.order_center_driver.find_elements(
                self.order_center_driver.li_page_disabled), "上一页不是不可点击标签"
        self.driver.refresh()
        time.sleep(5)

    def test_order_center_ongoing_order(self):
        """进行中订单列表"""
        # 登陆成功后跳转到订单中心页面
        self.login_driver.user_login_click_order_center(self.login_driver)
        time.sleep(5)
        # 获取页面所有进行中的订单元素
        order_center_elements = self.order_center_driver.find_elements(self.order_center_driver.ul_ongoing_order)
        self.log.info("进行中订单列表长度:{}".format(len(order_center_elements)))
        # 获取数据库中所有进行中的订单信息
        try:
            order_mysql = MysqlPool("mysql")
            get_member_id = "select member_id from member.tm_member_identity where identity = %s "
            member_id = order_mysql.getOne(get_member_id, "lifq_user26@qq.com")
            get_order_info_list = "select ID,SIDE,CREATE_TIME,STANDARD_COIN,TARGET_COIN,STANDARD_VOLUME,STANDARD_REAL_VOLUME,EXCHANGE_RATE,TARGET_VOLUME,FEE_VOLUME from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s)and STATE in (10,20,30)order by id desc ;"
            order_info_list = order_mysql.getAll(get_order_info_list, (member_id['member_id'], member_id['member_id']))
        except Exception as e:
            self.log.info(e)
        finally:
            order_mysql.dispose()
        for ongoing_order_position in range(len(order_center_elements)):
            # 将页面text信息封装为
            loc_ongoing_order_info = order_center_elements[ongoing_order_position].text.split('\n')
            self.log.info("页面订单详情:{}".format(loc_ongoing_order_info))
            # 获取数据库中信息
            mysql_ongoing_order_info = order_info_list[ongoing_order_position]
            self.log.info("数据库订单详情:{}".format(mysql_ongoing_order_info))
            # 数据校验
            if loc_ongoing_order_info[0] == 'buy':
                # 校验订单类型
                assert mysql_ongoing_order_info['SIDE'] == 1
                # 校验数字币数量
                assert mysql_ongoing_order_info['STANDARD_REAL_VOLUME'].quantize(Decimal('0.0000')), \
                    mysql_ongoing_order_info['STANDARD_COIN'] == loc_ongoing_order_info[5]

            elif loc_ongoing_order_info[0] == 'sell':
                assert mysql_ongoing_order_info['SIDE'] == 2
                # 校验数字币数量
                assert mysql_ongoing_order_info['STANDARD_VOLUME'].quantize(Decimal('0.0000')), \
                    mysql_ongoing_order_info['STANDARD_COIN'] == loc_ongoing_order_info[5]
            # 校验订单号
            assert str(mysql_ongoing_order_info['ID']) in loc_ongoing_order_info[
                1], "数据库订单ID:{},页面订单ID:{},索引:{}".format(mysql_ongoing_order_info['ID'],
                                                        loc_ongoing_order_info[1],
                                                        ongoing_order_position)
            # 校验交易时间
            assert str(mysql_ongoing_order_info['CREATE_TIME']) in loc_ongoing_order_info[
                2], "数据库时间为:{},页面时间:{}".format(
                str(mysql_ongoing_order_info['CREATE_TIME']), loc_ongoing_order_info[2])
            # 校验法币数量
            assert format(str(mysql_ongoing_order_info['TARGET_VOLUME'].quantize(Decimal('0.00'))), ','), \
                mysql_ongoing_order_info['TARGET_COIN'] == loc_ongoing_order_info[3]
            # 校验价格
            if mysql_ongoing_order_info['TARGET_COIN'] == 'HDK':
                assert str(mysql_ongoing_order_info['EXCHANGE_RATE'].quantize(Decimal('0.000'))), "{}/{}".format(
                    mysql_ongoing_order_info['TARGET_COIN'], mysql_ongoing_order_info['STANDARD_COIN']) == \
                                                                                                  loc_ongoing_order_info[
                                                                                                      ongoing_order_position][
                                                                                                      4]
            elif mysql_ongoing_order_info['TARGET_COIN'] == 'USD':
                assert str(mysql_ongoing_order_info['EXCHANGE_RATE'].quantize(Decimal('0.0000'))), "{}/{}".format(
                    mysql_ongoing_order_info['TARGET_COIN'], mysql_ongoing_order_info['STANDARD_COIN']) == \
                                                                                                   loc_ongoing_order_info[
                                                                                                       ongoing_order_position][
                                                                                                       4]
            else:
                assert str(mysql_ongoing_order_info['EXCHANGE_RATE'].quantize(Decimal('0.00'))), "{}/{}".format(
                    mysql_ongoing_order_info['TARGET_COIN'], mysql_ongoing_order_info['STANDARD_COIN']) == \
                                                                                                 loc_ongoing_order_info[
                                                                                                     ongoing_order_position][
                                                                                                     4]
            # 检验手续费
            assert mysql_ongoing_order_info['FEE_VOLUME'].quantize(Decimal('0.0000')), mysql_ongoing_order_info[
                                                                                           'STANDARD_COIN'] == \
                                                                                       loc_ongoing_order_info[
                                                                                           ongoing_order_position][7]
        self.driver.refresh()
        time.sleep(5)

    def test_order_center_trade_order(self):
        """大额订单列表"""
        # 登陆成功后跳转到订单中心页面
        self.login_driver.user_login_click_order_center(self.login_driver)
        time.sleep(5)
        order_center_elements = self.order_center_driver.find_elements(self.order_center_driver.ul_trade_order)
        self.log.info("大额订单列表长度:{}".format(len(order_center_elements)))
        for element in order_center_elements:
            self.log.info(element.text)
        self.driver.refresh()
        time.sleep(5)

    def test_order_center_recent_order(self):
        """近期订单列表"""
        # 登陆成功后跳转到订单中心页面
        self.login_driver.user_login_click_order_center(self.login_driver)
        time.sleep(5)
        # 获取数据库中所有进行中的订单信息
        try:
            order_mysql = MysqlPool("mysql")
            get_member_id = "select member_id from member.tm_member_identity where identity = %s "
            member_id = order_mysql.getOne(get_member_id, "lifq_user26@qq.com")
            get_order_info_list = "select ID,SIDE,CREATE_TIME,STANDARD_COIN,TARGET_COIN,STANDARD_VOLUME,STANDARD_REAL_VOLUME,EXCHANGE_RATE,TARGET_VOLUME,FEE_VOLUME from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and STATE  in (40,90,50) and ADVERTISER_MEMBER_ID=%s order by id desc ;"
            order_info_list = order_mysql.getAll(get_order_info_list, (
                member_id['member_id'], member_id['member_id'], member_id['member_id']))
        except Exception as e:
            self.log.info(e)
        finally:
            order_mysql.dispose()
        order_center_elements = self.order_center_driver.find_elements(self.order_center_driver.ul_recent_order)
        self.log.info("近期订单列表长度:{}".format(len(order_center_elements)))
        for recent_order_position in range(len(order_center_elements)):
            # 将页面text信息封装为
            loc_recent_order_info = order_center_elements[recent_order_position].text.split('\n')
            # self.log.info("页面订单详情:{}".format(loc_recent_order_info))
            # 获取数据库中信息
            mysql_recent_order_info = order_info_list[recent_order_position]
            # self.log.info("数据库订单详情:{}".format(mysql_recent_order_info))
            # 数据校验
            if loc_recent_order_info[0] == 'buy':
                # 校验订单类型
                assert mysql_recent_order_info['SIDE'] == 1
                # 校验数字币数量
                assert mysql_recent_order_info['STANDARD_REAL_VOLUME'].quantize(Decimal('0.0000')), \
                    mysql_recent_order_info['STANDARD_COIN'] == loc_recent_order_info[5]

            elif loc_recent_order_info[0] == 'sell':
                assert mysql_recent_order_info['SIDE'] == 2
                # 校验数字币数量
                assert mysql_recent_order_info['STANDARD_VOLUME'].quantize(Decimal('0.0000')), \
                    mysql_recent_order_info['STANDARD_COIN'] == loc_recent_order_info[5]
            # 校验订单号
            assert str(mysql_recent_order_info['ID']) in loc_recent_order_info[
                1], "数据库订单ID:{},页面订单ID:{},索引:{}".format(mysql_recent_order_info['ID'],
                                                        loc_recent_order_info[1],
                                                        recent_order_position)
            # 校验交易时间
            assert str(mysql_recent_order_info['CREATE_TIME']) in loc_recent_order_info[
                2], "数据库时间为:{},页面时间:{}".format(
                str(mysql_recent_order_info['CREATE_TIME']), loc_recent_order_info[2])
            # 校验法币数量
            assert format(str(mysql_recent_order_info['TARGET_VOLUME'].quantize(Decimal('0.00'))), ','), \
                mysql_recent_order_info['TARGET_COIN'] == loc_recent_order_info[3]
            # 校验价格
            if mysql_recent_order_info['TARGET_COIN'] == 'HDK':
                assert str(mysql_recent_order_info['EXCHANGE_RATE'].quantize(Decimal('0.000'))), "{}/{}".format(
                    mysql_recent_order_info['TARGET_COIN'], mysql_recent_order_info['STANDARD_COIN']) == \
                                                                                                 loc_recent_order_info[
                                                                                                     recent_order_position][
                                                                                                     4]
            elif mysql_recent_order_info['TARGET_COIN'] == 'USD':
                assert str(mysql_recent_order_info['EXCHANGE_RATE'].quantize(Decimal('0.0000'))), "{}/{}".format(
                    mysql_recent_order_info['TARGET_COIN'], mysql_recent_order_info['STANDARD_COIN']) == \
                                                                                                  loc_recent_order_info[
                                                                                                      recent_order_position][
                                                                                                      4]
            else:
                assert str(mysql_recent_order_info['EXCHANGE_RATE'].quantize(Decimal('0.00'))), "{}/{}".format(
                    mysql_recent_order_info['TARGET_COIN'], mysql_recent_order_info['STANDARD_COIN']) == \
                                                                                                loc_recent_order_info[
                                                                                                    recent_order_position][
                                                                                                    4]
            # 检验手续费
            assert mysql_recent_order_info['FEE_VOLUME'].quantize(Decimal('0.0000')), mysql_recent_order_info[
                                                                                          'STANDARD_COIN'] == \
                                                                                      loc_recent_order_info[
                                                                                          recent_order_position][7]
        self.driver.refresh()
        time.sleep(5)

    def test_order_center_order_refresh(self):
        """刷新按钮测试"""
        # 登陆成功后跳转到订单中心页面
        self.login_driver.user_login_click_order_center(self.login_driver)
        time.sleep(5)
        # 获取所有刷新按钮
        order_center_refresh_elements = self.order_center_driver.find_elements(self.order_center_driver.i_order_refresh)
        self.log.info("刷新按钮数量:{}".format(len(order_center_refresh_elements)))
        for order_center_refresh_position in range(len(order_center_refresh_elements)):
            order_center_refresh_elements[order_center_refresh_position].click()
            time.sleep(5)
            # 校验进行中订单数据
            if order_center_refresh_position == 0:
                # 获取页面所有进行中的订单元素
                order_center_elements = self.order_center_driver.find_elements(
                    self.order_center_driver.ul_ongoing_order)
                self.log.info("进行中订单列表长度:{}".format(len(order_center_elements)))
                # 获取数据库中所有进行中的订单信息
                try:
                    order_mysql = MysqlPool("mysql")
                    get_member_id = "select member_id from member.tm_member_identity where identity = %s "
                    member_id = order_mysql.getOne(get_member_id, "lifq_user26@qq.com")
                    get_order_info_list = "select ID,SIDE,CREATE_TIME,STANDARD_COIN,TARGET_COIN,STANDARD_VOLUME,STANDARD_REAL_VOLUME,EXCHANGE_RATE,TARGET_VOLUME,FEE_VOLUME from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s)and STATE in (10,20,30)order by id desc ;"
                    order_info_list = order_mysql.getAll(get_order_info_list,
                                                         (member_id['member_id'], member_id['member_id']))
                except Exception as e:
                    self.log.info(e)
                finally:
                    order_mysql.dispose()
                for ongoing_order_position in range(len(order_center_elements)):
                    # 将页面text信息封装为
                    loc_ongoing_order_info = order_center_elements[ongoing_order_position].text.split('\n')
                    self.log.info("页面订单详情:{}".format(loc_ongoing_order_info))
                    # 获取数据库中信息
                    mysql_ongoing_order_info = order_info_list[ongoing_order_position]
                    self.log.info("数据库订单详情:{}".format(mysql_ongoing_order_info))
                    # 数据校验
                    if loc_ongoing_order_info[0] == 'buy':
                        # 校验订单类型
                        assert mysql_ongoing_order_info['SIDE'] == 1
                        # 校验数字币数量
                        assert mysql_ongoing_order_info['STANDARD_REAL_VOLUME'].quantize(Decimal('0.0000')), \
                            mysql_ongoing_order_info['STANDARD_COIN'] == loc_ongoing_order_info[5]

                    elif loc_ongoing_order_info[0] == 'sell':
                        assert mysql_ongoing_order_info['SIDE'] == 2
                        # 校验数字币数量
                        assert mysql_ongoing_order_info['STANDARD_VOLUME'].quantize(Decimal('0.0000')), \
                            mysql_ongoing_order_info['STANDARD_COIN'] == loc_ongoing_order_info[5]
                    # 校验订单号
                    assert str(mysql_ongoing_order_info['ID']) in loc_ongoing_order_info[
                        1], "数据库订单ID:{},页面订单ID:{},索引:{}".format(mysql_ongoing_order_info['ID'],
                                                                loc_ongoing_order_info[1],
                                                                ongoing_order_position)
                    # 校验交易时间
                    assert str(mysql_ongoing_order_info['CREATE_TIME']) in loc_ongoing_order_info[
                        2], "数据库时间为:{},页面时间:{}".format(
                        str(mysql_ongoing_order_info['CREATE_TIME']), loc_ongoing_order_info[2])
                    # 校验法币数量
                    assert format(str(mysql_ongoing_order_info['TARGET_VOLUME'].quantize(Decimal('0.00'))), ","), \
                        mysql_ongoing_order_info['TARGET_COIN'] == loc_ongoing_order_info[3]
                    # 校验价格
                    if mysql_ongoing_order_info['TARGET_COIN'] == 'HDK':
                        assert str(
                            mysql_ongoing_order_info['EXCHANGE_RATE'].quantize(Decimal('0.000'))), "{}/{}".format(
                            mysql_ongoing_order_info['TARGET_COIN'], mysql_ongoing_order_info['STANDARD_COIN']) == \
                                                                                                   loc_ongoing_order_info[
                                                                                                       ongoing_order_position][
                                                                                                       4]
                    elif mysql_ongoing_order_info['TARGET_COIN'] == 'USD':
                        assert str(
                            mysql_ongoing_order_info['EXCHANGE_RATE'].quantize(Decimal('0.0000'))), "{}/{}".format(
                            mysql_ongoing_order_info['TARGET_COIN'], mysql_ongoing_order_info['STANDARD_COIN']) == \
                                                                                                    loc_ongoing_order_info[
                                                                                                        ongoing_order_position][
                                                                                                        4]
                    else:
                        assert str(mysql_ongoing_order_info['EXCHANGE_RATE'].quantize(Decimal('0.00'))), "{}/{}".format(
                            mysql_ongoing_order_info['TARGET_COIN'], mysql_ongoing_order_info['STANDARD_COIN']) == \
                                                                                                         loc_ongoing_order_info[
                                                                                                             ongoing_order_position][
                                                                                                             4]
                    # 检验手续费
                    assert mysql_ongoing_order_info['FEE_VOLUME'].quantize(Decimal('0.0000')), mysql_ongoing_order_info[
                                                                                                   'STANDARD_COIN'] == \
                                                                                               loc_ongoing_order_info[
                                                                                                   ongoing_order_position][
                                                                                                   7]
            elif order_center_refresh_position == 1:
                pass
        self.driver.refresh()
        time.sleep(5)

    def test_order_center_order_view_all_order(self):
        """查询所有订单测试"""
        # 登陆成功后跳转到订单中心页面
        self.login_driver.user_login_click_order_center(self.login_driver)
        time.sleep(5)
        # 获取查看所有订单按钮并点击
        self.order_center_driver.click(self.order_center_driver.span_view_all_orders)
        time.sleep(5)
        assert self.driver.current_url == 'http://wex.test.tigerft.com/business/order-list', "当前页面URL{}".format(
            self.driver.current_url)
        self.driver.refresh()
        time.sleep(5)

    def test_order_center_ongoing_order_detail(self):
        """进行中的订单查看详情测试"""
        # 登陆成功后跳转到订单中心页面
        self.login_driver.user_login_click_order_center(self.login_driver)
        time.sleep(5)
        # 获取页面所有进行中的订单元素
        all_ongoing_order_elements = self.order_center_driver.find_elements_by_class_name(
            self.order_center_driver.span_ongoing_order_detail)
        self.log.info("进行中订单列表长度:{}".format(len(all_ongoing_order_elements)))
        detail_ongoing_order_elements = []
        for order_center_element in all_ongoing_order_elements:
            # self.log.info(order_center_element.get_attribute("class"))
            if "bright-blue" in order_center_element.get_attribute("class"):
                detail_ongoing_order_elements.append(order_center_element)
        self.log.info(detail_ongoing_order_elements)
        # 获取数据库中所有进行中的订单信息
        try:
            order_mysql = MysqlPool("mysql")
            get_member_id = "select member_id from member.tm_member_identity where identity = %s "
            member_id = order_mysql.getOne(get_member_id, "lifq_user26@qq.com")
            get_order_info_list = "select ID,SIDE,ADVERT_ID from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s)and STATE in (10,20,30)order by id desc ;"
            order_info_list = order_mysql.getAll(get_order_info_list, (
                member_id['member_id'], member_id['member_id']))
            self.log.info(order_info_list)
        except Exception as e:
            self.log.info(e)
        finally:
            order_mysql.dispose()
        # 随机获取一个订单
        detail_ongoing_order_element_position = random.randint(0, len(detail_ongoing_order_elements) - 1)
        self.log.info(detail_ongoing_order_element_position)
        # 点击该订单的查看详情按钮
        detail_ongoing_order_elements[detail_ongoing_order_element_position].click()
        time.sleep(5)
        # 断言跳转页面URL是否正确(订单、状态）
        self.log.info(self.driver.current_url)
        assert str(order_info_list[detail_ongoing_order_element_position][
                       'ID']) in self.driver.current_url, "数据库订单ID:{},页面URL:{}".format(
            order_info_list[detail_ongoing_order_element_position]['ID'], self.driver.current_url)
        if order_info_list[detail_ongoing_order_element_position]['SIDE'] == 1:
            assert "buy" in self.driver.current_url, "数据库订单方向:1,页面URL:{}".format(
                order_info_list[detail_ongoing_order_element_position]['ID'], self.driver.current_url)
        elif order_info_list[detail_ongoing_order_element_position]['SIDE'] == 2:
            assert "sell" in self.driver.current_url, "数据库订单方向:2,页面URL:{}".format(
                order_info_list[detail_ongoing_order_element_position]['ID'], self.driver.current_url)
        assert str(order_info_list[detail_ongoing_order_element_position][
                       'ADVERT_ID']) in self.driver.current_url, "数据库广告ID:{},页面URL:{}".format(
            order_info_list[detail_ongoing_order_element_position]['ADVERT_ID'], self.driver.current_url)

    def test_order_center_recent_order_detail(self):
        """近期的订单查看详情测试"""
        # 登陆成功后跳转到订单中心页面
        self.login_driver.user_login_click_order_center(self.login_driver)
        time.sleep(5)
        # 获取页面所有进行中的订单元素
        all_recent_order_elements = self.order_center_driver.find_elements_by_class_name(
            self.order_center_driver.span_recent_order_detail)
        self.log.info("最近订单列表长度:{}".format(len(all_recent_order_elements)))
        detail_recent_order_elements = []
        for order_center_element in all_recent_order_elements:
            # self.log.info(order_center_element.get_attribute("class"))
            if "bright-blue" in order_center_element.get_attribute("class"):
                detail_recent_order_elements.append(order_center_element)
        self.log.info(detail_recent_order_elements)
        # 获取数据库中所有进行中的订单信息
        try:
            order_mysql = MysqlPool("mysql")
            get_member_id = "select member_id from member.tm_member_identity where identity = %s "
            member_id = order_mysql.getOne(get_member_id, "lifq_user26@qq.com")
            get_order_info_list = "select ID,SIDE,ADVERT_ID from otc.tb_otc_order where (PAY_MEMBER_ID =%s or RECIEVE_MEMBER_ID=%s) and STATE  in (40,90,50) and ADVERTISER_MEMBER_ID=%s order by id desc ;"
            order_info_list = order_mysql.getAll(get_order_info_list, (
                member_id['member_id'], member_id['member_id'], member_id['member_id']))
            self.log.info(order_info_list)
        except Exception as e:
            self.log.info(e)
        finally:
            order_mysql.dispose()
        # 随机获取一个订单
        detail_recent_order_element_position = random.randint(0, len(detail_recent_order_elements) - 1)
        self.log.info(detail_recent_order_element_position)
        # 点击该订单的查看详情按钮
        detail_recent_order_elements[detail_recent_order_element_position].click()
        time.sleep(5)
        # 断言跳转页面URL是否正确(订单、状态）
        self.log.info(self.driver.current_url)
        assert str(order_info_list[detail_recent_order_element_position][
                       'ID']) in self.driver.current_url, "数据库订单ID:{},页面URL:{}".format(
            order_info_list[detail_recent_order_element_position]['ID'], self.driver.current_url)
        if order_info_list[detail_recent_order_element_position]['SIDE'] == 1:
            assert "buy" in self.driver.current_url, "数据库订单方向:1,页面URL:{}".format(
                order_info_list[detail_recent_order_element_position]['ID'], self.driver.current_url)
        elif order_info_list[detail_recent_order_element_position]['SIDE'] == 2:
            assert "sell" in self.driver.current_url, "数据库订单方向:2,页面URL:{}".format(
                order_info_list[detail_recent_order_element_position]['ID'], self.driver.current_url)
        assert str(order_info_list[detail_recent_order_element_position][
                       'ADVERT_ID']) in self.driver.current_url, "数据库广告ID:{},页面URL:{}".format(
            order_info_list[detail_recent_order_element_position]['ADVERT_ID'], self.driver.current_url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    if __name__ == "__main__":
        unittest.main()
