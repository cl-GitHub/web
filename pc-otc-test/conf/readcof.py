# coding:utf-8

import configparser
import os

# 获取当前文件真实路径
cur_path = os.path.dirname(os.path.realpath(__file__))
print(cur_path)

"""邮件配置"""
email_cfg_path = os.path.join(cur_path, "email_cof.ini")
email_conf = configparser.ConfigParser()
email_conf.read(email_cfg_path, encoding="utf-8")
email_smtp_server = email_conf.get("email", "smtp_server")
email_sender = email_conf.get("email", "sender")
email_psw = email_conf.get("email", "psw")
email_port = int(email_conf.get("email", "port"))
email_receiver = email_conf.get("email", "receiver")

"""获取数据库连接池配置"""


class MysqlConfig(object):
    """
    # MysqlConfig().get_content("mysql")
    配置文件里面的参数
    [dbMysql]
    host = 192.168.9.168
    port = 3306
    user = reader
    password = reader
    """

    def __init__(self, config_filename="mysql_cof.ini"):
        file_path = os.path.join(os.path.dirname(__file__), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        mysql_result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            mysql_result[option] = int(value) if value.isdigit() else value
        return mysql_result
