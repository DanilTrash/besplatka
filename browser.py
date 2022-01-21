from itertools import cycle
from random import choice
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class Browser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        breakpoint()
        self.driver.quit()

    def __call__(self, *args, **kwargs):
        self.driver.get('https://besplatka.ua/')
        while True:
            self.driver.execute_script("window.open('https://besplatka.ua/message/payment?reserve=2045708&id=2045707&category_packet=166&for_app=')")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            WebDriverWait(self.driver, 5).until(
                lambda d: self.driver.find_element_by_xpath('//*[@id="body-wrap-container"]/div[3]/div[2]/div/div[2]/div[4]/div[3]/label/div[1]')
            ).click()


if __name__ == '__main__':
    with Browser() as browser:
        browser()
