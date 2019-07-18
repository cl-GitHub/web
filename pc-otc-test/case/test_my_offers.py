# coding:utf-8
import os
from common.excelutil import Excel
from common.opmysql import MysqlPool
import unittest
import ddt
from decimal import *
from common.base import set_options
from page.myoffers import MyOffersPage
from page.login_page import LoginPage, login_url
from common.log import Log
import time
import random

"""
初始化数据表 发布广告成功数据表
"""
project_dir = os.path.dirname(os.path.abspath('.'))
excelPath = project_dir + '/pc-otc-test/data/login.xlsx'
"""如果测试单个test"""
# excelPath = project_dir + '/data/login.xlsx'
MyOfferSheetName = "广告管理数据表"
post_an_offer_excel = Excel(excelPath)
my_offers_data = post_an_offer_excel.get_list(MyOfferSheetName, False)


@ddt.ddt
class TestMyOffers(unittest.TestCase):
    """测试广告管理"""

    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.login_driver = LoginPage(cls.driver)
        cls.login_driver.open(login_url)
        cls.login_driver.user_login(cls.login_driver, "lifq_user26@qq.com", "ab1234567")
        cls.my_offers_driver = MyOffersPage(cls.driver)
        cls.log = Log()

    def test_my_offers_home_page_success(self):
        """测试首页广告信息"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)

        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()

        # 获取当前页面所有广告
        my_offers_elements = self.my_offers_driver.find_elements(self.my_offers_driver.div_my_offer)

        # 获取数据库中所有广告
        try:
            otc_mysql = MysqlPool("mysql")
            get_member_id = "select member_id from member.tm_member_identity where identity = %s "
            member_id = otc_mysql.getOne(get_member_id, "lifq_user26@qq.com")
            get_otc_info = "select * from otc.tb_otc_advert where member_id = %s and STATE != 90 order by STATE,CREATE_TIME desc limit 0,19"
            otc_info = otc_mysql.getAll(get_otc_info, (member_id['member_id'],))
            self.log.info("广告详情:{}".format(otc_info))
        except Exception as e:
            self.log.info(e)
        finally:
            otc_mysql.dispose()
        for advert_position in range(len(my_offers_elements)):
            # 获取每个广告div的text信息
            element_text = my_offers_elements[advert_position].text
            # 将text信息封装为
            my_offers_info = element_text.split('\n')
            self.log.info("my_offers_info:{}".format(my_offers_info))
            # 获取当前广告的支付方式
            try:
                otc_advert_payment_way_mysql = MysqlPool("mysql")
                get_payment_way = "select distinct EXCHANGE_WAY from otc.tb_otc_advert_payment_way where VALID=1 and ADVERT_ID = %s order by EXCHANGE_WAY;"
                payment_way = otc_advert_payment_way_mysql.getAll(get_payment_way, (otc_info[advert_position]['ID'],))
                self.log.info("支付方式:{}".format(payment_way))
            except Exception as e:
                self.log.info(e)
            finally:
                otc_advert_payment_way_mysql.dispose(otc_advert_payment_way_mysql)
            payment_way_list = []
            for payment_way_info in payment_way:
                payment_way_list.append(payment_way_info['EXCHANGE_WAY'])
            self.log.info("支付列表:{}".format(payment_way_list))
            # 将广告信息与数据库表做断言
            # 判断广告方向
            if 'Buy offer' in my_offers_info[1]:
                assert otc_info[advert_position]['SIDE'] == 1, "数据库中广告类型:{}，页面广告类型:{}".format(
                    otc_info[advert_position]['SIDE'], my_offers_info[1])
            elif 'Sell offer' in my_offers_info[1]:
                assert otc_info[advert_position]['SIDE'] == 2, "数据库中广告类型:{}，页面广告类型:{}".format(
                    otc_info[advert_position]['SIDE'], my_offers_info[1])
            # 判断广告类型
            elif '(Float)' in my_offers_info[1]:
                assert otc_info[advert_position]['BID_WAY'] == 1, "数据库中广告类型:{}，页面广告类型:{}".format(
                    otc_info[advert_position]['BID_WAY'], my_offers_info[1])
            elif '(Fixed)' in my_offers_info[1]:
                assert otc_info[advert_position]['BID_WAY'] == 2, "数据库中广告类型:{}，页面广告类型:{}".format(
                    otc_info[advert_position]['BID_WAY'], my_offers_info[1])
            # 判断广告价格
            if otc_info[advert_position]['OFFLINE_COIN'] == 'USD':
                assert my_offers_info[2] == str(otc_info[advert_position]['BID_PRICE'].quantize(
                    Decimal(
                        '0.0000'))), "页面价格:{},页面价格的数据类型:{},数据库价格:{},数据库价格的数据类型:{}".format(
                    my_offers_info[2],
                    type(my_offers_info[2]),
                    otc_info[advert_position][
                        'BID_PRICE'].quantize(
                        Decimal('0.0000')),
                    type(
                        otc_info[advert_position][
                            'BID_PRICE'].quantize(
                            Decimal('0.0000'))))
            elif otc_info[advert_position]['OFFLINE_COIN'] == 'HKD':
                assert my_offers_info[2] == str(otc_info[advert_position]['BID_PRICE'].quantize(
                    Decimal(
                        '0.000'))), "页面价格:{},页面价格的数据类型:{},数据库价格:{},数据库价格的数据类型:{}".format(
                    my_offers_info[2],
                    type(my_offers_info[2]),
                    otc_info[advert_position][
                        'BID_PRICE'].quantize(
                        Decimal('0.000')),
                    type(
                        otc_info[advert_position][
                            'BID_PRICE'].quantize(
                            Decimal('0.000'))))
            else:
                assert my_offers_info[2] == str(otc_info[advert_position]['BID_PRICE'].quantize(
                    Decimal(
                        '0.00'))), "页面价格:{},页面价格的数据类型:{},数据库价格:{},数据库价格的数据类型:{}".format(
                    my_offers_info[2],
                    type(my_offers_info[2]),
                    otc_info[advert_position][
                        'BID_PRICE'].quantize(
                        Decimal('0.00')),
                    type(
                        otc_info[advert_position][
                            'BID_PRICE'].quantize(
                            Decimal('0.00'))))
            # 判断广告币种
            assert "{}/{}".format(otc_info[advert_position]['OFFLINE_COIN'],
                                  otc_info[advert_position]['PLATFORM_COIN']) == my_offers_info[
                       3], "数据库中交易币种:{},页面交易币种:{}".format(
                "{}/{}".format(otc_info[advert_position]['OFFLINE_COIN'], otc_info[advert_position]['PLATFORM_COIN']),
                my_offers_info[3])
            # 判断广告限额
            assert "{}-{}".format(otc_info[advert_position]['EXCHANGE_MIN_VOLUMN'].quantize(Decimal('0')),
                                  otc_info[advert_position]['EXCHANGE_MAX_VOLUMN'].quantize(Decimal('0'))) == \
                   my_offers_info[4].translate(str.maketrans('', '', ',')), "数据库拼接广告限额:{},页面广告限额:{}".format(
                "{}-{}".format(otc_info[advert_position]['EXCHANGE_MIN_VOLUMN'].quantize(Decimal('0')),
                               otc_info[advert_position]['EXCHANGE_MAX_VOLUMN'].quantize(Decimal('0'))),
                my_offers_info[4].translate(str.maketrans('', '', ',')))

            # 判断支付方式
            # 支付方式列表
            payment_method = {1: 'Bank card', 2: 'Alipay', 3: 'WeChat', 4: 'PayPal', 5: 'FPS', 6: 'PayMe', 7: 'Faspay',
                              8: 'Line Pay', 9: 'Cash'}
            for i in range(len(payment_way_list)):
                assert my_offers_info[6 + i] == payment_method[payment_way_list[i]], "数据库中支付方式:{},页面支付方式:{}".format(
                    payment_way_list[i], my_offers_info[6 + i])
            # 判断广告是否开启自动上下架
            if my_offers_info[-2] == 'Off':
                # 判断广告交易时间
                assert "{} minutes".format(otc_info[advert_position]['RESPONSE_MIN']) == str(
                    my_offers_info[-5]), "未开启自动上架的交易时间:数据库{},页面{}".format(
                    "{} minutes".format(otc_info[advert_position]['RESPONSE_MIN']),
                    my_offers_info[-5])
                self.log.info("交易数:数据库{},页面{}".format(otc_info[advert_position]['TRADE_SUCCESS_COUNT'],
                                                      my_offers_info[-4]))
                self.log.info(
                    "交易数类型:数据库{},页面{}".format(type(otc_info[advert_position]['TRADE_SUCCESS_COUNT']),
                                              type(my_offers_info[-4])))
                # 判断广告交易数
                assert str(otc_info[advert_position]['TRADE_SUCCESS_COUNT']) == my_offers_info[
                    -4], "交易数:数据库{},页面{}".format(
                    otc_info[advert_position]['TRADE_SUCCESS_COUNT'],
                    my_offers_info[-4])
            else:
                # 判断广告交易时间
                assert "{} minutes".format(otc_info[advert_position]['RESPONSE_MIN']) == str(
                    my_offers_info[-6]), "自动上架的交易时间:数据库{},页面{}".format(
                    "{} minutes".format(otc_info[advert_position]['RESPONSE_MIN']),
                    my_offers_info[-6])
                # 判断广告交易数
                assert str(otc_info[advert_position]['TRADE_SUCCESS_COUNT']) == my_offers_info[
                    -5], "交易数:数据库{},页面{}".format(
                    otc_info[advert_position]['TRADE_SUCCESS_COUNT'],
                    my_offers_info[-5])
            # 判断广告是否开启自动上下架
            if my_offers_info[-2] == 'Off':
                assert otc_info[advert_position]['AUTO_UP_OR_DOWN'] == 0, "数据库中广告自动上下架信息为:{}".format(
                    otc_info[advert_position]['AUTO_UP_OR_DOWN'])
                # 判断广告是否上架
                if otc_info[advert_position]['STATE'] == 10:
                    assert my_offers_info[-3] == 'on', "页面广告上架信息为:{}".format(my_offers_info[-3])
                elif otc_info[advert_position]['STATE'] == 20:
                    assert my_offers_info[-3] == 'off', "页面广告上架信息为:{}".format(my_offers_info[-3])
            else:
                assert otc_info[advert_position]['AUTO_UP_OR_DOWN'] == 1, "数据库中广告自动上下架信息为:{}".format(
                    otc_info[advert_position]['AUTO_UP_OR_DOWN'])
                assert otc_info[advert_position]['JOB_UP_TIME'] in my_offers_info[-3], "数据库中广告自动上架时间为:{}".format(
                    otc_info[advert_position]['JOB_UP_TIME'])
                assert otc_info[advert_position]['JOB_DOWN_TIME'] in my_offers_info[-2], "数据库中广告自动下架时间为:{}".format(
                    otc_info[advert_position]['JOB_DOWN_TIME'])
                # 判断广告是否上架
                if otc_info[advert_position]['STATE'] == 10:
                    assert my_offers_info[-4] == 'on', "页面广告上架信息为:{}".format(my_offers_info[-4])
                elif otc_info[advert_position]['STATE'] == 20:
                    assert my_offers_info[-4] == 'off', "页面广告上架信息为:{}".format(my_offers_info[-4])
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_all_page_success(self):
        """测试每页广告数据"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为底端
        self.my_offers_driver.js_scroll_end()
        # 获得所有分页的数量
        elements = self.my_offers_driver.find_elements(self.my_offers_driver.li_page_item)
        page_account = len(elements)
        for page_position in range(page_account):
            self.log.info("第{}页".format(page_position + 1))
            elements[page_position].click()
            time.sleep(30)
            # 获取数据库中所有广告
            try:
                otc_mysql = MysqlPool("mysql")
                get_member_id = "select member_id from member.tm_member_identity where identity = %s "
                member_id = otc_mysql.getOne(get_member_id, "lifq_user26@qq.com")
                get_otc_info = "select * from otc.tb_otc_advert where member_id = %s and STATE != 90 order by STATE,CREATE_TIME desc limit %s,%s"
                otc_info = otc_mysql.getAll(get_otc_info,
                                            (member_id['member_id'], 0 + 20 * page_position, 20 + 20 * page_position))
                self.log.info("广告数量:{},广告详情:{}".format(len(otc_info), otc_info))
            except Exception as e:
                self.log.info(e)
            finally:
                otc_mysql.dispose()
            # 获取当前页面所有广告
            my_offers_elements = self.my_offers_driver.find_elements(self.my_offers_driver.div_my_offer)
            self.log.info("当前页面广告数量:{}".format(len(my_offers_elements)))
            for advert_position in range(len(my_offers_elements)):
                self.log.info("第{}个广告".format(advert_position + 1))
                # 获取每个广告div的text信息
                element_text = my_offers_elements[advert_position].text
                # 将text信息封装为列表
                my_offers_info = element_text.split('\n')
                self.log.info("my_offers_info:{}".format(my_offers_info))
                # 获取当前广告的支付方式
                try:
                    otc_advert_payment_way_mysql = MysqlPool("mysql")
                    get_payment_way = "select distinct EXCHANGE_WAY from otc.tb_otc_advert_payment_way where VALID=1 and ADVERT_ID = %s order by EXCHANGE_WAY;"
                    self.log.info("广告ID:{}".format(otc_info[advert_position]['ID']))
                    payment_way = otc_advert_payment_way_mysql.getAll(get_payment_way,
                                                                      (otc_info[advert_position]['ID'],))
                    # self.log.info("支付方式:{}".format(payment_way))
                except Exception as e:
                    self.log.info("获取广告方式".format(e))
                finally:
                    otc_advert_payment_way_mysql.dispose(otc_advert_payment_way_mysql)
                # 将广告信息与数据库表做断言
                # 判断广告方向
                if 'Buy offer' in my_offers_info[1]:
                    assert otc_info[advert_position]['SIDE'] == 1, "数据库中广告类型:{}，页面广告类型:{}".format(
                        otc_info[advert_position]['SIDE'], my_offers_info[1])
                elif 'Sell offer' in my_offers_info[1]:
                    assert otc_info[advert_position]['SIDE'] == 2, "数据库中广告类型:{}，页面广告类型:{}".format(
                        otc_info[advert_position]['SIDE'], my_offers_info[1])
                # 判断广告类型
                elif '(Float)' in my_offers_info[1]:
                    assert otc_info[advert_position]['BID_WAY'] == 1, "数据库中广告类型:{}，页面广告类型:{}".format(
                        otc_info[advert_position]['BID_WAY'], my_offers_info[1])
                elif '(Fixed)' in my_offers_info[1]:
                    assert otc_info[advert_position]['BID_WAY'] == 2, "数据库中广告类型:{}，页面广告类型:{}".format(
                        otc_info[advert_position]['BID_WAY'], my_offers_info[1])
                # 判断广告价格
                if otc_info[advert_position]['OFFLINE_COIN'] == 'USD':
                    assert my_offers_info[2] == str(otc_info[advert_position]['BID_PRICE'].quantize(
                        Decimal(
                            '0.0000'))), "页面价格:{},页面价格的数据类型:{},数据库价格:{},数据库价格的数据类型:{}".format(
                        my_offers_info[2],
                        type(my_offers_info[2]),
                        otc_info[advert_position][
                            'BID_PRICE'].quantize(
                            Decimal('0.0000')),
                        type(
                            otc_info[advert_position][
                                'BID_PRICE'].quantize(
                                Decimal('0.0000'))))
                elif otc_info[advert_position]['OFFLINE_COIN'] == 'HKD':
                    assert my_offers_info[2] == str(otc_info[advert_position]['BID_PRICE'].quantize(
                        Decimal(
                            '0.000'))), "页面价格:{},页面价格的数据类型:{},数据库价格:{},数据库价格的数据类型:{}".format(
                        my_offers_info[2],
                        type(my_offers_info[2]),
                        otc_info[advert_position][
                            'BID_PRICE'].quantize(
                            Decimal('0.000')),
                        type(
                            otc_info[advert_position][
                                'BID_PRICE'].quantize(
                                Decimal('0.000'))))
                else:
                    assert my_offers_info[2] == str(otc_info[advert_position]['BID_PRICE'].quantize(
                        Decimal(
                            '0.00'))), "页面价格:{},页面价格的数据类型:{},数据库价格:{},数据库价格的数据类型:{}".format(
                        my_offers_info[2],
                        type(my_offers_info[2]),
                        otc_info[advert_position][
                            'BID_PRICE'].quantize(
                            Decimal('0.00')),
                        type(
                            otc_info[advert_position][
                                'BID_PRICE'].quantize(
                                Decimal('0.00'))))
                # 判断广告币种
                assert "{}/{}".format(otc_info[advert_position]['OFFLINE_COIN'],
                                      otc_info[advert_position]['PLATFORM_COIN']) == my_offers_info[
                           3], "数据库中交易币种:{},页面交易币种:{}".format(
                    "{}/{}".format(otc_info[advert_position]['OFFLINE_COIN'],
                                   otc_info[advert_position]['PLATFORM_COIN']),
                    my_offers_info[3])
                # 判断广告限额
                assert "{}-{}".format(otc_info[advert_position]['EXCHANGE_MIN_VOLUMN'].quantize(Decimal('0')),
                                      otc_info[advert_position]['EXCHANGE_MAX_VOLUMN'].quantize(Decimal('0'))) == \
                       my_offers_info[4].translate(str.maketrans('', '', ',')), "数据库拼接广告限额:{},页面广告限额:{}".format(
                    "{}-{}".format(otc_info[advert_position]['EXCHANGE_MIN_VOLUMN'].quantize(Decimal('0')),
                                   otc_info[advert_position]['EXCHANGE_MAX_VOLUMN'].quantize(Decimal('0'))),
                    my_offers_info[4].translate(str.maketrans('', '', ',')))

                # 判断支付方式
                # 获取当前广告的支付方式列表
                payment_way_list = []
                for payment_way_info in payment_way:
                    payment_way_list.append(payment_way_info['EXCHANGE_WAY'])
                self.log.info("当前支付列表:{}".format(payment_way_list))
                # 支付方式列表
                payment_method = {1: 'Bank card', 2: 'Alipay', 3: 'WeChat', 4: 'PayPal', 5: 'FPS', 6: 'PayMe',
                                  7: 'Faspay',
                                  8: 'Line Pay', 9: 'Cash'}
                for payment_way_position in range(len(payment_way_list)):
                    assert my_offers_info[6 + payment_way_position] == payment_method[
                        payment_way_list[payment_way_position]], "数据库中支付方式:{},页面支付方式:{}".format(
                        payment_way_list[payment_way_position], my_offers_info[6 + payment_way_position])

                # 判断广告是否开启自动上下架
                if my_offers_info[-2] == 'Off':
                    # 判断广告交易时间
                    assert "{} minutes".format(otc_info[advert_position]['RESPONSE_MIN']) == str(
                        my_offers_info[-5]), "未开启自动上架的交易时间:数据库{},页面{}".format(
                        "{} minutes".format(otc_info[advert_position]['RESPONSE_MIN']),
                        my_offers_info[-5])
                    self.log.info("交易数:数据库{},页面{}".format(otc_info[advert_position]['TRADE_SUCCESS_COUNT'],
                                                          my_offers_info[-4]))
                    self.log.info(
                        "交易数类型:数据库{},页面{}".format(type(otc_info[advert_position]['TRADE_SUCCESS_COUNT']),
                                                  type(my_offers_info[-4])))
                    # 判断广告交易数
                    assert str(otc_info[advert_position]['TRADE_SUCCESS_COUNT']) == my_offers_info[
                        -4], "交易数:数据库{},页面{}".format(
                        otc_info[advert_position]['TRADE_SUCCESS_COUNT'],
                        my_offers_info[-4])
                else:
                    # 判断广告交易时间
                    assert "{} minutes".format(otc_info[advert_position]['RESPONSE_MIN']) == str(
                        my_offers_info[-6]), "自动上架的交易时间:数据库{},页面{}".format(
                        "{} minutes".format(otc_info[advert_position]['RESPONSE_MIN']),
                        my_offers_info[-6])
                    # 判断广告交易数
                    assert str(otc_info[advert_position]['TRADE_SUCCESS_COUNT']) == my_offers_info[
                        -5], "交易数:数据库{},页面{}".format(
                        otc_info[advert_position]['TRADE_SUCCESS_COUNT'],
                        my_offers_info[-5])

                # 判断广告是否开启自动上下架
                if my_offers_info[-2] == 'Off':
                    assert otc_info[advert_position]['AUTO_UP_OR_DOWN'] == 0, "数据库中广告自动上下架信息为:{}".format(
                        otc_info[advert_position]['AUTO_UP_OR_DOWN'])
                    # 判断广告是否上架
                    if otc_info[advert_position]['STATE'] == 10:
                        assert my_offers_info[-3] == 'on', "页面广告上架信息为:{}".format(my_offers_info[-3])
                    elif otc_info[advert_position]['STATE'] == 20:
                        assert my_offers_info[-3] == 'off', "页面广告上架信息为:{}".format(my_offers_info[-3])
                else:
                    assert otc_info[advert_position]['AUTO_UP_OR_DOWN'] == 1, "数据库中广告自动上下架信息为:{}".format(
                        otc_info[advert_position]['AUTO_UP_OR_DOWN'])
                    assert otc_info[advert_position]['JOB_UP_TIME'] in my_offers_info[-3], "数据库中广告自动上架时间为:{}".format(
                        otc_info[advert_position]['JOB_UP_TIME'])
                    assert otc_info[advert_position]['JOB_DOWN_TIME'] in my_offers_info[-2], "数据库中广告自动下架时间为:{}".format(
                        otc_info[advert_position]['JOB_DOWN_TIME'])
                    # 判断广告是否上架
                    if otc_info[advert_position]['STATE'] == 10:
                        assert my_offers_info[-4] == 'on', "页面广告上架信息为:{}".format(my_offers_info[-4])
                    elif otc_info[advert_position]['STATE'] == 20:
                        assert my_offers_info[-4] == 'off', "页面广告上架信息为:{}".format(my_offers_info[-4])
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_item_page_success(self):
        """测试点击页码功能"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为底端
        self.my_offers_driver.js_scroll_end()
        # 获得所有分页的数量
        elements = self.my_offers_driver.find_elements(self.my_offers_driver.li_page_item)
        page_account = len(elements)
        self.log.info("页码数量为:{}".format(page_account))
        # 获得上一页按钮
        prev_element = self.my_offers_driver.find_element(self.my_offers_driver.li_page_prev)
        # 获得下一页按钮
        next_element = self.my_offers_driver.find_element(self.my_offers_driver.li_page_next)
        # 获得不可点击按钮
        disabled_element = self.my_offers_driver.find_elements(self.my_offers_driver.li_page_disabled)
        # 判断不可点击按钮是否是首页
        assert prev_element in disabled_element
        # 判断当前选中的页码是否是第一页
        assert self.my_offers_driver.find_element(
            self.my_offers_driver.li_page_item_active).text == '1', "当前选中标签为:{}".format(
            self.my_offers_driver.find_element(self.my_offers_driver.li_page_item_active).text)
        if page_account == 1:
            assert prev_element in disabled_element
            assert next_element in disabled_element
        else:
            for page_position in range(page_account):
                self.log.info("第{}页".format(page_position + 1))
                elements[page_position].click()
                assert self.my_offers_driver.find_element(
                    self.my_offers_driver.li_page_item_active).text == str(page_position + 1), "当前选中标签为:{}".format(
                    self.my_offers_driver.find_element(self.my_offers_driver.li_page_item_active).text)
                time.sleep(5)
            # 判断不可点击按钮是否为下一页
            assert next_element in self.my_offers_driver.find_elements(self.my_offers_driver.li_page_disabled)
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_next_page_success(self):
        """测试点击下一页|上一页功能"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为底端
        self.my_offers_driver.js_scroll_end()
        # 获得所有分页的数量
        elements = self.my_offers_driver.find_elements(self.my_offers_driver.li_page_item)
        page_account = int(elements[len(elements)-1].text)
        self.log.info("页码数量为:{}".format(page_account))
        # 获得上一页按钮
        prev_element = self.my_offers_driver.find_element(self.my_offers_driver.li_page_prev)
        # 获得下一页按钮
        next_element = self.my_offers_driver.find_element(self.my_offers_driver.li_page_next)
        # 获得不可点击按钮
        disabled_element = self.my_offers_driver.find_elements(self.my_offers_driver.li_page_disabled)
        if page_account == 1:
            assert prev_element in disabled_element, "上一页不是不可点击标签"
            assert next_element in disabled_element, "下一页不是不可点击标签"
        else:
            for page_position in range(page_account - 1):
                next_element.click()
                assert self.my_offers_driver.find_element(
                    self.my_offers_driver.li_page_item_active).text == str(
                    page_position + 2), "当前选中标签为:{},页码应为:{}".format(
                    self.my_offers_driver.find_element(self.my_offers_driver.li_page_item_active).text,
                    page_position + 2)
            time.sleep(5)
            # 判断不可点击按钮是否为下一页
            assert next_element in self.my_offers_driver.find_elements(
                self.my_offers_driver.li_page_disabled), "下一页不是不可点击标签"
            for page_position in range(page_account - 1)[::-1]:
                prev_element.click()
                assert self.my_offers_driver.find_element(
                    self.my_offers_driver.li_page_item_active).text == str(
                    page_position + 1), "当前选中标签为:{},页码应为:{}".format(
                    self.my_offers_driver.find_element(self.my_offers_driver.li_page_item_active).text,
                    page_position + 1)
            time.sleep(5)
            # 判断不可点击按钮是否为上一页
            assert prev_element in self.my_offers_driver.find_elements(
                self.my_offers_driver.li_page_disabled), "上一页不是不可点击标签"
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_edit_button_success(self):
        """编辑按钮"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()
        # 获取第一条广告的信息
        try:
            edit_otc_mysql = MysqlPool("mysql")
            get_member_id = "select member_id from member.tm_member_identity where identity = %s "
            member_id = edit_otc_mysql.getOne(get_member_id, "lifq_user26@qq.com")
            get_otc_info = "select * from otc.tb_otc_advert where member_id = %s and STATE != 90 order by STATE,CREATE_TIME desc limit 1"
            otc_info = edit_otc_mysql.getAll(get_otc_info, (member_id['member_id'],))
            self.log.info("广告详情:{}".format(otc_info))
            pass
            # 点击第一条广告编辑按钮
        except Exception as e:
            self.log.info(e)
        finally:
            edit_otc_mysql.dispose()
        self.my_offers_driver.click(self.my_offers_driver.a_edit_offer)
        time.sleep(10)
        # 获取跳转后的URL
        edit_url = self.driver.current_url
        assert str(otc_info[0]['ID']) in edit_url, "数据库广告ID:{},跳转广告URL:{}".format(otc_info[0]['ID'], edit_url)
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_share_button_success(self):
        """分享按钮"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()
        # 点击分享按钮
        self.my_offers_driver.click(self.my_offers_driver.a_share_offer)
        result = self.my_offers_driver.get_text(self.my_offers_driver.vue_alert_success)
        assert result == "This ad link has been copied, you can share it with others"
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_delete_button_success(self):
        """删除按钮"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()
        # 获取第一条广告的信息
        try:
            delete_otc_mysql = MysqlPool("mysql")
            get_member_id = "select member_id from member.tm_member_identity where identity = %s "
            member_id = delete_otc_mysql.getOne(get_member_id, "lifq_user26@qq.com")
            get_otc_info = "select ID,STATE from otc.tb_otc_advert where member_id = %s and STATE != 90 order by STATE,CREATE_TIME desc limit 1"
            otc_info = delete_otc_mysql.getAll(get_otc_info, (member_id['member_id'],))
            otc_advert_id = otc_info[0]['ID']
        except Exception as e:
            self.log.info("获取广告信息数据库错误:{}".format(e))
        finally:
            delete_otc_mysql.dispose()
        # 点击第一条广告删除按钮
        self.my_offers_driver.click(self.my_offers_driver.a_delete_offer)
        time.sleep(5)
        # 获取删除提示框取消按钮
        alert_cancel_button_elements = self.my_offers_driver.find_elements(
            self.my_offers_driver.alert_cancel_button)
        time.sleep(5)
        # 点击取消按钮（第二个元素）
        alert_cancel_button_elements[len(alert_cancel_button_elements) - 1].click()
        time.sleep(5)
        try:
            delete_otc_cancel_mysql = MysqlPool("mysql")
            get_otc_cancel_status = "select STATE from otc.tb_otc_advert where ID = %s"
            otc_cancel_status = delete_otc_cancel_mysql.getOne(get_otc_cancel_status, otc_advert_id)
            assert otc_cancel_status['STATE'] == otc_info[0]['STATE'], "广告状态:{}".format(otc_info[0]['STATE'])
            time.sleep(5)
        except Exception as e:
            self.log.info("取消按钮数据库异常:{}".format(e))
        finally:
            delete_otc_cancel_mysql.dispose()

        # 再次点击第一条广告删除按钮
        self.my_offers_driver.click(self.my_offers_driver.a_delete_offer)
        # 获取删除提示框确认按钮
        alert_confirm_button_elements = self.my_offers_driver.find_elements(
            self.my_offers_driver.alert_confirm_button)
        time.sleep(5)
        # 点击确认按钮（第二个元素）
        alert_confirm_button_elements[len(alert_confirm_button_elements) - 1].click()
        time.sleep(5)
        try:
            delete_otc_confirm_mysql = MysqlPool("mysql")
            get_otc_confirm_status = "select STATE from otc.tb_otc_advert where ID = %s"
            otc_confirm_status = delete_otc_confirm_mysql.getOne(get_otc_confirm_status, otc_advert_id)
            assert otc_confirm_status['STATE'] == 90, "广告状态:{}".format(otc_confirm_status['STATE'])
        except Exception as e:
            self.log.info("确认按钮数据库异常:{}".format(e))
        finally:
            delete_otc_confirm_mysql.dispose()
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_type_buy_success(self):
        """根据广告种类筛选广告（全部/买/卖）"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()
        # 获取所有下拉列表框
        div_dropdown_elements = self.my_offers_driver.find_elements(self.my_offers_driver.div_dropdown_rel)
        # 获取全部按钮
        li_dropdown_elements = self.my_offers_driver.find_elements(self.my_offers_driver.li_dropdown_item)
        # 倒数第二个为广告种类下拉列表框,点击
        div_dropdown_elements[-2].click()
        time.sleep(5)
        # 点击买
        li_dropdown_elements[-5].click()
        time.sleep(5)
        # 获取当前页面所有广告
        my_offers_elements = self.my_offers_driver.find_elements(self.my_offers_driver.div_my_offer)
        for advert_position in range(len(my_offers_elements)):
            self.log.info("第{}个广告".format(advert_position + 1))
            # 获取每个广告div的text信息
            element_text = my_offers_elements[advert_position].text
            # 将text信息封装为列表
            my_offers_info = element_text.split('\n')
            self.log.info("my_offers_info:{}".format(my_offers_info))
            assert "Buy offer" in my_offers_info[1], "广告方向为:{},非买方广告".format(my_offers_info[1])
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_type_sell_success(self):
        """根据广告种类筛选广告（全部/买/卖）"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()
        # 获取所有下拉列表框
        div_dropdown_elements = self.my_offers_driver.find_elements(self.my_offers_driver.div_dropdown_rel)
        # 获取全部按钮
        li_dropdown_elements = self.my_offers_driver.find_elements(self.my_offers_driver.li_dropdown_item)
        # 倒数第二个为广告种类下拉列表框,点击
        div_dropdown_elements[-2].click()
        time.sleep(5)
        # 点击卖
        li_dropdown_elements[-4].click()
        time.sleep(5)
        # 获取当前页面所有广告
        my_offers_elements = self.my_offers_driver.find_elements(self.my_offers_driver.div_my_offer)
        for advert_position in range(len(my_offers_elements)):
            self.log.info("第{}个广告".format(advert_position + 1))
            # 获取每个广告div的text信息
            element_text = my_offers_elements[advert_position].text
            # 将text信息封装为列表
            my_offers_info = element_text.split('\n')
            self.log.info("my_offers_info:{}".format(my_offers_info))
            assert "Sell offer" in my_offers_info[1], "广告方向为:{},非卖方广告".format(my_offers_info[1])
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_status_off_success(self):
        """根据广告上下架筛选广告（下架）"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()
        # 获取所有下拉列表框
        div_dropdown_elements = self.my_offers_driver.find_elements(self.my_offers_driver.div_dropdown_rel)
        # 获取全部按钮
        li_dropdown_elements = self.my_offers_driver.find_elements(self.my_offers_driver.li_dropdown_item)
        # 倒数第一个为上下架类型下拉列表框,点击
        div_dropdown_elements[-1].click()
        time.sleep(5)
        # 点击下架
        li_dropdown_elements[-1].click()
        time.sleep(5)
        # 获取当前页面所有广告上下架状态
        my_offers_elements = self.my_offers_driver.find_elements(self.my_offers_driver.span_switch)
        for advert_position in range(len(my_offers_elements)):
            self.log.info("第{}个广告".format(advert_position + 1))
            # 获取每个广告状态的text信息
            element_text = my_offers_elements[advert_position].text
            self.log.info("element_text:{}".format(element_text))
            assert "off" == element_text, "广告上下架状态为:{},非下架广告".format(element_text)
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_status_on_success(self):
        """根据广告上下架筛选广告（已上架）"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()
        # 获取所有下拉列表框
        div_dropdown_elements = self.my_offers_driver.find_elements(self.my_offers_driver.div_dropdown_rel)
        # 获取全部按钮
        li_dropdown_elements = self.my_offers_driver.find_elements(self.my_offers_driver.li_dropdown_item)
        # 倒数第一个为上下架类型下拉列表框,点击
        div_dropdown_elements[-1].click()
        time.sleep(5)
        # 点击已上架
        li_dropdown_elements[-2].click()
        time.sleep(5)
        # 获取当前页面所有广告上下架状态
        my_offers_elements = self.my_offers_driver.find_elements(self.my_offers_driver.span_switch)
        for advert_position in range(len(my_offers_elements)):
            self.log.info("第{}个广告".format(advert_position + 1))
            # 获取每个广告状态的text信息
            element_text = my_offers_elements[advert_position].text
            self.log.info("element_text:{}".format(element_text))
            assert "on" == element_text, "广告上下架状态为:{},非上架广告".format(element_text)
        self.driver.refresh()
        time.sleep(5)

    def test_my_offers_click_status_button_success(self):
        """修改广告上下架状态"""
        # 登陆成功后跳转到广告列表页面
        self.login_driver.user_login_click_my_offers(self.login_driver)
        # 设置页面锚点为顶端
        self.my_offers_driver.js_scroll_top()
        # 获取所有上下架状态选择框
        switch_status_elements = self.my_offers_driver.find_elements(self.my_offers_driver.span_switch)
        # 随机获取任意广告
        switch_status_position = random.randint(0, len(switch_status_elements) - 1)
        # 获取该条广告的数据库信息
        try:
            otc_mysql = MysqlPool("mysql")
            get_member_id = "select member_id from member.tm_member_identity where identity = %s "
            member_id = otc_mysql.getOne(get_member_id, "lifq_user26@qq.com")
            get_otc_info = "select ID,STATE from otc.tb_otc_advert where member_id = %s and STATE != 90 order by STATE,CREATE_TIME desc"
            otc_info = otc_mysql.getAll(get_otc_info, (member_id['member_id'],))
            otc_info_state = otc_info[switch_status_position]['STATE']
            otc_info_id = otc_info[switch_status_position]['ID']
            self.log.info("STATE:{},ID:{}".format(otc_info_state, otc_info_id))
        except Exception as e:
            self.log.info("获取广告信息数据库错误:{}".format(e))
        finally:
            otc_mysql.dispose()
        # 获取该条广告的页面信息
        switch_status_element_text = switch_status_elements[switch_status_position].text
        self.log.info("页面广告上下架信息:{}".format(switch_status_element_text))
        if switch_status_element_text == "on":
            switch_status_elements[switch_status_position].click()
            time.sleep(5)
            assert "off" == switch_status_elements[switch_status_position].text, "页面广告信息".format(
                switch_status_elements[switch_status_position].text)
        elif switch_status_element_text == "off":
            switch_status_elements[switch_status_position].click()
            time.sleep(5)
            assert "on" == switch_status_elements[switch_status_position].text, "页面广告信息".format(
                switch_status_elements[switch_status_position].text)
        self.driver.refresh()
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
