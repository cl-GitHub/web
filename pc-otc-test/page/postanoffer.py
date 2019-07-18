# coding:utf-8
post_an_offer_url = "http://wex.test.tigerft.com/advert/buy"
from common.base import BasePage
from selenium import webdriver
from common.base import browser
import time

# 加载配置项
options = webdriver.ChromeOptions()
options.add_argument('--disable-infobars')
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)


class PostAnOfferPage(BasePage):
    """发布广告页面"""
    # 我想要 出售
    sell_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[1]/div[2]/div[1]/div/span[1]')
    # 我想要 购买
    buy_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[1]/div[2]/div[1]/div/span[2]')
    # 我想要 数字币下拉列表框
    crypto_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[1]/div[2]/div[2]/div/div')
    # 下拉列表框中li元素
    li_crypto_loc = ("class name", "ivu-select-item")
    # 广告标题
    offer_title_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[2]/div[2]/div/div/div/input')
    # 价格设置 固定
    fixed_price_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[3]/div[2]/div[1]/div/div/div/label[1]')
    # 价格设置 浮动
    floating_price_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[3]/div[2]/div[1]/div/div/div/label[2]')
    # 交易币种下拉列表框
    select_currency_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[3]/div[2]/div[2]/div[1]/div[2]/div/div')
    # 浮动比例 +
    a_float_rate_up_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[3]/div[2]/div[2]/div[4]/div[2]/div/div['
                                    '1]/a[1]')
    # 浮动比例 -
    a_float_rate_down_loc = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[3]/div[2]/div[2]/div[4]/div['
                                      '2]/div/div[1]/a[2]')
    # 您的报价
    input_your_offer = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[3]/div[2]/div[2]/div[4]/div[2]/div/div/div/div/div[2]/input')
    # 最低/最高报价
    input_acceptable_price = ("xpath", '//*[@id="InputNumber"]/div[2]/input')
    # 最小限额
    input_minimum_volume = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[5]/div[2]/div[1]/div/div/div[1]/div[2]/input')
    # 最大限额
    input_maximum_volume = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[5]/div[2]/div[2]/div/div/div[1]/div[2]/input')
    # 付款时限
    input_payment_time_limit = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[6]/div[2]/div/div/div/div[2]/input')
    # 发布USDT广告交易说明
    usdt_textarea_trade_instructions = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[8]/div[2]/div/textarea')
    # 发布其他广告交易说明
    other_textarea_trade_instructions = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[7]/div[2]/div/textarea')
    # 自动上下架 开启
    other_label_auto_publish_on = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[10]/div[2]/div/div/div/div/label[1]')
    usdt_label_auto_publish_on = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[11]/div[2]/div/div/div/div/label[1]')
    # 自动上下架 关闭
    other_label_auto_publish_off = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[10]/div[2]/div/div/div/div/label[2]')
    usdt_label_auto_publish_off = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[11]/div[2]/div/div/div/div/label[2]')
    # 是否以广告价格接受大额交易的预约 开启
    label_accept_large_trade_on = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[7]/div[1]/div/div/div/label[1]')
    # 是否以广告价格接受大额交易的预约 关闭
    label_accept_large_trade_off = ("xpath", '//*[@id="app"]/main/div/div/div/form/div[7]/div[1]/div/div/div/label[2]')
    # 预约交易额度
    input_large_trade_trade_limit = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[7]/div[2]/div[2]/div/div/div[1]/div[2]/input')
    # 付款时限
    input_large_trade_payment_time_limit = (
        "xpath", '//*[@id="app"]/main/div/div/div/form/div[7]/div[3]/div[2]/div/div/div/div[2]/input')
    # 显示高级选项
    i_advance_options = ("class name", 'ivu-icon-md-arrow-dropup')
    # 自动回复
    # textarea_auto_reply = ("xpath", '//*[@id="app"]/main/div/div/form/div[8]/div[2]/div/div/div/textarea')
    textarea_auto_reply = ("class name", 'ivu-input')
    # 交易限制 交易对手须成交过几次
    input_restrictions = ("class name", 'ivu-input-number-input')
    # 发布广告
    span_post_an_offer = ("xpath", '//*[@id="app"]/main/div/div/div/button/span/span')
    # 断言
    div_first_offer = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/div[1]/div/div[2]')
    # 删除第一条广告
    a_del_offer = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/div[1]/div/div[2]/span[9]/a[3]')
    # 删除提示框 确认按钮（可能有多个）
    button_confirm = ("class name", "ivu-btn-primary")

    # 错误提示文本框
    error_offer_title = ("class name", 'ivu-form-item-error-tip')


    def __init__(self, driver):
        super().__init__(driver)

    def click_button(self, locator):
        self.click(locator)

    def get_crypto(self):
        print(self.find_element(self.crypto_ul_loc))


if __name__ == "__main__":
    driver = browser()
    post_an_offer_driver = PostAnOfferPage(driver)
    post_an_offer_driver.open(post_an_offer_url)
    post_an_offer_driver.get_crypto()
    driver.quit()
