import time
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
            time.sleep(1)
            rtr = []
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for item in soup.find_all(htmlTag):
                a = item[attr]
                if condition in a:
                    rtr.append(a)
            return rtr
        except Exception as e:
            print(e)
            return []
