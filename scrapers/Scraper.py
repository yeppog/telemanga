import time
import requests
from typing import List
from bs4 import BeautifulSoup


class Scraper:

    @classmethod
    def scrape(
            self, driver, url: str,
            condition: str, htmlTag: str,
            attr: str) -> List[str]:
        try:
            driver.get(url)
            time.sleep(2)
            rtr = []
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for item in soup.find_all(htmlTag):
                print(item)
                a = item[attr]
                if condition in a:
                    rtr.append(a)
            return rtr
        except Exception as e:
            print(e)
            return []

    @classmethod
    def simpleScrape(self, url, condition, htmlTag, attr, blacklist=[], regex = None):
        r = requests.get(url)
        rtr = set()
        soup = BeautifulSoup(r.content, 'html.parser')
        for item in soup.find_all(htmlTag, href=True):
            a = item[attr]
            if condition in a and a not in blacklist:
                if regex is not None and regex.search(a):
                    rtr.add(a)
                elif regex is None:
                    rtr.add(a)
        return rtr
