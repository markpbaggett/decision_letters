from seleniumrequests import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import os
import yaml


class DigitalCommonsConnection:
    def __init__(self, user, password):
        self.options = Options()
        self.driver = Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"), options=self.options)
        self.login(user, password)
        self.links = self.get_list_of_dissertations()

    def login(self, username, passwd):
        self.driver.get('https://trace.tennessee.edu/cgi/myaccount.cgi?context=')
        self.driver.find_element_by_id('auth_email').send_keys(username)
        self.driver.find_element_by_id('auth_password').send_keys(passwd)
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/div[1]/div/form/div/p/button'
        ).click()

    def get_list_of_dissertations(self):
        self.driver.get('https://trace.tennessee.edu/utk_graddiss/index.11.html#year_2015')
        disserations = self.driver.find_elements_by_css_selector('.article-listing > a')
        return [disserations[link].get_attribute('href') for link in range(0, len(x))]


if __name__ == "__main__":

    x = DigitalCommonsConnection("username", "password")
    print(x.links)
