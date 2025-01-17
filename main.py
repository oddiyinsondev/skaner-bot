import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_user, add_user, check_and_add_tolov, hisobdagi_summa, get_users
from test import read_qr_code
import os
from keyboard import contact, user, hisob, Tasdiqlash, Tolov

TOKEN = "7263177243:AAHIyMx5FIKcNyOo_Fj7UXMUVdrIVP4QiEw"
ADMIN_ID = 5502720862
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    rasm = FSInputFile("rasm/apteka.png")
    await message.answer_photo(photo=rasm, caption=f"Assalomu alaykum {message.from_user.first_name}\nBiz bilan ishlamoqchi bo'lganizdan xursandmiz!\nKantaktni ulashing!", reply_markup=contact)



@dp.message(F.text == "obunachilar", F.from_user.id == ADMIN_ID)
async def Obunachilar(message: Message):
    await message.answer(f"Sizning ubunachilaringiz?\n{get_users()}")

@dp.message(F.contact)
async def ContactBot(message: Message):
    phone = message.contact.phone_number
    add_user(contact=phone, name=message.from_user.first_name, telegram_id=message.from_user.id)
    rasm = FSInputFile('rasm/haspital.webp')
    await message.answer(text="Asosiy menyu ishga tushmoqda", reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(photo=rasm, caption="Siz muvaffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=user)


@dp.message(F.photo)
async def Photobot(message: Message):
    try:
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file_data = await bot.download_file(file_info.file_path)

        save_path = "code/rasm.png"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(file_data.read())

        code_id = read_qr_code("code/rasm.png")
        data = check_and_add_tolov(code_id=code_id, telegram_id=message.from_user.id)
        await message.answer(f"{data}")
    except Exception as e:
        await message.reply("Xato yuz berdi: QR kodni o'qishda muammo!")


@dp.callback_query(F.data == "hisob")
async def HisobBot(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = get_user(telegram_id=telegram_id)
    som = hisobdagi_summa(telegram_id=telegram_id) * 5000
    await call.message.answer(f"Sizning hisobingiz: {som} so'm", reply_markup=hisob)
                                          

@dp.callback_query(F.data == "pulni yechish")
async def PulYechishBot(call: CallbackQuery, state: FSMContext):
    telegram_id = call.from_user.id
    await state.update_data(tel=telegram_id)
    som = hisobdagi_summa(telegram_id=telegram_id) * 5000
    if som > 0:
        await call.message.answer(f"Hisobingizdan {som} so'm yechib olish uchun tasdiqlang.", reply_markup=Tasdiqlash)
    else:
        await call.message.answer("Hisobingizda yetarli mablag' yo'q.")


@dp.callback_query(F.data == "tasdiqlash")
async def TasdiqlashBot(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    telegram_id = data.get("tel")
    user_data = get_user(telegram_id=telegram_id)
    som = hisobdagi_summa(telegram_id=telegram_id) * 5000
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Foydalanuvchi mablag'ni yechib olmoqchi:\nID: {user_data['telegram_id']}\nIsm: {user_data['name']}\nSumma: {som} so'm",
        reply_markup=Tolov
    )
    await call.message.answer("So'rovingiz adminga yuborildi. Tez orada javob beriladi.")


@dp.callback_query(F.data == "bajarish")
async def AdminTasdiqlash(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    telegram_id = data.get("tel")
    if telegram_id:
        await bot.send_message(chat_id=telegram_id, text="Pul yechish so'rovingiz bajarildi. Biz bilan ishlaganingiz uchun rahmat!")
        await call.answer("Tasdiq xabar yuborildi.", show_alert=True)
    else:
        await call.answer("Foydalanuvchi ID si topilmadi.", show_alert=True)


async def main():
    await bot.send_message(chat_id=ADMIN_ID, text="bot ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
