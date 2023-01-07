import os

import gspread
from pyrogram import Client, filters
from pyrogram.types import Message, ForceReply
from pyrogram.types import Photo
from typing import Dict
from keyboards import initial_keyboard, questions_keyboard
from secret import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    CHANNEL_LINK, OWNER_ID
)

bot = Client("BOT_ORDER", api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN)
user_info = {
    'chat_id': 0,
    'first_name': '',
    'last_name': '',
    'mk_number': '',
    'screenshot': ''
}

# Function to reply /start command
@bot.on_message(filters.command(commands=['start']) & filters.private)
async def welcome(client: Client, message: Message):
    await message.reply_text(
        text=f"**Hello, {message.from_user.first_name}!**\n\nPlease, choose an option below!",
        disable_web_page_preview=False, reply_markup=initial_keyboard)


@bot.on_message(filters.command(commands=['menu']) & filters.private)
async def menu(client: Client, message: Message):
    await message.reply_text(
        text=f"**Dear {message.from_user.first_name}!**\n\nPlease, choose an option below!",
        disable_web_page_preview=False, reply_markup=initial_keyboard)


@bot.on_message(
    filters.regex(initial_keyboard.keyboard[0][0].text) & filters.private)
async def get_username(client: Client, message: Message) -> None:
    await message.reply(
        text='Before we proceed, we need to do 2 step Verification.\n\n' \
             'Please, send your **first** and **last name**\n\n' \
             '**/menu** — back to menu',
        reply_markup=ForceReply(
            placeholder="Full name"
        )
    )


@bot.on_message(
    filters.regex(initial_keyboard.keyboard[1][0].text) & filters.private)
async def get_support(client: Client, message: Message) -> None:
    await client.send_message(
        chat_id=message.chat.id,
        text='Send a message to @g0uman 📥'
    )


@bot.on_message(
    filters.regex(initial_keyboard.keyboard[2][0].text) & filters.private)
async def get_FAQ(client: Client, message: Message) -> None:
    await client.send_message(
        chat_id=message.chat.id,
        text='There is the list of FAQ👇🏻',
        reply_markup=questions_keyboard
    )


# First answer
@bot.on_message(
    filters.regex(questions_keyboard.keyboard[0][0].text) & filters.private)
async def get_first_FAQ_answer(client: Client, message: Message) -> None:
    await client.send_photo(
        chat_id=message.chat.id,
        photo='https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Lion_waiting_in_Namibia.jpg/1200px-Lion_waiting_in_Namibia.jpg',
        caption=f'**{questions_keyboard.keyboard[0][0].text}**\n\n'
                'The lion is a large cat of the genus Panthera native to Africa and India. '
                'It has a muscular, broad-chested body; short, rounded head; '
                'round ears; and a hairy tuft at the end of its tail.\n\n'
                f"[Learn more]({'https://en.wikipedia.org/wiki/Lion'})",
        reply_markup=questions_keyboard
    )


# Second answer
@bot.on_message(
    filters.regex(questions_keyboard.keyboard[1][0].text) & filters.private)
async def get_second_FAQ_answer(client: Client, message: Message) -> None:
    await client.send_photo(
        chat_id=message.chat.id,
        photo='https://upload.wikimedia.org/wikipedia/commons/8/89/Citrullus_lanatus5SHSU.jpg',
        caption=f'**{questions_keyboard.keyboard[1][0].text}**\n\n'
                'Watermelon (Citrullus lanatus) is a flowering plant '
                'species of the Cucurbitaceae family and the name of its edible fruit. '
                'A scrambling and trailing vine-like plant, it is a highly '
                'cultivated fruit worldwide, with more than 1,000 varieties.\n\n'
                f"[Learn more]({'https://en.wikipedia.org/wiki/Watermelon'})",
        reply_markup=questions_keyboard
    )


# Third answer
@bot.on_message(
    filters.regex(questions_keyboard.keyboard[2][0].text) & filters.private)
async def get_third_FAQ_answer(client: Client, message: Message) -> None:
    await client.send_photo(
        chat_id=message.chat.id,
        photo='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/220px-President_Barack_Obama.jpg',
        caption=f'**{questions_keyboard.keyboard[2][0].text}**\n\n'
                'Barack Hussein Obama II is an American politician who served '
                'as the 44th president of the United States from 2009 to 2017.\n\n'
                f"[Learn more]({'https://en.wikipedia.org/wiki/Barack_Obama'})",
        reply_markup=questions_keyboard
    )


# GO back button
@bot.on_message(
    filters.regex(questions_keyboard.keyboard[3][0].text) & filters.private)
