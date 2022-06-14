
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



class SeleniumService:

    def __init__(self): 
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)

    def getDriver(self):
        return self.driver
