import os
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode

# Set your Telegram bot token
bot_token = 'YOUR:TG_TOKEN'
# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

bot = Bot(token=bot_token)
dp = Dispatcher(bot)
prev_message = ""

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Для того, чтобы пользоваться ботом, просто напишите мне сообщение. Я готов ответить на ваши вопросы!", parse_mode=ParseMode.HTML)

@dp.message_handler()
async def generate_response(message: types.Message):
    global prev_message
    user_input = prev_message + message.text

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_input,
        temperature=0.7,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["\n"]
    )

    prev_message = user_input + response.choices[0].text

    await bot.send_message(message.chat.id, response.choices[0].text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)