from pyrogram import Client, filters
from pyrogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ForceReply
import sqlite3
import gspread
from secret import API_ID, API_HASH, BOT_TOKEN

bot = Client("BOT_ORDER", api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

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

@bot.on_message(filters.regex(initial_keyboard.keyboard[0][0].text) & filters.private)
async def get_username(client: Client, message: Message) -> None:
    await message.reply(
        text='Before we proceed, we need to do 2 step Verification.\n\n' \
             'Please, send your **first** and **last name**\n\n' \
             '**/menu** — back to menu',
        reply_markup=ForceReply(
            placeholder="Full name"
        )
    )

@bot.on_message(filters.regex(initial_keyboard.keyboard[1][0].text) & filters.private)
async def get_support(client: Client, message: Message) -> None:
    await client.send_message(
        chat_id=message.chat.id,
        text='Send a message to @g0uman 📥'
    )

@bot.on_message(filters.regex(initial_keyboard.keyboard[2][0].text) & filters.private)
async def get_FAQ(client: Client, message: Message) -> None:
    await client.send_message(
        chat_id=message.chat.id,
        text='There is the list of FAQ👇🏻',
        reply_markup=questions_keyboard
    )

@bot.on_message(filters.regex(questions_keyboard.keyboard[0][0].text) & filters.private)
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

@bot.on_message(filters.regex(questions_keyboard.keyboard[1][0].text) & filters.private)
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

@bot.on_message(filters.regex(questions_keyboard.keyboard[2][0].text) & filters.private)
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

@bot.on_message(filters.regex(questions_keyboard.keyboard[3][0].text) & filters.private)
async def get_back_FAQ_answer(client: Client, message: Message) -> None:
    await client.send_message(
        chat_id=message.chat.id,
        text=f'**Dear, {message.from_user.first_name}!**\n\nPlease, choose an option below!',
        reply_markup=initial_keyboard
    )


# Need to fix this decorator
@bot.on_message()
async def input_name_handler(client: Client, update: Message):
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
                               f"**Example:** MK__123456789__\n\n" \
                               f"**/menu** — back to menu"

                    await client.send_message(
                        chat_id=update.chat.id,
                        text=greeting,
                        reply_markup=ForceReply(placeholder='Identification number')
                    )
            except Exception as err:
                pass

        if update.reply_to_message.reply_markup.placeholder == "Identification number":
            try:
                if not update.text[:2] == 'MK':
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
                    reply_text = f"Congratulations, you have passed the verification✅\n\n" \
                                 f"Here is the link to our secret " \
                                 f"[Telegram Channel]({'https://t.me/+iB4ViV7atY40Y2E0'})\n\n"

                    await client.send_message(
                        chat_id=update.chat.id,
                        text=reply_text,
                        disable_web_page_preview=True,
                        reply_markup=initial_keyboard
                    )
            except Exception as err:
                pass

    else:
        await client.send_message(
            chat_id=update.chat.id,
            text='Send **/menu** to see actions'
        )

    return


def post_user_fullname(first_name, last_name, id_number):

    sa = gspread.service_account(filename='creds.json')
    sheet_file = sa.open('telegram_test')
    sheet = sheet_file.worksheet('records')

    try:
        sheet.append_row(
            [
                str(first_name),
                str(last_name),
                str(id_number),
            ]
        )
    except Exception:
        pass

    return





print('Bot has started')
if __name__ == "__main__":
    bot.run()
print('Bot has stopped')