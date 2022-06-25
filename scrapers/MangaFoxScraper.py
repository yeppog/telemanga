import re
import logging
from scrapers.Scraper import Scraper
from typing import List, Tuple


pageConfigs = {
    "filter": "https",
    "htmlTag": "option",
    "htmlAttr": "value"
}

searchConfigs = {
    "filter": "http://mangafox.win",
    "htmlTag": "a",
    "htmlAttr": "href",
    "className": "truyen-list",
    "container": "div",
    "regex": "^(?!.*chapter).*^(?!.*search\?q).*http:\/\/[a-z1-9\/\?\.\&\-=]*"
}

domain = "http://mangafox.win/"

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

logger = logging.getLogger("MangaFoxScraper")
scraper = "MangaFoxScraper"

class MangaFoxScraper(Scraper):

    @classmethod
    async def getMangaPages(self, driver, url: str, chapter: int, count: int, fullPath=None) -> List[str]:
        logger.info(f"Scraping pages in {scraper}, at {url}, chapter: {chapter}, count: {count}")
        urls = [url + f"-chapter-{i+chapter}" for i in range(count)]
        return await super().scrape(
            driver,
            urls,
            pageConfigs["filter"],
            pageConfigs["htmlTag"],
            pageConfigs["htmlAttr"],
        )

    @classmethod
    # should refactor filter to regex.
    def getMangaTitles(self, driver, query: str) -> List[str]:
        logger.info(f"Scraping titles in {scraper} with query: {query}")
        newUrl = domain + "search?q=" + query
        results = super().scrapeTitles(
            driver,
            newUrl,
            searchConfigs["filter"],
            searchConfigs["htmlTag"],
            searchConfigs["htmlAttr"],
            searchConfigs["container"],
            searchConfigs["className"],
            blackListUrl,
            re.compile(searchConfigs["regex"] + f"(?:{query})*")
        )
        for i, v in enumerate(results):
            newUrl = domain + (v[len(domain):]).replace("manga/", "")
            results[i] = (newUrl, self.parseReadableNames(newUrl).title())
        return results

    @classmethod
    def parsePDFName(self, title, base, count):
        title = title.replace(" ", "_")
        if count > 1:
            return f"{title}_chapter_{base}-{base+count-1}"
        return f"{title}_chapter_{base}"

    @classmethod
    def parseReadableNames(self, url):
        postfix = url[len(domain):]
        postfix = postfix.replace("-", " ")
        hashIndex = postfix.find("#")
        if hashIndex > 0:
            postfix = postfix[:hashIndex]
        return postfix
