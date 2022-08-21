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


if __name__ == '__main__':
    executor.start_polling(dp)
