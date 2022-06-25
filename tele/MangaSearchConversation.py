import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from consts.Replies import Replies
from scrapers.MangaFoxScraper import MangaFoxScraper
from service.ImageService import ImageService

SOURCE, SEARCH, CHAPTER, COUNT, FETCH, FINISH = range(6)


class MangaSearchConversation:

    def __init__(self, driver):
        self.driver = driver

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        reply_keyboard = [["MangaFox"]]
        reply = Replies()
        context.user_data['replies'] = reply
        context.user_data["botMessage"] = await update.message.reply_text(
            reply.getChooseSource(),
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True
            )
        )
        return SOURCE

    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # cleanup
        await handleMessageDelete(update, context)

        context.user_data["source"] = update.message.text
        replies = context.user_data["replies"].updateSource(
            update.message.text)
        context.user_data["botMessage"] = await update.message.reply_text(
            replies,
            reply_markup=ReplyKeyboardRemove()
        )
        return SEARCH

    async def selectTitle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # cleanup
        await handleMessageDelete(update, context)

        context.user_data["search"] = update.message.text
        titles = MangaFoxScraper.getMangaTitles(
            self.driver.getDriver(), update.message.text)
        context.user_data["urls"] = titles
        replies = context.user_data['replies'].updateTitle(update.message.text, titles)
        context.user_data["botMessage"] = await update.message.reply_text(
            replies, disable_web_page_preview=True,
            reply_markup=ReplyKeyboardRemove()
        )
        return CHAPTER

    async def selectChapters(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await handleMessageDelete(update, context)
        result = context.user_data["urls"][int(
            update.message.text) - 1]
        context.user_data['url'] = result[0]
        context.user_data['title'] = result[1]
        replies = context.user_data['replies'].chapterUpdate(result[1])
        context.user_data["botMessage"] = await update.message.reply_text(
            replies,
            reply_markup=ReplyKeyboardRemove()
        )
        return COUNT

    async def getCount(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await handleMessageDelete(update, context)
        chapter = int(update.message.text)
        context.user_data["chapter"] = chapter
        msg = context.user_data["replies"].getCount(chapter)
        context.user_data["botMessage"] = await update.message.reply_text(
            msg,
            reply_markup=ReplyKeyboardRemove()
        )
        return FETCH

    async def fetch(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await handleMessageDelete(update, context)
        count = int(update.message.text)
        chapter = context.user_data["chapter"]
        link = context.user_data["url"]
        msg = context.user_data["replies"].getGrabManga(count)
        await context.bot.send_message(update.message.chat_id, msg, disable_web_page_preview=True)
        fileName = MangaFoxScraper.parsePDFName(context.user_data['title'], chapter, count)
        manga = await MangaFoxScraper.getMangaPages(
            self.driver.getDriver(), link, chapter, count)

        fileUrl, err = await ImageService.parsePDF(manga, fileName)
        if err != None:
            await context.bot.send_message(update.message.chat_id, err)
            return ConversationHandler.END

        caption = context.user_data["replies"].getFinalCaption()
        try:
            document = open(fileUrl, 'rb')
            await context.bot.send_document(update.message.chat_id, caption=caption, document=document)
            # probably need to check for any directory traversal links to avoid blowing up
            # the entire directory by deleting shit..
            os.remove(fileUrl)

        except Exception as e:
            if "413" in e:
                await context.bot.send_message(update.message.chat_id, "Issue sending manga. Perhaps the file is too large.")
            print(e)
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # user = update.message.from_user
        await update.message.reply_text(
            "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    def getConvoHandler(self):
        return ConversationHandler(
            entry_points=[CommandHandler("getManga", self.start)],
            states={
                SOURCE: [MessageHandler(
                    filters.Regex("^(MangaFox)$"), self.search)],
                SEARCH: [MessageHandler(
                    filters.Regex("^([a-zA -Z0-9]*)$"), self.selectTitle)],
                CHAPTER: [MessageHandler(
                    filters.Regex("^([0-9]*)$"), self.selectChapters)],
                COUNT: [MessageHandler(
                    filters.Regex("^([0-9]*)$"), self.getCount)],
                FETCH: [MessageHandler(
                    filters.Regex("^([0-9]*)$"), self.fetch)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)]
        )


async def handleMessageDelete(update, context):
    try:
        await context.bot.delete_message(update.message.chat_id, update.message.message_id)
        await context.bot.delete_message(update.message.chat_id, context.user_data["botMessage"].message_id)
    except:
        print("Error deleting, please change this to a log")
        pass

