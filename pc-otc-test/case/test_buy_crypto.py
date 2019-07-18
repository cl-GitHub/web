# coding:utf-8
import unittest
from common.base import set_options
from page.buycrypto import buy_crypto_url, BuyCryptoPage
from common.log import Log
import ddt
import os
from common.excelutil import Excel
from common.opmysql import MysqlPool
from page.login_page import LoginPage
import time

"""
初始化数据表 查询订单条件数据表
"""
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
excelPath = os.path.join(os.path.join(project_dir, 'data'), "login.xlsx")
buyCryptoSheetName = "购买查询条件数据表"
buy_crypto_excel = Excel(excelPath)
buy_crypto_data = buy_crypto_excel.get_list(buyCryptoSheetName, False)


@ddt.ddt
class TestBuyCrypto(unittest.TestCase):
    """测试购买页面"""

    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.buy_crypto_driver = BuyCryptoPage(cls.driver)
        cls.log = Log()
        cls.buy_crypto_driver.open(buy_crypto_url)

    @ddt.data(*buy_crypto_data)
    def test_default_info(self, data):
        """测试页面数据"""
        self.buy_crypto_driver.click(self.buy_crypto_driver.input_crypto)
        buy_crypto_elements = self.buy_crypto_driver.find_elements(self.buy_crypto_driver.li_crypto)
        # 设置广告方向和数字币种
        BuyCryptoPage.side_crypto(data, buy_crypto_elements)
        # 设置法币币种
        self.buy_crypto_driver.set_legal_currency(data, self.buy_crypto_driver)
        # 校验文案
        if data['Type'] == 'Buy':
            assert self.buy_crypto_driver.find_element(self.buy_crypto_driver.h2_buy_crypto).text in (
                "Use {} To Buy {}".format(data['Currency'], data['Crypto']),
                "使用 {} 購買 {}".format(data['Currency'], data['Crypto']),
                "使用 {} 购买 {}".format(data['Currency'], data['Crypto']))
        elif data['Type'] == 'Sell':
            assert self.buy_crypto_driver.find_element(self.buy_crypto_driver.h2_buy_crypto).text in (
                "Sell {} To Get {}".format(data['Crypto'], data['Currency']),
                "出售 {} 換取 {}".format(data['Crypto'], data['Currency']),
                "出售 {} 换取 {}".format(data['Crypto'], data['Currency']))

        # 校验广告参数
        tr_adverts_elements = self.buy_crypto_driver.find_elements(self.buy_crypto_driver.tr_adverts)
        get_adverts_info_sql = ""
        try:
            my_adverts_mysql = MysqlPool("mysql")
            if data['Type'] == 'Buy':
                get_adverts_info_sql = "select ID,MEMBER_ID,TITLE,PLATFORM_COIN,OFFLINE_COIN,EXCHANGE_MAX_VOLUMN,EXCHANGE_MIN_VOLUMN,BID_PRICE from otc.tb_otc_advert where side =2 and PLATFORM_COIN=%s and OFFLINE_COIN=%s and STATE=10 order by BID_PRICE;"
            elif data['Type'] == 'Sell':
                get_adverts_info_sql = "select ID,MEMBER_ID,TITLE,PLATFORM_COIN,OFFLINE_COIN,EXCHANGE_MAX_VOLUMN,EXCHANGE_MIN_VOLUMN,BID_PRICE from otc.tb_otc_advert where side =1 and PLATFORM_COIN=%s and OFFLINE_COIN=%s and STATE=10 order by BID_PRICE desc;"
            adverts_info_list = my_adverts_mysql.getAll(get_adverts_info_sql, (
                data['Crypto'], data['Currency']))
        except Exception as e:
            self.log.info(e)
        finally:
            my_adverts_mysql.dispose()
        if len(tr_adverts_elements) > 1:
            for tr_adverts_element_position in range(1, len(tr_adverts_elements)):
                tr_web_adverts_info = tr_adverts_elements[tr_adverts_element_position].text.split('\n')
                tr_sql_adverts_info = adverts_info_list[tr_adverts_element_position - 1]
                self.log.info(tr_web_adverts_info)
                self.log.info(tr_sql_adverts_info)
                try:
                    exchange_way_mysql = MysqlPool("mysql")
                    get_exchange_way_sql = "select distinct (EXCHANGE_WAY) from otc.tb_otc_advert_payment_way where ADVERT_ID =%s order by EXCHANGE_WAY;"
                    exchange_way_list = exchange_way_mysql.getAll(get_exchange_way_sql, (
                        tr_sql_adverts_info['ID'],))
                    get_member_name_sql = "select member_name from member.tm_member where MEMBER_ID = %s;"
                    member_name = exchange_way_mysql.getOne(get_member_name_sql, (tr_sql_adverts_info['MEMBER_ID'],))
                    self.log.info(exchange_way_list)
                    self.log.info(member_name)
                    self.buy_crypto_driver.check_data(member_name, exchange_way_list, tr_sql_adverts_info,
                                                      tr_web_adverts_info)
                except Exception as e:
                    self.log.info(e)
                finally:
                    exchange_way_mysql.dispose()
        else:
            assert adverts_info_list == False

    def test_not_login_click_buy(self):
        """测试未登陆用户点击购买按钮CASE"""
        tr_adverts_elements = self.buy_crypto_driver.find_elements(self.buy_crypto_driver.tr_adverts)
        if len(tr_adverts_elements) > 1:
            # 点击第一条广告的去购买列表
            self.buy_crypto_driver.click(self.buy_crypto_driver.frist_advert)
            # 获取URL并断言
            assert self.driver.current_url == "http://wex.test.tigerft.com/login"
        else:
            self.log.info('\033[0;32m 当前页面无广告')

    def test_not_login_click_member_name(self):
        """测试未登陆用户点击广告主名称CASE"""
        tr_adverts_elements = self.buy_crypto_driver.find_elements(self.buy_crypto_driver.tr_adverts)
        if len(tr_adverts_elements) > 1:
            # 点击第一条广告的去购买列表
            self.buy_crypto_driver.click(self.buy_crypto_driver.frist_advert_name)
            # 获取URL并断言
            assert self.driver.current_url == "http://wex.test.tigerft.com/login"
        else:
            self.log.info('\033[0;32m 当前页面无广告')

    def test_login_click_buy(self):
        """已登陆用户点击广告CASE"""
        login_driver = LoginPage(self.driver)
        login_driver.user_login(login_driver, "lifq_user26@qq.com", "ab1234567")
        time.sleep(5)
        self.buy_crypto_driver.open(buy_crypto_url)
        tr_adverts_elements = self.buy_crypto_driver.find_elements(self.buy_crypto_driver.tr_adverts)
        if len(tr_adverts_elements) > 1:
            # 点击第一条广告的去购买列表
            self.buy_crypto_driver.click(self.buy_crypto_driver.frist_advert)
            try:
                my_adverts_mysql = MysqlPool("mysql")
                get_adverts_info_sql = "select ID from otc.tb_otc_advert where side =2 and PLATFORM_COIN='USDT' and OFFLINE_COIN='HKD' and STATE=10 order by BID_PRICE;"
                adverts_info = my_adverts_mysql.getOne(get_adverts_info_sql)
            except Exception as e:
                self.log.info(e)
            finally:
                my_adverts_mysql.dispose()
            assert str(adverts_info['ID']) in self.driver.current_url, "数据库广告ID:{},URL:{}".format(adverts_info['ID'],
                                                                                                  self.driver.current_url)
        else:
            self.log.info('\033[0;32m 当前页面无广告')
        login_driver.user_logout(login_driver)

    def test_large_order(self):
        """测试大额订单跳转"""
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
