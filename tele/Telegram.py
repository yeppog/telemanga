from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tele.MangaSearchConversation import MangaSearchConversation


class Telegram:

    def __init__(self, key, sel):
        app = ApplicationBuilder().token(key).build()
        self.app = app
        self.sel = sel
        # app.add_handler(CommandHandler("getManga", self.getManga))
        conv = MangaSearchConversation(self.sel)
        app.add_handler(conv.getConvoHandler())

    def addHandler(self, commandStr, commandFn):
        self.app.add_handler(commandStr, commandFn)

    def run(self):
        self.app.run_polling()
