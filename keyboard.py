"""slbot keyboard."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton
# from aiogram.utils.emoji import emojize

# button_back = KeyboardButton(emojize(':arrow_backward: Назад'))
button_start = KeyboardButton('/start')
button_help = KeyboardButton('/help')
button_stop = KeyboardButton('/stop')

# Основное меню
menu_kb = ReplyKeyboardMarkup(
    resize_keyboard=True
).add(button_start).insert(
    button_help).add(button_stop)
