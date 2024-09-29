from aiogram.types import Message, FSInputFile
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import environs
import logging
import os

from utils import gen_qr_code


env = environs.Env()
env.read_env()
API_TOKEN = env.str("BOT_TOKEN")  # Replace with your actual bot token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Echo handler for "/start" command
@dp.message(Command("start"))
async def start_message(message: Message):
    # Open the image and send it using FSInputFile (updated for aiogram 3.x)
    await message.answer(
        f"""Assalomu alaykum {message.from_user.full_name} \n«IT ACADEMY NAMANGAN» MCHJ НАМАНГАН Ш., МФО:00873; ИНН:311130419; Манзил:   Namangan viloyati Namangan shahar Yangi yol MFY, Yikchilik ko'chasi, 32-uy Рахбар:SHARIPOV AKBARALI MUMINOVICH"""
    )
    photo = FSInputFile(os.path.join("media", "image.png"))
    await bot.send_photo(message.chat.id, photo=photo)
    

@dp.message(Command("qrcode"))
async def get_qr_code(message: types.Message):
    # Generate the QR code and save it
    gen_qr_code(
        f"https://t.me/{env.str('BOT_USERNAME')}?start=start",
        filename="media/qrcode.png",
    )
    # Now check if the QR code file exists and send it
    if os.path.exists(os.path.join("media", "qrcode.png")):
        photo = FSInputFile(os.path.join("media", "qrcode.png"))
        await bot.send_photo(message.chat.id, photo)
    else:
        await message.answer("QR code generation failed. Please try again.")


if __name__ == "__main__":

    async def main():
        # Delete webhook before starting polling
        await bot.delete_webhook(drop_pending_updates=True)
        # Start polling
        await dp.start_polling(bot)

    import asyncio

    asyncio.run(main())
