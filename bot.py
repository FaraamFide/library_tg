from aiogram import Bot, Dispatcher, executor
from config import API_TOKEN
from handlers import register_handlers
import atexit

from data_store import load_data, save_data

bot = Bot(token=API_TOKEN, parse_mode="MarkdownV2")
dp = Dispatcher(bot)



load_data()


register_handlers(dp)


atexit.register(save_data)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


