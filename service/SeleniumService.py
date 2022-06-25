import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumService:

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        if os.environ.get("GOOGLE_CHROME_PATH") != None: 
            options.binary_location = os.environ.get("GOOGLE_CHROME_PATH")
        if os.environ.get("CHROME_DRIVER_PATH") != None:
            self.driver = webdriver.Chrome(os.environ.get("CHROME_DRIVER_PATH"), chrome_options=options)
        else:
            self.driver = webdriver.Chrome("/app/.chromedriver/bin/chromedriver", chrome_options=options)

    def getDriver(self):
        return self.driver
