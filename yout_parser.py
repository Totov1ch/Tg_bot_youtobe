import hashlib

from aiogram import Bot, types
from dotenv import load_dotenv, find_dotenv
from aiogram.dispatcher import Dispatcher
import aiogram.utils
from youtube_search import YoutubeSearch
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import os

load_dotenv(find_dotenv())

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


def searcher(text):
    res = YoutubeSearch(text, max_results=10).to_dict()
    return res


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or "echo"
    links = searcher(text)

    articles = [InlineQueryResultArticle(
        id=hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title=f'{link["title"]}',
        url=f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}')
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)


aiogram.utils.executor.start_polling(dp, skip_updates=True)
