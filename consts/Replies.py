

class Replies:
    start = "Hello there, would you like to"
    chooseSource = "Choose your source you'd like to get your manga from."
    searchManga = "\n\nEnter some keywords to search this source."
    showTitles = "Here are some of the titles I have found. Enter a number that corresponds to it"
    titleUpdate = "\nYou have selected: "
    getChapters = "\nEnter the base chapter that you'd want"
    queryUpdate = "\nYou have searched for: "
    end = "Enjoy your manga: "

    def getCountString(self,x): 
        return f"\nYou have chosen to start from chapter {x}.\nEnter how many chapters from chapter {x} you'd like to get"

    sourceUpdate = "You have chosen the source: "

    def __init__(self):
        self.source = ""
        self.query = ""
        self.chapter = 0
        self.count = 1
        self.mangaList = ""
        self.urls = []
        self.title = ""
        self.reply = ""
        self.queryReply = ""

    def getChooseSource(self) -> str:
        return self.chooseSource

    def updateSource(self, source) -> str:
        self.source = source
        self.reply = self.sourceUpdate + source
        return self.reply + self.searchManga

    def updateTitle(self, query, urls) -> str:
        reply = self.reply + self.queryUpdate + query + "\n"
        mangaList = "\n"
        for i, v in enumerate(urls):
            mangaList += f"{i+1}. {v[1]} \n"
        self.mangaList = mangaList
        self.urls = urls
        return reply + self.showTitles + mangaList


    def chapterUpdate(self, title: str):
        self.title = title
        self.reply += self.titleUpdate + title
        return self.reply + self.getChapters

    def getCount(self, baseChapter: int) -> str:
        self.chapter = baseChapter
        return self.reply + self.getCountString(baseChapter)


    def getGrabManga(self, count: int) -> str:
        self.count = count
        if self.count == 1:
            return self.reply + f" chapter {self.chapter}."
        return self.reply + f" chapter {self.chapter} - chapter {self.chapter + self.count - 1}."

    def getFinalCaption(self) -> str:
        if self.count > 1:
            return f"{self.end} {self.title} Chapter {self.chapter} - Chapter {self.chapter + self.count - 1}"
        return f"{self.end}, {self.title}, Chapter {self.chapter}."
