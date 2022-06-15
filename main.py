from app import App

if __name__ == "__main__":
    print("start")
    app = App()
    app.run()
    app.getManga("http://mangafox.win/tokyo-revengers-chapter-255#1")
    # app.searchManga("http://mangafox.win", "tokyo")
