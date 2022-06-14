import sys
from typing import List
from scrapers.MangaFoxScraper import MangaFoxScraper
from scrapers import Scraper
from service.SeleniumService import SeleniumService
import logging


class App:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout)
                ]
            )
        self.sel = SeleniumService()
        self.logger = logging.getLogger()
        self.scraper = Scraper.Scraper()

    """
    Currently only works with MangaFox
    """

    def getManga(self, url: str) -> List[str]:
        results = MangaFoxScraper.getMangaPages(self.sel.getDriver(), url)
        for i in results:
            print(i)
        return results

    def run(self) -> None:
        # define telebot run instance here i guess?
        self.logger.info("Starting app...")
        return None