async def get_back_FAQ_answer(client: Client, message: Message) -> None:
    await client.send_message(
        chat_id=message.chat.id,
        text=f'**Dear, {message.from_user.first_name}!**\n\nPlease, choose an option below!',
        reply_markup=initial_keyboard
    )


@bot.on_message()
async def input_handler(client: Client, update: Message):
    global user_info
    print(user_info)
    if update.reply_to_message:
        if update.reply_to_message.reply_markup.placeholder == "Full name":
            # Split the message text into first and last
            try:
                # Name error handling
                names = update.text.split(' ')
                if len(names) == 1:
                    await client.send_message(
                        chat_id=update.chat.id,
                        text='Please enter your __first__ and __last__ __name__ to continue',
                        reply_markup=ForceReply(
                            placeholder="Full name"
                        )
                    )
                    return
                else:
                    first_name = names[0].title()
                    last_name = names[1].title()
                    greeting = f"**Hello, {first_name} {last_name}!**\n\n" \
                               f"Please respond to this message with your ID number.\n\n" \
                               f"**/menu** — back to menu"

                    await client.send_message(
                        chat_id=update.chat.id,
                        text=greeting,
                        reply_markup=ForceReply(
                            placeholder='Identification number')
                    )

                    user_info['chat_id'] = update.chat.id
                    user_info['first_name'] = first_name
                    user_info['last_name'] = last_name

            except Exception:
                pass
        if update.reply_to_message.reply_markup.placeholder == "Identification number":
            try:
                if not update.text[:2].lower() in ['mk', 'mK', 'Mk']:
                    await client.send_message(
                        chat_id=update.chat.id,
                        text="Invalid ID number. Please ensure that it starts with 'MK'",
                        reply_markup=ForceReply(
                            placeholder="Identification number"
                        )
                    )
                    return
                else:
                    id_number = update.text
                    # screenshot
                    await client.send_message(
                        chat_id=update.chat.id,
                        text='Envoie-moi la preuve de dépôt que Markets t’a envoyé par mail',
                        reply_markup=ForceReply(
                            placeholder='Screenshot')
                    )
                    if user_info['chat_id'] == update.chat.id:
                        user_info['mk_number'] = id_number


            except Exception:
                pass
        if update.reply_to_message.reply_markup.placeholder == "Screenshot":

            try:
                if type(update.photo) == Photo:
                    reply_text = f"Congratulations, you have passed the verification✅\n\n" \
                                 f"Here is the link to our secret " \
                                 f"[Telegram Channel]({CHANNEL_LINK})\n\n"
                    await client.send_message(
                        chat_id=update.chat.id,
                        text=reply_text,
                        disable_web_page_preview=True,
                        reply_markup=initial_keyboard
                    )
                    screenshot = await bot.download_media(
                        message=update.photo.file_id, file_name="photo.jpg")
                    with open(screenshot, "rb"):
                        if user_info['chat_id'] == update.chat.id:
                            user_info['screenshot'] = screenshot
                else:
                    await client.send_message(
                        chat_id=update.chat.id,
                        text="We were unable to process the photo you sent. Please send a valid photo in compressed mode.",
                        reply_markup=ForceReply(
                            placeholder="Screenshot"
                        )
                    )
                    return


            except Exception:
                pass

    if len(user_info) == 3:
        print(len(user_info))
        try:
            await client.send_photo(
                chat_id=OWNER_ID,
                photo=user_info['screenshot'],
                caption=
f"""**New User**

**First name**: {user_info['first_name']}
**Last name:** {user_info['last_name']}
**Username:** @{'Not Available' if update.chat.username is None else update.chat.username}
**MK number:** `{user_info['mk_number']}`
"""
            )

            if os.path.exists(user_info['screenshot']):
                os.remove(user_info['screenshot'])
        except Exception:
            pass

        else:
            await client.send_message(
                chat_id=update.chat.id,
                text='Send **/menu** to see actions'
            )
    single_user = update.chat.id
    return post_user_fullname(user_info, single_user)


def post_user_fullname(user_info, single_user):
    sa = gspread.service_account(filename='creds.json')
    sheet_file = sa.open('telegram_test')
    sheet = sheet_file.worksheet('records')

    if len(user_info) == 4 and single_user == user_info['chat_id']:
        try:
            sheet.append_row(
                [
                    str(user_info['first_name']),
                    str(user_info['last_name']),
                    str(user_info['mk_number']),
                ]
            )
        except Exception:
            pass

    return


print('Bot has started')
if __name__ == "__main__":
    bot.run()
print('Bot has stopped')
