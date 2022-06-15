class Manga:

    def __init__(self, title: str, url: str, latestChapter: int):
        # find some way to store source
        self.title = title
        self.url = url
        self.latestChapter = latestChapter
