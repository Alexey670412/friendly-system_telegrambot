#2100973927:AAFcrypN-1vmtdtVVWp6pufJmbosiWcmJA8 Token
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BASE_URL = 'https://news.ykt.ru'


def start_cmd(update: Update, context: CallbackContext):
    update.message.reply_text("Hello!")

def get_news_cmd(update: Update, context: CallbackContext):
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    sidebar = soup.find(id='left-float-wrapper')
    text = 'News not found'
    links = sidebar.find_all('a', class_='n-latest-news_title_link')
    if links:
        link = links[0]
        for span in link('span'):
            span.decompose()
        url = BASE_URL + link['href']
        text = f'<a href="{url}">{link.text}</a>'
    update.message.reply_html(text, disable_web_page_preview=True)

with open('token.txt') as f:
    token = f.readline()
updater = Updater(token)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start_cmd))
dispatcher.add_handler(CommandHandler('get_news', get_news_cmd))

updater.start_polling()
updater.idle()
