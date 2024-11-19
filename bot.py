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



# CALLBACK DATA EXAMPLE
#{"id": "3300290482092852398", "from": {"id": 12378483456 "is_bot": false, "first_name": "Иван", "username": "faraamf", "language_code": "en"},
#  "message": {"message_id": 1171, "from": {"id": 8151232315, "is_bot": true, "first_name": "Library", "username": "russian_library_bot"}, 
# "chat": {"id": 41234513467, "first_name": "Иван", "username": "faraamf", "type": "private"},
#  "date": 1730643784, "text": "Произведения Пушкин А. С.:", "reply_markup": {"inline_keyboard": {"text": "19 октября 1827", "callback_data": "work_/author/pushkin/text/629/p.1"},
#  {"text": "19 октября 1828", "callback_data": "work_/author/pushkin/text/658/p.1"}, {"text": "19 октября", "callback_data": "work_/author/pushkin/text/566/p.1"}, 
# {"text": "27 мая 1819", "callback_data": "work_/author/pushkin/text/387/p.1"}, {"text": "«A son amant Eglé sans résistance...»", "callback_data": "work_/author/pushkin/text/423/p.1"},
#  {"text": "➡️ Следующая страница", "callback_data": "page_pushkin_1"}}}, "chat_instance": "-1457524254077791789", "data": "work_/author/pushkin/text/629/p.1"}