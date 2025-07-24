from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.states import States

def choice_keyboard():
    buttons = [
        InlineKeyboardButton("✍️", callback_data='create'),
        InlineKeyboardButton("💾", callback_data='save'),
        InlineKeyboardButton("Отмена", callback_data='cancel'),
    ]
    return InlineKeyboardMarkup([buttons])

def image_keyboard():
    buttons = [
        InlineKeyboardButton("Использовать картинку", callback_data='use_image'),
        InlineKeyboardButton("Без изображения", callback_data='no_image'),
        InlineKeyboardButton("Отмена", callback_data='cancel'),
    ]
    return InlineKeyboardMarkup([buttons])

def type_keyboard(types: list):
    buttons = [
        InlineKeyboardButton(t['label'], callback_data=t['key']) for t in types
    ] + [InlineKeyboardButton("Отмена", callback_data='cancel')]
    # split into rows of 2
    rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(rows)
