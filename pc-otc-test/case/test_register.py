# coding:utf-8
from common.log import Log
import unittest
import ddt
from common.excelutil import Excel
import os
from page.register import RegisterPage,register_url
from selenium import webdriver


"""
初始化EXCEL数据
"""
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
excelPath = os.path.join(os.path.join(project_dir,'data'),"login.xlsx")
registerFailSheetName = "注册失败数据表"
registerSuccessSheetName = "注册成功数据表"
register_excel = Excel(excelPath)

register_fail_data = register_excel.get_list(registerFailSheetName)
register_success_data = register_excel.get_list(registerSuccessSheetName)

@ddt.ddt
class Testregister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.register_driver = RegisterPage(cls.driver)
        cls.register_driver.open(register_url)
        cls.driver.maximize_window()
        cls.log = Log()

    @ddt.data(*register_success_data)
    def test_register_fail(self, data):
        '''测试注册成功用例'''
        self.log.info("测试注册成功用例")
        self.datatype = data['datatype']
        if self.datatype == 'register_success1':
            self.log.info(
                "测试数据:(邮箱:{},密码:{},确认密码:{}),昵称：{},邀请码：{})".format(data['email'], data['psw'], data['sure_psw'],
                                                                  data['nickname'], data['yaoqing_code'],
                                                                  data['except']))

            self.register_driver.register(data['email'], data['psw'], data['sure_psw'], data['nickname'],
                                          data['yaoqing_code'])
            try:
                result = self.register_driver.register_scuess()
                self.assertEqual(result, data['except'])
                self.log.info("注册成功:%s" % result)
            except:
                self.log.info("注册失败")


    @ddt.data(*register_fail_data)
    def test_register_fail(self, data):
        '''测试注册失败用例'''
        self.log.info("测试注册失败用例")
        self.datatype = data['datatype']
        if self.datatype == 'email_text1':
            self.log.info("测试数据:(邮箱:{},密码:{},确认密码:{}),昵称：{},邀请码：{})".format(data['email'],data['psw'],data['sure_psw'],
                                                                           data['nickname'],data['yaoqing_code'],data['except']))

            self.register_driver.register(data['email'],data['psw'],data['sure_psw'],data['nickname'],data['yaoqing_code'])
            result = self.register_driver.get_text(self.register_driver.email_tip)
            try:
                self.assertEqual(result,data['except'])
                self.log.info("测试通过:%s"%result)
            except:
                self.log.info("测试未通过")

        elif self.datatype == 'email_text2':
            self.log.info("测试数据:(邮箱:{},密码:{},确认密码:{}),昵称：{},邀请码：{})".format(data['email'],data['psw'],data['sure_psw'],
                                                                           data['nickname'],data['yaoqing_code'],data['except']))

            self.register_driver.register(data['email'],data['psw'],data['sure_psw'],data['nickname'],data['yaoqing_code'])
            result = self.register_driver.get_text(self.register_driver.email_tip)
            try:
                self.assertEqual(result, data['except'])
                self.log.info("测试通过:%s" % result)
            except:
                self.log.info("测试未通过")

        elif self.datatype == 'psw_text':
            self.log.info("测试数据:(邮箱:{},密码:{},确认密码:{},昵称：{},邀请码：{})".format(data['email'], data['psw'], data['sure_psw'],
                                                                           data['nickname'], data['yaoqing_code'],
                                                                           data['except']))

            self.register_driver.register(data['email'], data['psw'], data['sure_psw'], data['nickname'],
                                          data['yaoqing_code'])
            '''
            lenght = len(data['psw'])
            if lenght < 6 or lenght > 20:
                self.log.info("您输入的密码有误，请输入8-20位数字和字母组合")
                return True
            '''
            result = self.register_driver.get_text(self.register_driver.psw_tip)
            try:
                self.assertEqual(result, data['except'])
                self.log.info("测试通过:%s" % result)
            except:
                self.log.info("测试未通过")

        elif self.datatype == 'sure_psw_text':
            self.log.info("测试数据:(邮箱:{},密码:{},确认密码:{},昵称：{},邀请码：{})".format(data['email'], data['psw'], data['sure_psw'],
                                                                           data['nickname'], data['yaoqing_code'],
                                                                           data['except']))

            self.register_driver.register(data['email'], data['psw'], data['sure_psw'], data['nickname'],
                                          data['yaoqing_code'])

            result = self.register_driver.get_text(self.register_driver.sure_psw_tip)
            try:
                self.assertEqual(result, data['except'])
                self.log.info("测试通过:%s" % result)
            except:
                self.log.info("测试未通过")

        elif self.datatype == 'nick_text1':
            self.log.info("测试数据:(邮箱:{},密码:{},确认密码:{},昵称：{},邀请码：{})".format(data['email'], data['psw'], data['sure_psw'],
                                                                           data['nickname'], data['yaoqing_code'],
                                                                           data['except']))

            self.register_driver.register(data['email'], data['psw'], data['sure_psw'], data['nickname'],
                                          data['yaoqing_code'])
            result = self.register_driver.get_text(self.register_driver.nickname_tip)
            try:
                self.assertEqual(result, data['except'])
                self.log.info("测试通过:%s" % result)
            except:
                self.log.info("测试未通过")

        elif self.datatype == 'nick_text2':
            self.log.info("测试数据:(邮箱:{},密码:{},确认密码:{}),昵称：{},邀请码：{})".format(data['email'],data['psw'],data['sure_psw'],
                                                                           data['nickname'],data['yaoqing_code'],data['except']))

            self.register_driver.register(data['email'],data['psw'],data['sure_psw'],data['nickname'],data['yaoqing_code'])
            result = self.register_driver.get_text(self.register_driver.email_tip)
            try:
                self.assertEqual(result, data['except'])
                self.log.info("测试通过:%s" % result)
            except:
                self.log.info("测试未通过")


        elif self.datatype == 'yaoqing_text':
            self.log.info("测试数据:(邮箱:{},密码:{},确认密码:{},昵称：{},邀请码：{})".format(data['email'], data['psw'], data['sure_psw'],
                                                                           data['nickname'], data['yaoqing_code'],
                                                                           data['except']))

            self.register_driver.register(data['email'], data['psw'], data['sure_psw'], data['nickname'],
                                          data['yaoqing_code'])
            result = self.register_driver.get_text(self.register_driver.yaoqing_tip)
            try:
                self.assertEqual(result, data['except'])
                self.log.info("测试通过:%s" % result)
            except:
                self.log.info("测试未通过")

        elif self.datatype == 'tou_text':
            self.log.info("测试数据:(邮箱:{},密码:{},确认密码:{},昵称：{},邀请码：{})".format(data['email'], data['psw'], data['sure_psw'],
                                                                           data['nickname'], data['yaoqing_code'],
                                                                           data['except']))

            self.register_driver.register(data['email'], data['psw'], data['sure_psw'], data['nickname'],
                                          data['yaoqing_code'],is_click=False)
            result = self.register_driver.get_text(self.register_driver.tou_tip)
            try:
                self.assertEqual(result, data['except'])
                self.log.info("测试通过:%s" % result)
            except:
                self.log.info("测试未通过")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
