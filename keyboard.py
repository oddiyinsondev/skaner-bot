from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


contact = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="kantakt", request_contact=True)]
    ],
    resize_keyboard=True,
)


user = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Hisobni tekshirish 💸", callback_data="hisob")]
    ]
)

hisob = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Pulni yechish 💴", callback_data="pulni yechish"), InlineKeyboardButton(text="ortga ⬅️", callback_data="ortga")]
    ]
)
Tasdiqlash = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='tasdiqlash ✅', callback_data='tasdiqlash'), InlineKeyboardButton(text='ortga ⬅️', callback_data='zadnin')]
    ]
)


Tolov = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='tasdiqlash ✅', callback_data='bajarish'), InlineKeyboardButton(text='bekor qilish ❌', callback_data='bekor')]
    ]
)