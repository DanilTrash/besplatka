from itertools import cycle
from random import choice
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from logger import log

LOGGER = log('besplatka')


class Besplatka:
    def __init__(self, **kwargs):
        options = webdriver.ChromeOptions()
        if kwargs['headless']:
            options.add_argument('--headless')
        if kwargs.get('proxy', False):
            options.add_argument('--proxy-server=%s' % kwargs.get('proxy', ))
        self.driver = webdriver.Chrome(options=options)

    def auth(self, login, password):
        LOGGER.info('%s:%s' % (login, password))
        url = 'https://besplatka.ua/login'
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: self.driver.find_element_by_name('email')).send_keys(login)
            self.driver.find_element_by_name('password').send_keys(password)
            self.driver.find_element_by_class_name("accept-button").click()
            WebDriverWait(self.driver, 10).until_not(lambda d: self.driver.find_element_by_class_name("accept-button"))
            return True
        except Exception as error:
            LOGGER.exception(error)
            return False

    def post_ad(self, title, description, phone):
        url = 'https://besplatka.ua/message/create'
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: self.driver.find_element_by_name('MessageCreateForm[title]')).send_keys(title)
            for letter in description:
                self.driver.find_element_by_xpath('//*/textarea[@id="messagecreateform-text"]').send_keys(letter)
            phone_input_field = self.driver.find_element_by_name('MessageCreateForm[phone]')
            _ = phone_input_field.location_once_scrolled_into_view
            self.driver.find_element_by_xpath('//*[@id="category-modal-wrap-vue"]/div[2]/div/a').click()
            WebDriverWait(self.driver, 5).until(
                lambda d: self.driver.find_element_by_xpath(
                    '//*[@id="new_vue_category_modal"]/div/div/div[2]/div/ul/li[5]/a/span/p')).click()
            WebDriverWait(self.driver, 5).until(
                lambda d: self.driver.find_element_by_xpath(
                    '//*/div/div/div[2]/div/div[2]/div/div/div/ul/li[2]/a/span'
                )).click()
            sleep(1.5)
            self.driver.find_element_by_name('MessageCreateForm[price]').send_keys(f'1{str(choice(range(7, 9)))}000')
            self.driver.find_element_by_xpath('//*[@id="properties"]/div[1]/div[2]/div/a').click()
            self.driver.find_element_by_xpath('//*[@data-value="577288"]').click()
            self.driver.find_element_by_xpath('//*/div[2]/div/div[1]/div[1]/label/span[1]/i[2]').click()
            self.driver.find_element_by_xpath('//*[@id="properties"]/div[3]/div[2]/div/a').click()
            self.driver.find_element_by_xpath('//*[@id="properties"]/div[3]/div[2]/div/ul/li[3]/a').click()
            self.driver.find_element_by_xpath('//*[@id="properties"]/div[4]/div[2]/div/a').click()
            self.driver.find_element_by_xpath('//*[@id="properties"]/div[4]/div[2]/div/ul/li[3]/a').click()
            self.driver.find_element_by_xpath('//*/div[5]/div[2]/div/div[1]/label/span[1]/i[2]').click()
            self.driver.find_element_by_xpath('//*/div[5]/div[2]/div/div[2]/label/span[1]/i[2]').click()
            region_element = self.driver.find_element_by_xpath('//*[@id="region-modal-wrap-vue"]/div[2]/div/a')
            _ = region_element.location_once_scrolled_into_view
            region_element.click()
            sleep(1.5)
            self.driver.find_element_by_xpath('//*[@id="region_modal"]/div/div/div[1]/div[3]/div/input').send_keys('ки')
            sleep(1.5)
            self.driver.find_element_by_xpath('//*[@id="searchRegion"]/li[2]/a').click()
            self.driver.find_element_by_xpath('//*[@id="submit-form-btn"]').click()
            WebDriverWait(self.driver, 15).until_not(
                lambda d: self.driver.find_element_by_xpath('//*[@id="submit-form-btn"]'))
            self.driver.execute_script('window.scrollBy(0,1000)')
            self.driver.find_element_by_xpath('//*[@id="service-reset"]').click()
            return True
        except Exception as error:
            LOGGER.exception(error)
            return False


def main():
    df = pd.read_csv('https://docs.google.com/spreadsheets/'
                     'd/1zaxjdu9ESYy2MCNuDow0_5PnZpwEsyrdTQ_kk0PMZbw/expo'
                     'rt?format=csv&id=1zaxjdu9ESYy2MCNuDow0_5PnZpwEsyrdTQ_kk0PMZbw&gid=354035052',
                     dtype={'phone': str})
    titles = cycle(df['title'].dropna().tolist())
    descriptions = cycle(df['description'].dropna().tolist())
    phones = cycle(df['phone'].dropna().tolist())
    logins = df['login'].dropna().tolist()
    passwords = df['password'].dropna().tolist()
    besplatka = Besplatka(headless=False)
    if besplatka.auth(logins[0], passwords[0]):
        while True:
            besplatka.post_ad(next(titles), next(descriptions), next(phones))


if __name__ == '__main__':
    try:
        LOGGER.info(__name__)
        main()
    except Exception as error:
        LOGGER.exception(error)
