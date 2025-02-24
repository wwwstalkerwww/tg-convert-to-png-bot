import os
import asyncio
import pillow_heif  # Поддержка AVIF
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
from PIL import Image

# Глобальная переменная с токеном
TOKEN = "YOU_BOT_TOKEN"

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

        # Проверяем содержимое файла
        with open(webp_path, "rb") as f:
            first_bytes = f.read(20)
        print(f"[BOT] Первые 20 байт файла: {first_bytes}")

        # Если это AVIF – используем pillow-heif
        if b"ftypavif" in first_bytes:
            print("[BOT] Файл - AVIF! Конвертируем через pillow-heif.")
            heif_image = pillow_heif.open_heif(webp_path)
            img = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
        else:
            # Обычный WebP
            img = Image.open(webp_path)

        # Сохраняем в PNG
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

@dp.message(lambda message: message.document is not None)
async def handle_document(message: types.Message):
    """ Обрабатываем файлы webp """
    document = message.document

    if not document.file_name.lower().endswith(".webp"):
        await message.answer("Я могу конвертировать только файлы в формате .webp!")
        return

    webp_path = os.path.join(TEMP_FOLDER, document.file_name)
    png_path = os.path.join(TEMP_FOLDER, document.file_name.replace(".webp", ".png"))

    try:
        print("[BOT] Загружаем файл...")
        await asyncio.sleep(2)

        await bot.download(document.file_id, webp_path)
        print(f"[BOT] Файл загружен! Размер: {os.path.getsize(webp_path)} байт")

        # Проверяем содержимое файла
        with open(webp_path, "rb") as f:
            first_bytes = f.read(20)
        print(f"[BOT] Первые 20 байт файла: {first_bytes}")

        # Если это AVIF – используем pillow-heif
        if b"ftypavif" in first_bytes:
            print("[BOT] Файл - AVIF! Конвертируем через pillow-heif.")
            heif_image = pillow_heif.open_heif(webp_path)
            img = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
        else:
            # Обычный WebP
            img = Image.open(webp_path)

        # Сохраняем в PNG
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
