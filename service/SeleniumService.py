import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumService:

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        if "GOOGLE_CHROME_PATH" in os.environ: 
            options.binary_location = os.environ["GOOGLE_CHROME_PATH"]
        if "CHROME_DRIVER_PATH" in os.environ:
            self.driver = webdriver.Chrome(os.environ["CHROME_DRIVER_PATH"], chrome_options=options)
        else:
            self.driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)

    def getDriver(self):
        return self.driver
