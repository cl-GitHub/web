# coding:utf-8
my_order_url = "http://wex.test.tigerft.com/transaction/"
from common.base import BasePage
from common.base import browser
from common.logeventlistener import LogEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver


class MyOrdersPage(BasePage):
    """订单管理页面"""
    # 订单列表
    div_orders = ("class name", 'item')
    # 页码
    li_page_item = ("class name", "ivu-page-item")
    # 上一页
    li_page_prev = ("class name", 'ivu-page-prev')
    # 下一页
    li_page_next = ("class name", 'ivu-page-next')
    # 不可点击标签
    li_page_disabled = ("class name", 'ivu-page-disabled')
    # 页码被选中标签
    li_page_item_active = ("class name", 'ivu-page-item-active')
    # 搜索按钮
    button_search = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[7]/div/button[1]')
    # 重置按钮
    button_reset = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[7]/div/button[2]')
    # 订单输入框
    input_order_no = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[6]/div[2]/div/div/div/input')
    # 开始日期输入框
    input_start_date = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[5]/div[2]/div[1]/div[1]/div/input')
    # 结束日期输入框
    input_end_date = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[5]/div[2]/div[2]/div[1]/div/input')
    # 筛选条件
    span_all_type = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[1]/div[2]/span[1]')
    span_buy = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[1]/div[2]/span[2]')
    span_sell = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[1]/div[2]/span[3]')
    span_all_status = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div[2]/span[1]')
    span_progressing = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div[2]/span[2]')
    span_completed = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div[2]/span[3]')
    span_canceled = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[2]/div[2]/span[4]')
    span_all_crypto = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[3]/div[2]/span[1]')
    span__usdt = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[3]/div[2]/span[2]')
    span__usdc = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[3]/div[2]/span[3]')
    span__tusd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[3]/div[2]/span[4]')
    span_all_fiat = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[4]/div[2]/span[1]')
    span__hkd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[4]/div[2]/span[2]')
    span__twd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[4]/div[2]/span[3]')
    span__usd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[4]/div[2]/span[4]')
    span__idr = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[4]/div[2]/span[5]')
    span__vnd = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[4]/div[2]/span[6]')
    span__khr = ("xpath", '//*[@id="app"]/main/div/div/div/div[1]/form/div[4]/div[2]/span[7]')
    # 暂无数据
    div_no_records = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/div[2]/div')
    # 错误提示文本框
    error_orders_title = ("class name", 'ivu-message-error')
    # 查看按钮
    span_detail = ("class name", 'view-detail')
    # 广告主标签
    a_advert = ("class name", 'view-detail-gary')
    # 查看我的预约
    span_check_my_reservation = ("class name", 'ivu-btn-default')

    def __init__(self, driver):
        super().__init__(EventFiringWebDriver(driver, LogEventListener()))

    def get_float(self, f_str, n):
        """计算精度
        :param f_str:截取精度的数字
        :param n:精度长度
        """
        f_str = str(f_str)  # f_str = '{}'.format(f_str) 也可以转换为字符串
        a, b, c = f_str.partition('.')
        c = (c + "0" * n)[:n]  # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
        return ".".join([a, c])

    def get_amount(self, amount):
        """去除数量中的千分位"""
        return amount.replace(",", "")

    def check_data(self, my_orders_web_info, my_orders_sql_info):
        """数据校验
        :param my_orders_web_info:页面数据
        :type my_orders_web_info:list
        :param my_orders_sql_info:数据库数据
        :type my_orders_sql_info:dict
        """
        if my_orders_sql_info['SIDE'] == '1':
            # 判断订单方向
            assert "买" or "BuyOrder No" in my_orders_web_info[0]
            # 判断交易数字币数量
            assert MyOrdersPage.get_float(self, my_orders_sql_info['STANDARD_REAL_VOLUME'], 4) == \
                   my_orders_web_info[3]
        elif my_orders_sql_info['SIDE'] == '2':
            assert "卖" or "SellOrder No" in my_orders_web_info[0]
            assert MyOrdersPage.get_float(self, my_orders_sql_info['STANDARD_VOLUME'], 4) == \
                   my_orders_web_info[3]
        # 判断订单号
        assert str(my_orders_sql_info['ID']) in my_orders_web_info[0]
        # 判断订单创建日期
        assert str(my_orders_sql_info['CREATE_TIME']) in my_orders_web_info[0]
        # 判断交易法币数量
        # 获取页面法币数量
        web_currency_amount = MyOrdersPage.get_amount(self, my_orders_web_info[2].split(' ')[0])
        # 获取数据库法币数量
        sql_currency_amount = MyOrdersPage.get_float(self, my_orders_sql_info['TARGET_VOLUME'], 2)
        # 获取页面的法币单位
        web_currency_type = MyOrdersPage.get_amount(self, my_orders_web_info[2].split(' ')[1])
        # 获取数据库法币单位
        sql_currency_type = my_orders_sql_info['TARGET_COIN']
        assert web_currency_amount == sql_currency_amount
        assert web_currency_type == sql_currency_type
        # 判断交易价格
        if my_orders_sql_info['TARGET_COIN'] == 'HKD':
            assert "{} {}/{}".format(
                MyOrdersPage.get_float(self, my_orders_sql_info['EXCHANGE_RATE'], 3),
                my_orders_sql_info['TARGET_COIN'],
                my_orders_sql_info['STANDARD_COIN']) == my_orders_web_info[3]
        elif my_orders_sql_info['TARGET_COIN'] == 'USD':
            assert "{} {}/{}".format(
                MyOrdersPage.get_float(self, my_orders_sql_info['EXCHANGE_RATE'], 4),
                my_orders_sql_info['TARGET_COIN'],
                my_orders_sql_info['STANDARD_COIN']) == my_orders_web_info[3]
        else:
            assert "{} {}/{}".format(
                MyOrdersPage.get_float(self, my_orders_sql_info['EXCHANGE_RATE'], 2),
                my_orders_sql_info['TARGET_COIN'],
                my_orders_sql_info['STANDARD_COIN']) == my_orders_web_info[3]
        # 判断订单状态
        if my_orders_sql_info['STATE'] in (10, 20, 30):
            assert my_orders_web_info[5] in ('Progressing', '交易中')
        elif my_orders_sql_info['STATE'] in (40, 50):
            assert my_orders_web_info[5] in ('Completed', '已完成')
        elif my_orders_sql_info['STATE'] == 90:
            assert my_orders_web_info[5] in ('Canceled', '已取消')


if __name__ == "__main__":
    driver = browser()
    my_orders_driver = MyOrdersPage(driver)
    my_orders_driver.open(MyOrdersPage)
    my_orders_driver.get_crypto()
    driver.quit()
