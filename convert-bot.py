import os
import asyncio
import pillow_heif  # Поддержка AVIF
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
from PIL import Image

# Глобальная переменная загружается из окружения
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("ERROR: Не указан TELEGRAM_BOT_TOKEN! Установите переменную окружения.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем папку для временных файлов
TEMP_FOLDER = "temp"
os.makedirs(TEMP_FOLDER, exist_ok=True)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    print("[BOT] Получена команда /start")
    await message.answer("Привет! Отправь мне обычный (неанимированный) стикер или .webp-файл, и я конвертирую его в PNG.")

@dp.message(lambda message: message.sticker is not None)
async def handle_sticker(message: types.Message):
    """ Обрабатываем стикеры """
    sticker = message.sticker

    if sticker.is_animated or sticker.is_video:
        await message.answer("Я могу конвертировать только обычные (неанимированные) стикеры. Попробуй другой!")
        return

    webp_path = os.path.join(TEMP_FOLDER, f"{sticker.file_unique_id}.webp")
    png_path = os.path.join(TEMP_FOLDER, f"{sticker.file_unique_id}.png")

    try:
        print(f"[BOT] Загружаем стикер... (file_id={sticker.file_id})")
        await asyncio.sleep(2)

        await bot.download(sticker.file_id, webp_path)
        print(f"[BOT] Файл загружен! Размер: {os.path.getsize(webp_path)} байт")

        # Открываем изображение (Pillow сам разберётся, AVIF это или WebP)
        with Image.open(webp_path) as img:
            print(f"[BOT] Pillow открыл файл! Формат: {img.format}, Размер: {img.size}, Режим: {img.mode}")
            img.save(png_path, "PNG")

        await message.answer_document(FSInputFile(png_path), caption="Вот твой файл в формате PNG!")

    except Exception as e:
        await message.answer("Ошибка при обработке файла. Попробуй другой!")
        print(f"[ERROR] Ошибка: {e}")

    finally:
        if os.path.exists(webp_path):
            os.remove(webp_path)
        if os.path.exists(png_path):
            os.remove(png_path)

async def main():
    print("[BOT] Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
