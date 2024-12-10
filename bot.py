from aiogram import Bot, Dispatcher, executor
from config import API_TOKEN
from handlers import register_handlers
import atexit

from data_store import load_data, save_data#, mes_to_execute_and_position
# Так как программа работает не постоянно, нужно добавить сторонний json файл чтобы избежать  if messages_to_execute[user_id]["work"] != []: KeyError: (тут ID пользователя)
# Это возникает когда программа запускается дважды а user_id назначается при старте, хотя юзер делал это при первом запуске. В будующем это можно будет убрать, если прога работает 24/7
# Хотя лучше оставить чтобы иметь возможность делать обновления

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode="MarkdownV2")
dp = Dispatcher(bot)



load_data()

# Регистрация всех обработчиков
register_handlers(dp)


atexit.register(save_data)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


