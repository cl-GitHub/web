# coding:utf-8
my_offers_url = "http://wex.test.tigerft.com/transaction/ad"
from common.base import BasePage
from selenium import webdriver
from common.base import browser
import time


class MyOffersPage(BasePage):
    """广告管理页面"""
    # 广告
    div_my_offer = ("class name", "item")
    # 编辑第一条广告按钮
    a_edit_offer = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/div[1]/div/div[2]/span[9]/a[1]')
    # 分享第一条广告按钮
    a_share_offer = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/div[1]/div/div[2]/span[9]/a[2]')
    # 删除第一条广告按钮
    a_delete_offer = ("xpath", '//*[@id="app"]/main/div/div/div/div[2]/div[1]/div/div[2]/span[9]/a[3]')
    # 删除提示框确认按钮（可能有多个）
    alert_confirm_button = ("class name", "ivu-btn-primary")
    # 删除提示框取消按钮（可能有多个）
    alert_cancel_button = ("class name", "ivu-btn-text")
    # 页码
    li_page_item = ("class name", "ivu-page-item")
    ul_page = ("xpath", '//*[@id="app"]/main/div/div/div/div[3]/ul')
    # 上一页
    li_page_prev = ("class name", 'ivu-page-prev')
    # 下一页
    li_page_next = ("class name", 'ivu-page-next')
    # 不可点击标签
    li_page_disabled = ("class name", 'ivu-page-disabled')
    # 页码被选中标签
    li_page_item_active = ("class name", 'ivu-page-item-active')
    # vue提示组件-成功
    vue_alert_success = ("class name", "ivu-message-success")
    # 广告上下架状态switch选择框
    span_switch = ("class name", "ivu-switch-inner")
    # 该页面所有下拉列表框按钮
    div_dropdown_rel = ("class name", "ivu-dropdown-rel")
    # 该页面所有下拉列表框中元素
    li_dropdown_item = ("class name", "ivu-dropdown-item")

    def __init__(self, driver):
        super().__init__(driver)


if __name__ == "__main__":
    driver = browser()
    post_an_offer_driver = MyOffersPage(driver)
    post_an_offer_driver.open(my_offers_url)
    post_an_offer_driver.get_crypto()
    driver.quit()
