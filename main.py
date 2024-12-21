import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery, ReplyKeyboardRemove
from keyboard import contact, user, hisob, Tasdiqlash
import time
from aiogram.fsm.context import FSMContext
from database import get_user, add_user, check_and_add_tolov, hisobdagi_summa, tolov_and_delete
from test import read_qr_code
import os

TOKEN = "7263177243:AAHIyMx5FIKcNyOo_Fj7UXMUVdrIVP4QiEw"
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    rasm = FSInputFile("rasm/apteka.png")
    await message.answer_photo(photo=rasm, caption=f"Assalomu alaykum {message.from_user.first_name}\nBiz bilan ishlamoqchi bo'lganizdan Xursandmzi!\nKantaktni ulashing!", reply_markup=contact)
    await message.delete()


@dp.message(F.contact)
async def ContactBot(message: Message):
    phone = message.contact.phone_number
    add_user(contact=phone, name=message.from_user.first_name, telegram_id = message.from_user.id)
    rasm = FSInputFile('rasm/haspital.webp')
    await message.answer(text="Asosiy menyu ishga tushyabdi", reply_markup=ReplyKeyboardRemove())
    time.sleep(2)
    await message.answer_photo(photo=rasm,caption=f"Siz muvaffaqiyatli royhatdan o'tdingiz! 👌👌👌", reply_markup=user)
    await message.delete()


@dp.callback_query(F.data == 'hisob')
async def HisobBot(call: CallbackQuery):
    telegram_id = call.from_user.id
    a = get_user(telegram_id=telegram_id)
    som = hisobdagi_summa(telegram_id=telegram_id)*5000
    await call.message.answer(f"sizning id: {a['telegram_id']}\nism: {a['name']}\nTelefon: {a['contact']}\nSizning hisobingiz: {som} so'm", reply_markup=hisob)
    await call.message.delete()


@dp.callback_query(F.data=='ortga')
async def OrtgaBot(call: CallbackQuery):
    rasm = FSInputFile("rasm/apteka.png")
    await call.message.answer_photo(photo=rasm, caption=f"Siz asosiy Sahifadasiz 💉💉💉", reply_markup=user)
    await call.message.delete()

@dp.message(F.photo)
async def Photobot(message: Message):
    try:
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file_data = await bot.download_file(file_path)

        save_path = f"code/rasm.png"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(file_data.read())
    except Exception as e:
        await message.reply("Xato yuz berdi: Rasmni yuklab olishda muammo!")
    rasm = FSInputFile("rasm/apteka.png")
    code_id = read_qr_code("code/rasm.png")
    data = check_and_add_tolov(code_id=code_id, telegram_id=message.from_user.id)
    await message.answer(f"{data}")
    time.sleep(2)
    await message.answer_photo(photo=rasm, caption=f"Siz asosiy Sahifadasiz 💉💉💉", reply_markup=user)
   

@dp.callback_query(F.data=="pulni yechish")
async def PulYechibolish(call: CallbackQuery):
    telegram_id = call.from_user.id
    print(telegram_id)
    if hisobdagi_summa(telegram_id=telegram_id):
        som = hisobdagi_summa(telegram_id=telegram_id)*5000
        await call.message.answer(f"ism: {call.from_user.first_name}\nYechib olingan summa: {som} so'm", reply_markup=Tasdiqlash)
    else:
        await call.message.answer("Hisobingizda hali mablag' yo'q")



async def main() -> None:
    await bot.send_message(chat_id=5502720862, text="Bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())