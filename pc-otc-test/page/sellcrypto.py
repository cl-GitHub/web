# coding:utf-8
sell_crypto_url = "http://wex.test.tigerft.com/market/sell"
from common.base import BasePage
from common.base import browser
from common.logeventlistener import LogEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
import re
from common.digitalprocess import get_amount, get_float


class SellCryptoPage(BasePage):
    """购买页面"""
    # 数字币选择下拉列表框
    input_crypto = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/div/div/div[1]/div[1]/div[1]/input')
    # 数字币币种与广告方向
    ul_crypto = ("class name", 'ivu-cascader-menu')
    li_crypto = ("class name", 'ivu-cascader-menu-item')
    # 法币币种下拉选择框
    div_legal_currency = ('xpath', '//*[@id="app"]/main/div/div/div/div[1]/div/div/div[2]/div[1]/div/span')
    # 法币币种
    ul_legal_currency = ("class name", 'ivu-select-dropdown-list')
    li_hkd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/div/div/div[2]/div[2]/ul[2]/li[1]')
    li_twd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/div/div/div[2]/div[2]/ul[2]/li[2]')
    li_usd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/div/div/div[2]/div[2]/ul[2]/li[3]')
    li_idr = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/div/div/div[2]/div[2]/ul[2]/li[4]')
    li_vnd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/div/div/div[2]/div[2]/ul[2]/li[5]')
    li_khr = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/div/div/div[2]/div[2]/ul[2]/li[6]')
    # 购买页面标题
    h2_sell_crypto = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/h2')
    # 广告列表
    tr_adverts = ("tag name", 'tr')
    # 第一条广告
    frist_advert = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/div/table/tbody/tr[1]/td[5]/button')
    # 第一个广告主名称
    frist_advert_name = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/div/table/tbody/tr[1]/td[1]/h2')

    def __init__(self, driver):
        super().__init__(EventFiringWebDriver(driver, LogEventListener()))
        # 支付方式列表
        self.payment_method = {1: 'Bank card', 2: 'Alipay', 3: 'WeChat', 4: 'PayPal', 5: 'FPS', 6: 'PayMe', 7: 'Faspay',
                               8: 'Line Pay', 9: 'Cash'}

    @staticmethod
    def side_crypto(data, sell_crypto_elements):
        """选择数字币币和广告方向
        :param data:数据源
        :param sell_crypto_elements:元素集
        """
        if data['Type'] == 'Buy':
            sell_crypto_elements[0].click()
            if data['Crypto'] == 'USDT':
                sell_crypto_elements[2].click()
            elif data['Crypto'] == 'USDC':
                sell_crypto_elements[3].click()
            elif data['Crypto'] == 'TUSD':
                sell_crypto_elements[4].click()
        else:
            sell_crypto_elements[1].click()
            if data['Crypto'] == 'USDT':
                sell_crypto_elements[2].click()
            elif data['Crypto'] == 'USDC':
                sell_crypto_elements[3].click()
            elif data['Crypto'] == 'TUSD':
                sell_crypto_elements[4].click()

    def set_legal_currency(self, data, sell_crypto_driver):
        """选择法币
        :param data:数据源
        :param sell_crypto_driver:webdriver
        """
        if data['Currency'] == 'HKD':
            sell_crypto_driver.click_ul_li(self.div_legal_currency, self.ul_legal_currency, self.li_hkd, is_move=False)
        elif data['Currency'] == 'TWD':
            sell_crypto_driver.click_ul_li(self.div_legal_currency, self.ul_legal_currency, self.li_twd, is_move=False)
        elif data['Currency'] == 'USD':
            sell_crypto_driver.click_ul_li(self.div_legal_currency, self.ul_legal_currency, self.li_usd, is_move=False)
        elif data['Currency'] == 'IDR':
            sell_crypto_driver.click_ul_li(self.div_legal_currency, self.ul_legal_currency, self.li_idr, is_move=False)
        elif data['Currency'] == 'VND':
            sell_crypto_driver.click_ul_li(self.div_legal_currency, self.ul_legal_currency, self.li_vnd, is_move=False)
        elif data['Currency'] == 'KHR':
            sell_crypto_driver.click_ul_li(self.div_legal_currency, self.ul_legal_currency, self.li_khr, is_move=False)

    def check_data(self, member_name, exchange_way_list, tr_sql_adverts_info, tr_web_adverts_info):
        # 判断广告主名称
        assert member_name == tr_web_adverts_info[0]
        # 判断交易方式
        self.check_exchange_way(exchange_way_list, tr_web_adverts_info[2])
        # 判断标题
        assert tr_sql_adverts_info['TITLE'] == tr_web_adverts_info[3]
        # 判断法币币种
        assert tr_sql_adverts_info['OFFLINE_COIN'] == tr_web_adverts_info[5]
        # 判断交易价格
        if tr_sql_adverts_info['OFFLINE_COIN'] == 'HKD':
            assert get_float(tr_sql_adverts_info['BID_PRICE'], 3) == tr_web_adverts_info[6]
        elif tr_sql_adverts_info['OFFLINE_COIN'] == 'USD':
            assert get_float(tr_sql_adverts_info['BID_PRICE'], 4) == tr_web_adverts_info[6]
        else:
            assert get_float(tr_sql_adverts_info['BID_PRICE'], 2) == tr_web_adverts_info[6]
        # 判断交易单位
        assert "{}/{}".format(tr_sql_adverts_info['OFFLINE_COIN'], tr_sql_adverts_info['PLATFORM_COIN']) == \
               tr_web_adverts_info[7]

    def check_exchange_way(self, exchange_way_list, tr_web_exchange_way_info):
        for exchange_way in exchange_way_list:
            assert self.payment_method[exchange_way['EXCHANGE_WAY']] in tr_web_exchange_way_info
