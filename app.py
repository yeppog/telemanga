import sys
from typing import List
from scrapers.MangaFoxScraper import MangaFoxScraper
from scrapers import Scraper
from service.SeleniumService import SeleniumService
from tele.Telegram import Telegram
from dotenv import load_dotenv
import os

import logging


class App:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(threadName)-12.12s] [%(name)-s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout)
                ]
            )
        load_dotenv()
        self.sel = SeleniumService()
        self.logger = logging.getLogger()
        self.scraper = Scraper.Scraper()
        self.telegram = Telegram(os.environ['KEY'], self.sel)

    """
    Currently only works with MangaFox
    """

    def getManga(self, url: str) -> List[str]:
        results = MangaFoxScraper.getMangaPages(self.sel.getDriver(), url)
        for i in results:
            print(i)
        return results

    def searchManga(self, url: str, query: str) -> List[str]:
        results = MangaFoxScraper.getMangaTitles(self.sel.getDriver(), url, query)
        for i in results:
            print(i)
        return results

    def run(self) -> None:
        # define telebot run instance here i guess?
        self.logger.info("Starting app...")
        self.telegram.run()
        return None
