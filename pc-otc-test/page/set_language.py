from common.base import BasePage
from common.base import browser
import time
'''语言设置'''

URL = "http://wex.test.tigerft.com/home"
class set_languagePage(BasePage):
    drop_up = ("xpath", "//*[@id='app']/div/div/div[1]/div/div[3]/div[5]/div[1]/div/div") # 一级菜单
    drop_down = ("class name", "ivu-dropdown-item") # 二级菜单


    def language(self):
        flag = self.find_elements(self.drop_down)
        return flag


    # 选择语言
    def select_luanguage(self, language):
        if language in "简体中文":
            self.click_mouse(self.drop_up)
            time.sleep(2)
            self.language()[0].click()
            language = self.get_text(self.drop_up)
            print("当前语言为：%s" % language)
            try:
                assert u"简体中文" in language
                print("Setting Success")
            except Exception as e:
                print('Setting Fail.', format(e))
        elif language in "繁體中文":
            self.click_mouse(self.drop_up)
            time.sleep(2)
            self.language()[1].click()
            language = self.get_text(self.drop_up)
            print("当前语言为：%s" % language)
            try:
                assert u"繁體中文" in language
                print("Setting Success")
            except Exception as e:
                print('Setting Fail.', format(e))
        elif language in "English":
            self.click_mouse(self.drop_up)
            time.sleep(2)
            self.language()[2].click()
            language = self.get_text(self.drop_up)
            print("当前语言为：%s" % language)
            try:
                assert "English" in language
                print("Setting Success")
            except Exception as e:
                print('Setting Fail.', format(e))
        else:
            print("没有该语种")

if __name__ == "__main__":
    driver = browser()
    language_driver = set_languagePage(driver)
    language_driver.open(URL)
    driver.maximize_window()
    language_driver.select_luanguage("简体中文")
    driver.quit()

