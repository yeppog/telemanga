import asyncio
import os
from consts.Replies import Replies
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scrapers.MangaFoxScraper import MangaFoxScraper
from service.ImageService import ImageService


class Telegram:

    async def getManga(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        link = update.message.text.split(" ")[1]
        await context.bot.delete_message(update.message.chat_id, update.message.message_id)
        await context.bot.send_message(update.message.chat_id, Replies.getGrabManga(link), disable_web_page_preview=True)
        title = MangaFoxScraper.parseNames(link)
        manga = MangaFoxScraper.getMangaPages(self.sel.getDriver(), link)
        fileUrl = await ImageService.parsePDF(manga, title)
        try:
            document = open(fileUrl, 'rb')
            await context.bot.send_document(update.message.chat_id, document=document)
            # probably need to check for any directory traversal links to avoid blowing up
            # the entire directory by deleting shit..
            os.remove(fileUrl)

        except Exception as e:
            print(e)

    def __init__(self, key, sel):
        app = ApplicationBuilder().token(key).build()
        self.app = app
        self.sel = sel
        app.add_handler(CommandHandler("getManga", self.getManga))

    def addHandler(self, commandStr, commandFn):
        self.app.add_handler(commandStr, commandFn)

    def run(self):
        self.app.run_polling()

