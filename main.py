import uuid
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

env = environs.Env()
env.read_env()
API_TOKEN = env.str("BOT_TOKEN")
BOT_USERNAME = env.str("BOT_USERNAME")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
CERTIFICATES_DIR = "media/certificates"
QRCODE_DIR = "media/qrcode"
os.makedirs(CERTIFICATES_DIR, exist_ok=True)
os.makedirs(QRCODE_DIR, exist_ok=True)


class CertificateState(StatesGroup):
    picture = State()


@dp.message(Command("start"))
async def start_message(message: Message):
    print(message.text)
    msg = f"""Assalomu alaykum {message.from_user.full_name}\n «IT ACADEMY NAMANGAN» MCHJ НАМАНГАН Ш., МФО:00873; ИНН:311130419; Манзил:   Namangan viloyati Namangan shahar Yangi yol MFY, Yikchilik ko'chasi, 32-uy Рахбар:SHARIPOV AKBARALI MUMINOVICH"""
    await message.answer(msg)
    try:
        pic_uuid = message.text.split(" ")[1].strip()
        parsed_uuid = uuid.UUID(pic_uuid)
    except (IndexError, ValueError):
        await message.answer("😔 Rasm UUID sini uzatishda xatolik")
        return
    pic_filename = f"{parsed_uuid}.png"
    pic_path = os.path.join(CERTIFICATES_DIR, pic_filename)
    if os.path.exists(pic_path):
        photo = FSInputFile(pic_path)
        await bot.send_photo(
            message.chat.id,
            photo,
            caption=f"😁 Marhamat {message.from_user.full_name}!",
        )
    else:
        await message.answer("😔 Uzr, sertifikat topilmadi")


@dp.message(Command("pic"))
async def handle_pic_command(message: Message, state: FSMContext):
    await message.answer("Iltimos, sertifikat rasmini jo'nating")
    await state.set_state(CertificateState.picture)


@dp.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi!")


@dp.message(CertificateState.picture)
async def handle_picture_state(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("⚠️ Iltimos yaroqli sertifikat rasmini jo'nating!!!")
        return
    pic_uuid = str(uuid.uuid4())
    pic_filename = f"{pic_uuid}.png"
    pic_path = os.path.join(CERTIFICATES_DIR, pic_filename)
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    await bot.download_file(file_info.file_path, pic_path)
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


if __name__ == "__main__":

    async def main():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    import asyncio

    asyncio.run(main())
