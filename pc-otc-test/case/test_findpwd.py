# coding:utf-8
from common.opmysql import MysqlPool
from page.forgetpsw import FindPage, find_url
from common.log import Log
import unittest
import time
import ddt
from common.excelutil import Excel
import os
from common.base import set_options

"""
初始化EXCEL数据
"""
project_dir = os.path.dirname(os.path.abspath('.'))
excelPath = project_dir + '/pc-otc-test/data/login.xlsx'
"""如果测试单个test"""
# excelPath = project_dir + '/data/login.xlsx'
findPwdSuccessSheetName = "找回密码成功数据表"
findPwdFailSheetName = "找回密码失败数据表"
find_pwd_excel = Excel(excelPath)
find_pwd_success_data = find_pwd_excel.get_list(findPwdSuccessSheetName)
find_pwd_fail_data = find_pwd_excel.get_list(findPwdFailSheetName)


@ddt.ddt
class TestFindPwd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = set_options()
        cls.driver.set_window_size(1920, 1080)
        cls.find_pwd_driver = FindPage(cls.driver)
        cls.find_pwd_driver.open(find_url)
        cls.log = Log()

    @ddt.data(*find_pwd_success_data)
    def test_find_pwd_success(self, data):
        """正确的邮箱地址"""
        self.log.info("---开始测试正确的邮箱地址找回密码---")
        self.find_pwd_driver.input_email_address(data['emailaddress'])
        self.find_pwd_driver.click_button_get_verfication_code()
        try:
            mysql = MysqlPool("mysql")
            get_auth_code_sql = "select AUTH_CODE from smsgateway.t_auth_code where biz_id = %s order by ID DESC;"
            result = mysql.getOne(get_auth_code_sql, (data['emailaddress'],))
        except Exception as e:
            self.log.info(e)
        finally:
            # 释放资源
            mysql.dispose()
        time.sleep(5)
        self.find_pwd_driver.input_verification(result['AUTH_CODE'])
        self.find_pwd_driver.click_button_button_resetting()
        result = self.find_pwd_driver.is_text_in_element(
            self.find_pwd_driver.find_resetting, data['except']
        )
        self.assertTrue(result)
        time.sleep(5)
        if result:
            self.log.info(u"打印:测试成功")
        else:
            self.log.info(u"打印:测试失败")

    @ddt.data(*find_pwd_fail_data)
    def test_find_pwd_fail(self, data):
        """输入错误的邮箱地址和验证码测试用例"""
        self.log.info("---开始测试错误的邮箱地址和验证码---")
        self.datatype = data['datatype']
        if self.datatype == 'alert':
            self.log.info("测试数据(用户名:{},密码:{},断言:{})".format(data['emailaddress'], data['verification'], data['except']))
            self.find_pwd_driver.find_password(self.find_pwd_driver, data['emailaddress'], data['verification'])
            result = self.find_pwd_driver.get_text(self.find_pwd_driver.vue_alert)
            print(result)
            try:
                assert data['except'] in result
            except Exception as e:
                print('Test Fail.', format(e))
            time.sleep(5)
        elif self.datatype == 'email_text':
            self.log.info("测试数据(用户名:{},密码:{},断言:{})".format(data['emailaddress'], data['verification'], data['except']))
            self.find_pwd_driver.find_password(self.find_pwd_driver, data['emailaddress'], data['verification'])
            result = self.find_pwd_driver.is_text_in_element(
                self.find_pwd_driver.error_email_address_tips, data['except']
            )
            self.assertTrue(result)
            time.sleep(5)
            if result:
                self.log.info(u"打印:测试成功")
            else:
                self.log.info(u"打印:测试失败")
        elif self.datatype == 'verification_text':
            self.log.info("测试数据(用户名:{},密码:{},断言:{})".format(data['emailaddress'], data['verification'], data['except']))
            self.find_pwd_driver.find_password(self.find_pwd_driver, data['emailaddress'], data['verification'])
            result = self.find_pwd_driver.is_text_in_element(
                self.find_pwd_driver.error_verification_tips, data['except']
            )
            self.assertTrue(result)
            time.sleep(5)
            if result:
                self.log.info(u"打印:测试成功")
            else:
                self.log.info(u"打印:测试失败")

    @ddt.data(*find_pwd_success_data)
    def test_frequent_requests(self, data):
        """正确的邮箱地址"""
        self.log.info("---开始测试正确的邮箱地址找回密码---")
        self.find_pwd_driver.input_email_address(data['emailaddress'])
        self.find_pwd_driver.click_button_get_verfication_code()
        self.driver.refresh()
        self.find_pwd_driver.input_email_address(data['emailaddress'])
        self.find_pwd_driver.click_button_get_verfication_code()
        result = self.find_pwd_driver.get_text(self.find_pwd_driver.vue_alert)
        print(result)
        try:
            assert "发送验证码过于频繁，请稍后再试" in result
        except Exception as e:
            print('Test Fail.', format(e))
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
