import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scrapers.MangaFoxScraper import MangaFoxScraper


class Telegram:

    async def getManga(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.message.text.split(" ")[1]
        manga = MangaFoxScraper.getMangaPages(self.sel.getDriver(), user)
        print(manga)
        for i, (key, val) in enumerate(manga.items()):
            await context.bot.send_document(update.message.chat_id, document=val)
            time.sleep(0.5)

    def __init__(self, key, sel):
        app = ApplicationBuilder().token(key).build()
        self.app = app
        self.sel = sel
        app.add_handler(CommandHandler("getManga", self.getManga))

    def addHandler(self, commandStr, commandFn):
        self.app.add_handler(commandStr, commandFn)

    def run(self):
        self.app.run_polling()
