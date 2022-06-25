import time, requests, logging, asyncio, aiohttp
from typing import List
from bs4 import BeautifulSoup
from PIL import Image
from config import Config
from io import BytesIO
from service.SeleniumService import SeleniumService


async def asyncScrape(urls, htmlTag, attr, condition):
    output = []

    async def process(output, url, htmlTag, attr, condition):
        driver = SeleniumService().getDriver()
        driver.get(url)
        rtr = {}
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for item in soup.find_all(htmlTag):
            a = item[attr]
            if condition in a:
                rtr[int(item.text.split("/")[0])] = a
        output.append(rtr)
        driver.close()

    tasks = [process(output, url, htmlTag, attr, condition) for url in urls]
    await asyncio.gather(*tasks)
    return output

logger = logging.getLogger("Scraper")

class Scraper:

    @classmethod
    async def scrape(
            self, driver, url: List[str],
            condition: str, htmlTag: str,
            attr: str) -> List[str]:
        startTime = time.time()
        final = await asyncScrape(url, htmlTag, attr, condition)
        rtr = []
        for j in final:
            for i in range(1, len(j) + 1):
                rtr.append(j[i])
        logger.info(f"Finish scraping {url}, took: {time.time() - startTime}s")
        return rtr

    @classmethod
    def scrapeTitles(self, driver, url, condition, htmlTag, attr, containerTag, className, blacklist=[], regex=None):
        r = requests.get(url)
        rtr = set()
        soup = BeautifulSoup(r.content, 'html.parser')
        containers = soup.find(containerTag, class_=className)
        for item in containers.find_all(htmlTag, href=True):
            a = item[attr]
            if condition in a and a not in blacklist:
                if regex is not None and regex.search(a):
                    rtr.add(a)
                elif regex is None:
                    rtr.add(a)
        return list(rtr)
