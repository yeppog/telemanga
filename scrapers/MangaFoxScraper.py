from scrapers.Scraper import Scraper
from typing import List


pageConfigs = {
        "filter": "https",
        "htmlTag": "option",
        "htmlAttr": "value"
        }


class MangaFoxScraper(Scraper):

    @classmethod
    def getMangaPages(self, driver, url: str) -> List[str]:
        return super().scrape(
                driver,
                url,
                pageConfigs["filter"],
                pageConfigs["htmlTag"],
                pageConfigs["htmlAttr"],
                )
