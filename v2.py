import uuid
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
import environs
import logging
import os
from utils import gen_qr_code
from aiogram.types.input_file import InputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# Environment and bot setup
env = environs.Env()
env.read_env()
API_TOKEN = env.str("BOT_TOKEN")
BOT_USERNAME = env.str("BOT_USERNAME")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Directories for storing certificates and QR codes
CERTIFICATES_DIR = "media/certificates"
QRCODE_DIR = "media/qrcode"
os.makedirs(CERTIFICATES_DIR, exist_ok=True)
os.makedirs(QRCODE_DIR, exist_ok=True)

# SQLite database setup
conn = sqlite3.connect("certificates.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        image_path TEXT NOT NULL
    )
"""
)
conn.commit()


# States for managing user input
class CertificateState(StatesGroup):
    fullname = State()
    picture = State()


@dp.message(Command("start"))
async def start_message(message: Message):
    msg = f"""Assalomu alaykum {message.from_user.full_name}\n «IT ACADEMY NAMANGAN» MCHJ НАМАНГАН Ш., МФО:00873; ИНН:311130419; Манзил:   Namangan viloyati Namangan shahar Yangi yol MFY, Yikchilik ko'chasi, 32-uy\n\nIT Park resident N 14/11 29.03.2024\n\nConfirmation N 2576\n\nTa’sischi: Sharipov Akbarali \nRahbar: ABDUVALIYEV JALOLIDDIN JAMОЛ O’G’ЛI\nAloqa: +998999145888"""
    await message.answer(msg)


@dp.message(Command("create"))
async def handle_pic_command(message: Message, state: FSMContext):
    await message.answer("Iltimos, to'liq ismingizni kiriting:")
    await state.set_state(CertificateState.fullname)


@dp.message(CertificateState.fullname)
async def handle_fullname_state(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Iltimos, sertifikat rasmini jo'nating:")
    await state.set_state(CertificateState.picture)


@dp.message(CertificateState.picture)
async def handle_picture_state(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("⚠️ Iltimos yaroqli sertifikat rasmini jo'nating!!!")
        return

    user_data = await state.get_data()
    fullname = user_data.get("fullname")

    # Generate unique filename and save the image
    pic_uuid = str(uuid.uuid4())
    pic_filename = f"{pic_uuid}.png"
    pic_path = os.path.join(CERTIFICATES_DIR, pic_filename)
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    await bot.download_file(file_info.file_path, pic_path)

    # Save the certificate information to the database
    cursor.execute(
        "INSERT INTO certificates (fullname, image_path) VALUES (?, ?)",
        (fullname, pic_path),
    )
    conn.commit()

    # Generate and send QR code
    qr_code_url = f"https://t.me/{BOT_USERNAME}?start={pic_uuid}"
    qr_code_path = os.path.join(QRCODE_DIR, f"{pic_uuid}.png")
    gen_qr_code(qr_code_url, filename=qr_code_path)
    qr_code_file = FSInputFile(qr_code_path)
    await bot.send_photo(
        message.chat.id,
        qr_code_file,
        caption="😁 Sertifikatga shu qr code orqali kirishingiz mumkin!",
    )
    await state.clear()


# New handler to search for a certificate by full name using LIKE
@dp.message(Command("search"))
async def handle_search_command(message: Message):
    await message.answer("Iltimos, to'liq ismingizni kiriting:")


@dp.message()
async def handle_fullname_search(message: Message):
    fullname = message.text.strip()
    # Use LIKE with wildcards for partial matching
    cursor.execute(
        "SELECT image_path FROM certificates WHERE fullname LIKE ?", (f"%{fullname}%",)
    )
    result = cursor.fetchone()
    if result:
        image_path = result[0]
        if os.path.exists(image_path):
            photo = FSInputFile(image_path)
            await bot.send_photo(
                message.chat.id,
                photo,
                caption=f"😁 Marhamat {message.from_user.full_name}!",
            )
        else:
            await message.answer("😔 Sertifikat topilmadi.")
    else:
        await message.answer("😔 Uzr, bunday ism bilan sertifikat topilmadi.")


@dp.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi!")


if __name__ == "__main__":

    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    import asyncio

    asyncio.run(main())
