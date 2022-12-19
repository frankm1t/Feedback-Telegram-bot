from aiogram import types



menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    types.KeyboardButton('Панель адміністратора 🛠')
)

adm = types.ReplyKeyboardMarkup(resize_keyboard=True)
adm.add(
    types.KeyboardButton('Заблоковані користувачі 📋'),
    types.KeyboardButton('Заблокувати 🚫'),
    types.KeyboardButton('Розблокувати ❎')
)
adm.add(
    types.KeyboardButton('Адміністратори 📖'),
    types.KeyboardButton('Розсилка 📨')
)

adm.add('Назад ◀️')

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(
    types.KeyboardButton('Скасування')
)


def fun(user_id):
    quest = types.InlineKeyboardMarkup(row_width=3)
    quest.add(
        types.InlineKeyboardButton(text='Відповісти ✅', callback_data=f'{user_id}-ans')
    )
    quest.add(
        types.InlineKeyboardButton(text='Видалити 🗑', callback_data='ignor'),
        types.InlineKeyboardButton(text='Заблокувати 🚫', callback_data=f'{user_id}-ban'),
    )
    return quest