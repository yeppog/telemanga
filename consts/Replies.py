

class Replies:
    grabManga = "Alright, getting you your manga:"
    
    @classmethod
    def getGrabManga(self,url: str) -> str:
        return f"{self.grabManga} {url}"
