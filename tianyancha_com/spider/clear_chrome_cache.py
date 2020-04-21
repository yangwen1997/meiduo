# _*_coding:utf-8_*_
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait

class Clear:
    def __init__(self):
        self.count = 0

    def get_clear_cookie_button(self,driver):
        return driver.find_element_by_css_selector('* /deep/ #cookiesCheckboxBasic')

    def get_clear_browsing_button(self,driver):
        return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


    def clear_cache(self, driver,timeout=60):
        driver.get('chrome://settings/clearBrowserData')

        wait = WebDriverWait(driver, timeout)
        wait.until(self.get_clear_browsing_button)

        if self.count ==0:
            # 清理cookie
            cookie_html = self.get_clear_cookie_button(driver)
            cookie_html.find_element_by_css_selector('* /deep/ #checkboxContainer').click()
            self.count+=1

        self.get_clear_browsing_button(driver).click()

        # 点击按钮
        wait.until_not(self.get_clear_browsing_button)



