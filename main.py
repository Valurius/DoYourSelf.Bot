from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.utils import executor
from user import User
import requests

# Вставьте ваш токен бота здесь
TOKEN = '7194534654:AAFdYI7bIgouUXiYnqpN9z6m-sfopJNGZ8c'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def send_message(chat_id):
    await bot.send_message(chat_id, 'Привет')


# Хендлер для команды /start
@dp.message_handler(commands=['start'])
async def register_user(msg: types.Message):
    
    if msg.chat.type == "private":
        await msg.answer("Нажмите на кнопку ниже, чтобы отправить контакт", reply_markup=await contact_keyboard())


async def continue_register_user(msg, data):
    chat_id = data.get("id")
    phone_number = data.get("phone_number")
    response = await User.register_by_number(phone_number, chat_id)

    await msg.answer(response)

# Получение номера
async def contact_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_phone = KeyboardButton('Отправить номер телефона', request_contact=True)
    markup.add(button_phone)
    return markup


# Обработчик, который получает контакт
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(msg: types.Message):
    contact = msg.contact
    await msg.answer(f"Спасибо, {contact.full_name}.\nВаш номер {contact.phone_number} был получен",
                     reply_markup=ReplyKeyboardRemove())

    data_values = {"id": msg.chat.id, "phone_number": contact.phone_number}
    await continue_register_user(msg, data_values)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
