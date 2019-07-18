# coding:utf-8
import os
from common.excelutil import Excel
import unittest
import ddt
from common.base import set_options
from page.postanoffer import PostAnOfferPage
from page.login_page import LoginPage, login_url
from common.log import Log
import time

"""
初始化数据表 发布广告成功数据表
"""
project_dir = os.path.dirname(os.path.abspath('.'))
excelPath = project_dir + '/pc-otc-test/data/login.xlsx'
"""如果测试单个test"""
# excelPath = project_dir + '/data/login.xlsx'
postAnOfferSuccessSheetName = "发布广告成功数据表"
post_an_offer_excel = Excel(excelPath)
post_an_offer_success_data = post_an_offer_excel.get_list(postAnOfferSuccessSheetName, False)
postAnOfferFailSheetName = "发布广告失败数据表"
post_an_offer_fail_data = post_an_offer_excel.get_list(postAnOfferFailSheetName, False)


@ddt.ddt
class TestPostAnOffer(unittest.TestCase):
    """测试发布广告"""

    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.login_driver = LoginPage(cls.driver)
        cls.login_driver.open(login_url)
        cls.login_driver.user_login(cls.login_driver, 'lifq_user26@qq.com', 'ab1234567')
        cls.find_pwd_driver = PostAnOfferPage(cls.driver)
        cls.log = Log()

    @ddt.data(*post_an_offer_success_data)
    def test_post_an_offer_success(self, data):

        """测试内容:发布成功一条广告
           准备数据:数字币、收款方式"""
        self.log.info(
            "测试数据(用户名:{},密码:{},广告类型:{},数字币种:{},标题:{},价格类型:{},法币币种:{},浮动比例:{},接受价格:{},最小额度:{},最大额度:{},付款时限:{},是否接受大额预约:{},大额预约额度:{},付款时限:{},交易说明:{},是否显示高级选项:{},自动回复:{},对手成交次数:{},是否开启自动上下架:{})".format(
                data['Username'], data['Password'], data['OfferType'], data['Crypto'], data['OfferTitle'],
                data['PriceSetting'], data['SelectCurrency'], data['FloatingRate'], data['AcceptablePrice'],
                data['MinimumVolume'], data['MaximumVolume'], data['PaymentTimeLimit'],
                data['AcceptTheLargeTrading'], data['LargeTradingMaximumVolume'],
                data['LargeTradingPaymentTimeLimit'], data['TradeInstructions'], data['AdvanceOptions'],
                data['AutoReply'], data['RestrictionsMeans'], data['AutoPublish']))
        time.sleep(10)
        # 登陆成功后跳转到发布广告页面
        self.login_driver.user_login_click_post_an_offer(self.login_driver)
        time.sleep(10)
        # 设置页面锚点为顶端
        self.find_pwd_driver.js_scroll_top()
        time.sleep(10)
        # 选择出售&购买广告
        if data['OfferType'] == 'sell':
            self.find_pwd_driver.click(self.find_pwd_driver.sell_loc)
        else:
            self.find_pwd_driver.click(self.find_pwd_driver.buy_loc)
        # 数字币下拉列表框，position范围[0,2]，选择USDC
        if data['Crypto'] == 'USDT':
            self.find_pwd_driver.click_li(self.find_pwd_driver.crypto_loc,
                                          self.find_pwd_driver.li_crypto_loc, is_move=False)
        elif data['Crypto'] == 'USDC':
            self.find_pwd_driver.click_li(self.find_pwd_driver.crypto_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=1, is_move=False)
        elif data['Crypto'] == 'TUSD':
            self.find_pwd_driver.click_li(self.find_pwd_driver.crypto_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=2, is_move=False)
        self.find_pwd_driver.send_keys(self.find_pwd_driver.offer_title_loc, data['OfferTitle'])
        # 选择浮动价格
        if data['PriceSetting'] == 'Fixed':
            self.find_pwd_driver.click(self.find_pwd_driver.fixed_price_loc)
        elif data['PriceSetting'] == 'Floating':
            self.find_pwd_driver.click(self.find_pwd_driver.floating_price_loc)
        time.sleep(10)
        # 设置浮动比例
        if data['PriceSetting'] == 'Floating' and data['FloatingRate'] == 'up':
            self.find_pwd_driver.click(self.find_pwd_driver.a_float_rate_up_loc)
        elif data['PriceSetting'] == 'Floating' and data['FloatingRate'] == 'down':
            self.find_pwd_driver.click(self.find_pwd_driver.a_float_rate_down_loc)
        # 法币下拉列表框，position范围[3,8]，选择USD
        if data['SelectCurrency'] == 'HKD':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=3, is_move=False)
        elif data['SelectCurrency'] == 'USD':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=4, is_move=False)
        elif data['SelectCurrency'] == 'TWD':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=5, is_move=False)
        elif data['SelectCurrency'] == 'IDR':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=6, is_move=False)
        elif data['SelectCurrency'] == 'VND':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=7, is_move=False)
        elif data['SelectCurrency'] == 'KHR':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=8, is_move=False)
        time.sleep(10)
        # 设置最低或最高报价
        if data['AcceptablePrice'] is not '' and data['PriceSetting'] == 'Floating':
            self.find_pwd_driver.send_keys(self.find_pwd_driver.input_acceptable_price, str(data['AcceptablePrice']))
        # 设置最小额度
        self.find_pwd_driver.send_keys(self.find_pwd_driver.input_minimum_volume, str(data['MinimumVolume']))
        # 设置最大额度
        self.find_pwd_driver.send_keys(self.find_pwd_driver.input_maximum_volume, str(data['MaximumVolume']))
        # 设置交易时间
        self.find_pwd_driver.send_keys(self.find_pwd_driver.input_payment_time_limit, str(data['PaymentTimeLimit']))
        # 输入交易说明
        if data['OfferType'] == 'sell' and data['TradeInstructions'] is not '':
            if data['Crypto'] == 'USDT':
                self.find_pwd_driver.send_keys(self.find_pwd_driver.usdt_textarea_trade_instructions,
                                               data['TradeInstructions'])
            elif data['Crypto'] == 'USDC' or data['Crypto'] == 'TUSD':
                self.find_pwd_driver.send_keys(self.find_pwd_driver.other_textarea_trade_instructions,
                                               data['TradeInstructions'])
                # js = "document.getElementsByClassName(\"ivu-input\")[2].value=\"{}\"".format(data['TradeInstructions'])
                # self.find_pwd_driver.js_execute(js)
        elif data['OfferType'] == 'buy' and data['TradeInstructions'] is not '':
            self.find_pwd_driver.send_keys(self.find_pwd_driver.other_textarea_trade_instructions,
                                           data['TradeInstructions'])
        time.sleep(10)
        # 设置接收大额交易
        if data['OfferType'] == 'sell' and data['AcceptTheLargeTrading'] == 'on':
            # print(self.find_pwd_driver.find_element(self.find_pwd_driver.label_accept_large_trade_on))
            self.find_pwd_driver.click(self.find_pwd_driver.label_accept_large_trade_on)
            time.sleep(10)
            if data['LargeTradingMaximumVolume'] is not '':
                self.find_pwd_driver.send_keys(self.find_pwd_driver.input_large_trade_trade_limit,
                                               data['LargeTradingMaximumVolume'])
                time.sleep(10)
            if data['LargeTradingPaymentTimeLimit'] is not '':
                self.find_pwd_driver.send_keys(self.find_pwd_driver.input_large_trade_payment_time_limit,
                                               data['LargeTradingPaymentTimeLimit'])
        time.sleep(10)
        # 设置显示高级选项
        if data['AdvanceOptions'] == 'on':
            advance_options = self.find_pwd_driver.find_element(self.find_pwd_driver.i_advance_options)
            advance_options.click()
            time.sleep(10)
            if data['AutoReply'] is not '':
                auto_reply_elements = self.find_pwd_driver.find_elements(self.find_pwd_driver.textarea_auto_reply)
                # print(auto_reply_elements)
                auto_reply_elements[len(auto_reply_elements) - 1].send_keys(data['AutoReply'])
                # self.find_pwd_driver.send_keys(self.find_pwd_driver.textarea_auto_reply, data['AutoReply'])
                # js = "document.getElementsByClassName(\"ivu-input\")[3].value=\"{}\"".format(data['AutoReply'])
                # self.find_pwd_driver.js_execute(js)
                time.sleep(10)
            if data['RestrictionsMeans'] is not '':
                number_input_elements = self.find_pwd_driver.find_elements(self.find_pwd_driver.input_restrictions)
                # self.log.info("元素列表长度为{}".format(len(number_input_elements)))
                number_input_elements[len(number_input_elements) - 1].send_keys(data['RestrictionsMeans'])
        time.sleep(10)
        # 设置广告自动上下架
        if data['OfferType'] == 'sell' and data['AutoPublish'] == 'on':
            if data['Crypto'] == 'USDT':
                self.find_pwd_driver.click(self.find_pwd_driver.usdt_label_auto_publish_on)
            elif data['Crypto'] == 'USDC' or data['Crypto'] == 'TUSD':
                self.find_pwd_driver.click(self.find_pwd_driver.other_label_auto_publish_on)
        elif data['OfferType'] == 'buy' and data['AutoPublish'] == 'on':
            self.find_pwd_driver.click(self.find_pwd_driver.other_label_auto_publish_on)
        time.sleep(10)
        # 点击发布广告
        self.find_pwd_driver.click(self.find_pwd_driver.span_post_an_offer)
        time.sleep(10)
        # 断言（广告类型、价格、交易限额、付款时限、自动上下架）
        result = self.find_pwd_driver.get_text(self.find_pwd_driver.div_first_offer)
        self.log.info("广告信息：{}".format(result))
        self.log.info(
            "断言数据：（广告类型:{},交易限额:{},交易币种:{}付款时限:{},广告上下架:{},自动上下架:{}".format(data['ExceptType'],
                                                                            data['ExceptTradingLimit'],
                                                                            data['ExceptUnit'],
                                                                            data['ExceptPaymentTimeLimit'],
                                                                            data['ExceptStatus'],
                                                                            data['ExceptAutoPublish']))
        if data['ExceptType'] is not '':
            assert data['ExceptType'] in result
        if data['ExceptTradingLimit'] is not '':
            assert data['ExceptTradingLimit'] in result
        if data['ExceptUnit'] is not '':
            assert data['ExceptUnit'] in result
        if data['ExceptPaymentTimeLimit'] is not '':
            assert data['ExceptPaymentTimeLimit'] in result
        if data['ExceptStatus'] is not '':
            assert data['ExceptStatus'] in result
        if data['ExceptAutoPublish'] is not '':
            assert data['ExceptAutoPublish'] in result
        time.sleep(10)
        self.find_pwd_driver.click(self.find_pwd_driver.a_del_offer)
        time.sleep(10)
        # 获取确认按钮
        confirm_elements = self.find_pwd_driver.find_elements(self.find_pwd_driver.button_confirm)
        time.sleep(10)
        # 多个确认按钮中，索引为1的是删除广告确认按钮
        confirm_elements[len(confirm_elements) - 1].click()
        time.sleep(10)

    @ddt.data(*post_an_offer_fail_data)
    def test_post_an_offer_fail(self, data):
        """测试内容:发布失败一条广告
           准备数据:数字币、收款方式"""
        self.log.info(
            "测试数据(广告类型:{},数字币种:{},标题:{},价格类型:{},法币币种:{},浮动比例:{},接受价格:{},最小额度:{},最大额度:{},付款时限:{},是否接受大额预约:{},大额预约额度:{},付款时限:{},交易说明:{},是否显示高级选项:{},自动回复:{},对手成交次数:{},是否开启自动上下架:{})".format(
                data['OfferType'], data['Crypto'], data['OfferTitle'],
                data['PriceSetting'], data['SelectCurrency'], data['FloatingRate'], data['AcceptablePrice'],
                data['MinimumVolume'], data['MaximumVolume'], data['PaymentTimeLimit'],
                data['AcceptTheLargeTrading'], data['LargeTradingMaximumVolume'],
                data['LargeTradingPaymentTimeLimit'], data['TradeInstructions'], data['AdvanceOptions'],
                data['AutoReply'], data['RestrictionsMeans'], data['AutoPublish']))
        time.sleep(10)
        # 登陆成功后跳转到发布广告页面
        self.login_driver.user_login_click_post_an_offer(self.login_driver)
        time.sleep(10)
        # 设置页面锚点为顶端
        self.find_pwd_driver.js_scroll_top()
        time.sleep(10)
        # 选择出售&购买广告
        if data['OfferType'] == 'sell':
            self.find_pwd_driver.click(self.find_pwd_driver.sell_loc)
        else:
            self.find_pwd_driver.click(self.find_pwd_driver.buy_loc)
        time.sleep(10)
        # 设置广告标题
        if data['OfferTitle'] is not '':
            self.find_pwd_driver.send_keys(self.find_pwd_driver.offer_title_loc, data['OfferTitle'])
        # 数字币下拉列表框，position范围[0,2]，选择USDC
        if data['Crypto'] == 'USDT':
            self.find_pwd_driver.click_li(self.find_pwd_driver.crypto_loc,
                                          self.find_pwd_driver.li_crypto_loc, is_move=False)
        elif data['Crypto'] == 'USDC':
            self.find_pwd_driver.click_li(self.find_pwd_driver.crypto_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=1, is_move=False)
        elif data['Crypto'] == 'TUSD':
            self.find_pwd_driver.click_li(self.find_pwd_driver.crypto_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=2, is_move=False)
        self.find_pwd_driver.send_keys(self.find_pwd_driver.offer_title_loc, data['OfferTitle'])
        # 选择浮动价格
        if data['PriceSetting'] == 'Fixed':
            self.find_pwd_driver.click(self.find_pwd_driver.fixed_price_loc)
        elif data['PriceSetting'] == 'Floating':
            self.find_pwd_driver.click(self.find_pwd_driver.floating_price_loc)
        time.sleep(10)
        # 设置浮动比例
        if data['PriceSetting'] == 'Floating' and data['FloatingRate'] == 'up':
            self.find_pwd_driver.click(self.find_pwd_driver.a_float_rate_up_loc)
        elif data['PriceSetting'] == 'Floating' and data['FloatingRate'] == 'down':
            self.find_pwd_driver.click(self.find_pwd_driver.a_float_rate_down_loc)
        # 法币下拉列表框，position范围[3,8]，选择USD
        if data['SelectCurrency'] == 'HKD':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=3, is_move=False)
        elif data['SelectCurrency'] == 'USD':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=4, is_move=False)
        elif data['SelectCurrency'] == 'TWD':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=5, is_move=False)
        elif data['SelectCurrency'] == 'IDR':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=6, is_move=False)
        elif data['SelectCurrency'] == 'VND':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=7, is_move=False)
        elif data['SelectCurrency'] == 'KHR':
            self.find_pwd_driver.click_li(self.find_pwd_driver.select_currency_loc,
                                          self.find_pwd_driver.li_crypto_loc, position=8, is_move=False)
        time.sleep(10)
        # 设置最低或最高报价
        if data['AcceptablePrice'] is not '' and data['PriceSetting'] == 'Floating':
            self.find_pwd_driver.send_keys(self.find_pwd_driver.input_acceptable_price,
                                           str(data['AcceptablePrice']))
        # 设置最小限额
        if data['MinimumVolume'] is not '':
            self.find_pwd_driver.send_keys(self.find_pwd_driver.input_minimum_volume, data['MinimumVolume'])
        else:
            self.find_pwd_driver.find_element(self.find_pwd_driver.input_minimum_volume).clear()
        # 设置最大限额
        if data['MaximumVolume'] is not '':
            self.find_pwd_driver.send_keys(self.find_pwd_driver.input_maximum_volume, data['MaximumVolume'])
        else:
            self.find_pwd_driver.find_element(self.find_pwd_driver.input_maximum_volume).clear()
        # 设置交易时间
        self.find_pwd_driver.send_keys(self.find_pwd_driver.input_payment_time_limit, str(data['PaymentTimeLimit']))
        # 输入交易说明
        if data['OfferType'] == 'sell' and data['TradeInstructions'] is not '':
            if data['Crypto'] == 'USDT':
                self.find_pwd_driver.send_keys(self.find_pwd_driver.usdt_textarea_trade_instructions,
                                               data['TradeInstructions'])
            elif data['Crypto'] == 'USDC' or data['Crypto'] == 'TUSD':
                self.find_pwd_driver.send_keys(self.find_pwd_driver.other_textarea_trade_instructions,
                                               data['TradeInstructions'])
                # js = "document.getElementsByClassName(\"ivu-input\")[2].value=\"{}\"".format(data['TradeInstructions'])
                # self.find_pwd_driver.js_execute(js)
        elif data['OfferType'] == 'buy' and data['TradeInstructions'] is not '':
            self.find_pwd_driver.send_keys(self.find_pwd_driver.other_textarea_trade_instructions,
                                           data['TradeInstructions'])
        time.sleep(10)
        # 设置接收大额交易
        if data['OfferType'] == 'sell' and data['AcceptTheLargeTrading'] == 'on':
            # print(self.find_pwd_driver.find_element(self.find_pwd_driver.label_accept_large_trade_on))
            self.find_pwd_driver.click(self.find_pwd_driver.label_accept_large_trade_on)
            time.sleep(10)
            if data['LargeTradingMaximumVolume'] is not '':
                self.find_pwd_driver.send_keys(self.find_pwd_driver.input_large_trade_trade_limit,
                                               data['LargeTradingMaximumVolume'])
                time.sleep(10)
            if data['LargeTradingPaymentTimeLimit'] is not '':
                self.find_pwd_driver.send_keys(self.find_pwd_driver.input_large_trade_payment_time_limit,
                                               data['LargeTradingPaymentTimeLimit'])
        time.sleep(10)
        # 点击发布广告
        self.find_pwd_driver.click(self.find_pwd_driver.span_post_an_offer)
        if data['OfferType'] == 'buy':
            buy_error_elements = self.find_pwd_driver.find_elements(self.find_pwd_driver.error_offer_title)
            for element in buy_error_elements:
                self.log.info(element.text)
            self.log.info("elements 详情{},数量{}".format(buy_error_elements, len(buy_error_elements)))
            assert data['ExceptResult'] == buy_error_elements[0].text
        elif data['OfferType'] == 'sell':
            sell_error_elements = self.find_pwd_driver.find_elements(self.find_pwd_driver.error_offer_title)
            for element in sell_error_elements:
                self.log.info(element.text)
            self.log.info("elements 详情{},数量{}".format(sell_error_elements, len(sell_error_elements)))
            assert data['ExceptResult'] == sell_error_elements[0].text
        self.driver.refresh()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
    suit = unittest.TestSuite()
    suit.addTest(TestPostAnOffer("test_post_an_offer_fail"))  # 把这个类中需要执行的测试用例加进去，有多条再加即可
    runner = unittest.TextTestRunner()
    runner.run(suit)
