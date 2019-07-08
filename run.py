from seleniumrequests import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os
import yaml


class DigitalCommonsConnection:
    def __init__(self, user, password):
        self.options = Options()
        self.driver = Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"), options=self.options)
        self.login(user, password)
        self.dissertations = self.get_list_of_dissertations()
        self.lookup_values = self.__review_dissertations()
        self.__lookup_decisions()

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
        return [disserations[link].get_attribute('href') for link in range(0, len(disserations))]

    def __review_dissertations(self):
        lookups = []
        for dissertation in self.dissertations:
            self.driver.get(dissertation)
            link = self.driver.find_element_by_css_selector('#title > p > a')
            lookups.append(link.get_attribute('href').split('=')[1].split('&')[0])
        return lookups

    def __lookup_decisions(self):
        for dissertation in self.lookup_values:
            self.driver.get(f'https://trace.tennessee.edu/cgi/editor.cgi?article={dissertation}'
                            f'&amp;window=viewdecisions&amp;context=utk_graddiss')
            decisions = self.driver.find_elements_by_css_selector('.MenuMain > tbody > tr > td > table > tbody > tr > td > a')
            all_decisions = [decisions[link].get_attribute('href') for link in range(0, len(decisions)) if link != 'https://trace.tennessee.edu/cgi/help.cgi?context=utk_graddiss&help=help-submissions.html#']
            for decision in all_decisions:
                self.driver.get(decision)
                try:
                    final_decision_metadata = self.driver.find_element_by_css_selector('.MenuMain > tbody > tr > td > span')
                    decision_metadata = final_decision_metadata.text
                    print(decision_metadata.split('\n'))
                    final_decision = self.driver.find_element_by_css_selector('.MenuMain > tbody > tr > td > pre')
                except NoSuchElementException:
                    pass
        return


if __name__ == "__main__":
    settings = yaml.safe_load(open("config.yml", "r"))
    x = DigitalCommonsConnection(settings['username'], settings["password"])
    print(x.links)
