import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import os
import environs
import segno

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
    photo = FSInputFile(os.path.join("media", "image.png"))
    await bot.send_photo(message.chat.id, photo=photo)


@dp.message(Command("qrcode"))
async def get_qr_code(message: types.Message):
    if os.path.exists(os.path.join("media", "qrcode.png")):
        photo = FSInputFile(os.path.join("media", "qrcode.png"))
        await bot.send_photo(message.chat.id, photo)
    qrcode_photo = segno.make_qr(
        content=f"https://t.me/{env.str('BOT_USERNAME')}?start=start"
    )
    qrcode_photo.save("media/qrcode.png")
    photo = FSInputFile(os.path.join("media", "qrcode.png"))
    await bot.send_photo(message.chat.id, photo)



if __name__ == "__main__":

    async def main():
        # Delete webhook before starting polling
        await bot.delete_webhook(drop_pending_updates=True)
        # Start polling
        await dp.start_polling(bot)

    import asyncio

    asyncio.run(main())
