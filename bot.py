import os 
import asyncio
import sqlite3 
from dotenv import load_dotenv      #  pip install python-dotenv # переменная среда 
from aiogram import Dispatcher, Bot #  pip install aiogram
from aiogram.types import Message, FSInputFile, CallbackQuery , BufferedInputFile , ReplyKeyboardMarkup , KeyboardButton
from aiogram import types
from aiogram.filters.command import Command
from datetime import datetime
from analise import get_user_notes , plot_user_notes 

load_dotenv()
# машинное состояние ?
# словарь для хранения состояния пользователя 
notedata = {}

start_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Внести данные"), KeyboardButton(text="Моя статистика")]])

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

quersions = [
    "Оцените ваше самочувствие от 1 до 10", 
    "Какая итоговая сумма трат за день у вас вышла ?",
    "еще вопросы можно задать"
            ]

cursor.execute(
    """
    CREATE TABLE 
    IF NOT EXISTS tablica(
        user_id INTEGER, 
        date TEXT DEFAULT (datetime('now', 'localtime')),
        money INTEGER,
        feels INTEGER,
        comments TEXT
    )
    """
)


bot = Bot(os.getenv("TOKEN")) # подключили токен ключа
dp = Dispatcher()  # диспетчер для обработки запросов 
@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer("Бот запущен", reply_markup=start_markup)
    
@dp.message(Command('about'))
async def about_command(message: Message):
    await message.answer("текст описания", reply_markup=start_markup)
    
@dp.message(lambda message: message.text == "Внести данные")
async def tone_command(message: Message):
    user_id = message.from_user.id
    
    notedata[user_id]={ "step": 0 } 
    await bot.send_message(user_id, "Оцените ваше самочувствие от 1 до 10" )

# lambda - анонимная функция 
@dp.message(lambda message:message.from_user.id in notedata)
async def process_question(message:Message):
    user_id = message.from_user.id
    step = notedata[user_id]["step"]
    notedata[user_id][quersions[step]] = message.text
    
    step += 1
    notedata[user_id]["step"] = step
    
    if step < len(quersions):
        await bot.send_message(user_id, f"{quersions[step]}")
    else:
        save(user_id, notedata[user_id])
        del notedata[user_id]
        await bot.send_message(user_id, "Спасибо! Ваши данные сохранены")
    
def save(user_id , data):
    cursor.execute(
    """
        INSERT  INTO tablica (
        user_id, feels, money, comments) VALUES (?, ?, ?, ?)
    """, 
    (user_id, 
                data["Оцените ваше самочувствие от 1 до 10"],
                data["Какая итоговая сумма трат за день у вас вышла ?"],
                data["еще вопросы можно задать"]
    )
    )
    conn.commit()

@dp.message(lambda message: message.text == "Моя статистика")
async def start_note_collection_command(message: Message):
    user_id = message.from_user.id
    # if user_exists(user_id):
    notes_df = get_user_notes(user_id)
    if notes_df.empty:
        await bot.send_message(user_id, "У вас ещё нет заметок" , reply_markup=start_markup)
    else:
        # goal = get_goal(user_id)
        # if goal != None:
        plots = plot_user_notes(notes_df)
        for name, img_bytes in plots.items():
            await bot.send_photo(chat_id=message.chat.id, photo=BufferedInputFile(file=img_bytes.read(), filename=f'{name}.png'), reply_markup=start_markup)
    # else:
        # await bot.send_message(user_id, "У вас ещё нет профиля, пожалуйста, создайте его, нажав на кнопку 'Мой профиль'.")
    
async def main(): 
    print("bot is ready")
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())      # безопасный запуск / всегда

# вершина состояний
# айди + дата автоматическая 
# @dp диспетчер  / @ декоратор 

