from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup

initial_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text='J’ai déposé les documents ✅')],
        [KeyboardButton(text='J’ai besoin d’aide 📥')],
        [KeyboardButton(text='FAQ ⁉️')]
    ],
    resize_keyboard=True
)

questions_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text='What is a lion?')],
        [KeyboardButton(text='What is a watermelon?')],
        [KeyboardButton(text='Who is Barack Obama?')],
        [KeyboardButton(text='⬅️Back')],
    ],
    resize_keyboard=True
)