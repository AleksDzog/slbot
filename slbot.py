import dotenv   
from os.path import join, dirname
import time
import os
import sys
from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher


def get_from_env(key):
    """Получение секретного ключа из файла."""
    dotenv_path = join(dirname(__file__), '.env')
    dotenv.load_dotenv(dotenv_path)
    return os.environ.get(key)  # Возвращен токен

bot = Bot(token=get_from_env("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """Команда Старт."""
    await bot.send_message(message.from_user.id, 'Вы нажали кнопку Старт')


@dp.message_handler()
async def text_message(message: types.Message):
    """Любое текстовое сообщение."""
    await bot.send_message(message.from_user.id, f'echo: {message.text}')


def format_end(value, measure):
    if 11 <= value % 100 <= 14:
        if measure == 'day':
            return 'дней'
        elif measure == 'hour':
            return 'часов'
        elif measure == 'minute':
            return 'минут'
    elif 2 <= value % 10 <= 4:
        if measure == 'day':
            return 'дня'
        elif measure == 'hour':
            return 'часа'
        elif measure == 'minute':
            return 'минуты'
    elif value % 10 == 1:
        if measure == 'day':
            return 'день'
        elif measure == 'hour':
            return 'час'
        elif measure == 'minute':
            return 'минута'
    else:
        if measure == 'day':
            return 'дней'
        elif measure == 'hour':
            return 'часов'
        elif measure == 'minute':
            return 'минут'
    


def work_time(bot_start_time):
    """Перевод рабочего времени в дд.чч.мм.сс."""
    wt = time.time() - bot_start_time
    wd = int(wt // 86400)
    wh = int(wt % 86400 // 3600)
    wm = int(wt % 86400 % 3600 // 60)
    ws = wt % 86400 % 3600 % 60 // 1
    wms = wt % 86400 % 3600 % 60 % 1
    print(f'Время работы бота: {wd} {format_end(wd, "day")} {wh} {format_end(wh, "hour")} {wm} ' +
          f'{format_end(wm, "minute")} {ws+round(wms, 2)} секунд')


if __name__ == '__main__':
    bot_start_time = time.time()
    print(f'Время старта: {time.ctime(bot_start_time)}')
    executor.start_polling(dp)
    print(f'Время завершения: {time.ctime(time.time())}')
    work_time(bot_start_time)