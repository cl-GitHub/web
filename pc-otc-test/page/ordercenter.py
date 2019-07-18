# coding:utf-8
my_offers_url = "http://wex.test.tigerft.com/business_order"
from common.base import BasePage


class OrderCenterPage(BasePage):
    """订单中心页面"""
    # 刷新按钮

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
    # 刷新按钮
    i_order_refresh = ("class name", 'ivu-icon-md-sync')
    # 查看全部订单
    span_view_all_orders = ("xpath", '//*[@id="app"]/main/div/div/div[4]/div[1]/span')
    # 进行中订单列表
    ul_ongoing_order = ("xpath", '//*[@id="app"]/main/div/div/div[2]/div[2]/div[2]/ul/li')
    # 进行中订单详情按钮列表
    span_ongoing_order_detail = 'ongoing-list-item'
    # 近期订单详情按钮列表
    span_recent_order_detail = 'recent-list-item'
    # 大额交易订单列表
    ul_trade_order = ("xpath", '//*[@id="app"]/main/div/div/div[3]/div[2]/div[2]/ul[1]/li')
    # 最近订单列表
    ul_recent_order = ("xpath", '//*[@id="app"]/main/div/div/div[4]/div[2]/div[2]/ul/li')
