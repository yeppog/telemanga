import re
from scrapers.Scraper import Scraper
from typing import List


pageConfigs = {
    "filter": "https",
    "htmlTag": "option",
    "htmlAttr": "value"
}

searchConfigs = {
    "filter": "http://mangafox.win",
    "htmlTag": "a",
    "htmlAttr": "href",
    "regex":"^(?!.*chapter).*http:\/\/[a-z1-9\/\?\.\&\-=]*"
}

blackListUrl = [
        "http://mangafox.win",
        "http://mangafox.win",
        "http://mangafox.win/bookmark-manga",
        "http://mangafox.win/history-manga",
        "http://mangafox.win/latest-manga",
        "http://mangafox.win/completed-manga",
        "http://mangafox.win/popular-manga",
        "http://mangafox.win/mangas/action",
        "http://mangafox.win/mangas/adult",
        "http://mangafox.win/mangas/adventure",
        "http://mangafox.win/mangas/comedy",
        "http://mangafox.win/mangas/cooking",
        "http://mangafox.win/mangas/doujinshi",
        "http://mangafox.win/mangas/drama",
        "http://mangafox.win/mangas/ecchi",
        "http://mangafox.win/mangas/fantasy",
        "http://mangafox.win/mangas/gender-bender",
        "http://mangafox.win/mangas/harem",
        "http://mangafox.win/mangas/historical",
        "http://mangafox.win/mangas/horror",
        "http://mangafox.win/mangas/isekai",
        "http://mangafox.win/mangas/josei",
        "http://mangafox.win/mangas/manhua",
        "http://mangafox.win/mangas/manhwa",
        "http://mangafox.win/mangas/martial-arts",
        "http://mangafox.win/mangas/mature",
        "http://mangafox.win/mangas/mecha",
        "http://mangafox.win/mangas/medical",
        "http://mangafox.win/mangas/mystery",
        "http://mangafox.win/mangas/one-shot",
        "http://mangafox.win/mangas/psychological",
        "http://mangafox.win/mangas/romance",
        "http://mangafox.win/mangas/school-life",
        "http://mangafox.win/mangas/sci-fi",
        "http://mangafox.win/mangas/seinen",
        "http://mangafox.win/mangas/shoujo",
        "http://mangafox.win/mangas/shoujo-ai",
        "http://mangafox.win/mangas/shounen",
        "http://mangafox.win/mangas/shounen-ai",
        "http://mangafox.win/mangas/slice-of-life",
        "http://mangafox.win/mangas/smut",
        "http://mangafox.win/mangas/sports",
        "http://mangafox.win/mangas/supernatural",
        "http://mangafox.win/mangas/tragedy",
        "http://mangafox.win/mangas/webtoons",
        "http://mangafox.win/mangas/yaoi",
        "http://mangafox.win/mangas/yuri",
        "http://mangafox.win/popular-manga"
]


class MangaFoxScraper(Scraper):

    @classmethod
    def getMangaPages(self, driver, url: str, fullPath=None) -> List[str]:
        fUrl = url
        if fullPath is not None:
            fUrl = fullPath
        return super().scrape(
            driver,
            fUrl,
            pageConfigs["filter"],
            pageConfigs["htmlTag"],
            pageConfigs["htmlAttr"],
        )

    @classmethod
    # should refactor filter to regex.
    def getMangaTitles(self, driver, url, query: str) -> List[str]:
        newUrl = url + "/search?q=" + query
        print(newUrl)
        return super().simpleScrape(
            newUrl,
            searchConfigs["filter"],
            searchConfigs["htmlTag"],
            searchConfigs["htmlAttr"],
            blackListUrl,
            re.compile(searchConfigs["regex"] + f"(?:{query})*")
            )
