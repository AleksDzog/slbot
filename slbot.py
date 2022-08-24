"""Speech to letter telegram bot."""

import os
import sys
import time
from os.path import dirname, join

import dotenv
import soundfile
import speech_recognition as sr
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils import executor
from aiogram.utils.markdown import pre, text  # , bold, italic, code

import keyboard as kb

FILE_VERSION = '0.0.1'


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
    await bot.send_message(message.from_user.id, 'Вы нажали кнопку Старт',
                           reply_markup=kb.menu_kb)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    """Команда Помощь."""
    await bot.send_message(message.from_user.id, 'Вы нажали кнопку Помощь')


@dp.message_handler(commands=['stop'])
async def process_stop_command(message: types.Message):
    """Команда Остановки бота."""
    await bot.send_message(message.from_user.id, 'Вы нажали кнопку Остановить')


@dp.message_handler()
async def text_message(message: types.Message):
    """Любое текстовое сообщение."""
    await bot.send_message(message.from_user.id, f'echo: {message.text}')


async def recognize(path):
    wavpath = join(dirname(path), f"{path.split('/')[-1][:-4]}.wav")
    print(wavpath)
    data, samplerate = soundfile.read(path)
    print(data)
    print(samplerate)
    input()
    soundfile.write(wavpath, data, samplerate)
    r = sr.Recognizer()
    with sr.AudioFile(wavpath) as source:
        audio = r.record(source)
        print(r.recognize_google(audio, language="ru-RU"))


async def dwnld_file(file, file_name, path):
    """Скачать файл.

    Args:
        file (File): Объект файла
        file_name (string): Имя файла
        path (string): Директория
    """
    os.makedirs(path, exist_ok=True)
    await bot.download_file(file.file_path, destination=f'{path}/{file_name}')
    return f'{path}/{file_name}'


@dp.message_handler(content_types=ContentType.VOICE)
async def voice_message(message: types.Message):
    """Голосовое сообщение."""
    voice = await message.voice.get_file()
    path = join(dirname(__file__), 'files/voices')
    await recognize(await dwnld_file(voice, f'{voice.file_id}.ogg', path))


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    """Любое сообщение не обработанное ранее."""
    answer = text(pre('Непонятное сообщение, используйте команду '), '/help')
    await message.reply(answer, parse_mode=ParseMode.MARKDOWN)
    print(message)


def format_end(value, measure):
    """Определение окончания слова.

    Args:
        value (integer): число дней/часов/минут
        measure (string): единица измерения день/час/минута

    Returns:
        string: окончание
    """
    endict = {
        'day': ['дней', 'дня', 'день'],
        'hour': ['часов', 'часа', 'час'],
        'minute': ['минут', 'минуты', 'минута']
    }
    if 11 <= value % 100 <= 14:
        return endict[measure][0]
    elif 2 <= value % 10 <= 4:
        return endict[measure][1]
    elif value % 10 == 1:
        return endict[measure][2]
    else:
        return endict[measure][0]


def work_time(bot_start_time):
    """Перевод рабочего времени в дд.чч.мм.сс."""
    wt = time.time() - bot_start_time
    wd = int(wt // 86400)
    wh = int(wt % 86400 // 3600)
    wm = int(wt % 86400 % 3600 // 60)
    ws = round(wt % 86400 % 3600 % 60, 3)
    wms = int((ws - int(ws)) * 1000)
    print(f'Время работы бота: {wd} {format_end(wd, "day")} ' +
          f'{wh} {format_end(wh, "hour")} {wm} ' +
          f'{format_end(wm, "minute")} {int(ws)}.{wms} секунд')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # если запущен без аргументов
        bot_start_time = time.time()  # время запуска бота
        print(f'Время старта: {time.ctime(bot_start_time)}')

        executor.start_polling(dp, skip_updates=True)

        print(f'Время завершения: {time.ctime(time.time())}')
        work_time(bot_start_time)
    elif '-ver' in sys.argv:
        # если среди аргументов запрашивается версия
        print(FILE_VERSION)
