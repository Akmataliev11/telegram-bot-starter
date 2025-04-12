import os
import pytesseract
import cv2
import tempfile
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Переменные окружения
TOKEN = os.getenv("TOKEN")
ИМЯ_ВЛАДЕЛЬЦА = os.getenv("OWNER_NAME")
MBANK_NUMBER = os.getenv("MBANK_NUMBER")
QR_PATH = "qr.png"  # Файл с QR-кодом рядом с bot.py

# Обработка фото
async def ручка_фото(update: Update, context: ContextTypes.DEFAULT_TYPE):
    пользователь = update.message.from_user

    # Сохраняем фото во временный файл
    фото = await update.message.photo[-1].get_file()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tf:
        путь = tf.name
        await фото.download_to_drive(путь)

    # OCR
    изображение = cv2.imread(путь)
    серое = cv2.cvtColor(изображение, cv2.COLOR_BGR2GRAY)
    текст = pytesseract.image_to_string(серое)

    сумма = None
    for слово in текст.split():
        слово = слово.replace(",", ".").replace("с", "5")
        try:
            число = float(слово)
            if 50 < число < 100000:
                сумма = число
                break
        except:
            continue

    сообщение = "✅ Спасибо, отчёт получен!\n\n"

    if сумма:
        процент = round(сумма * 0.3, 2)
        сообщение += f"💰 Найдена сумма: *{сумма}*\n"
        сообщение += f"💸 Переведи 30% → *{процент}*\n\n"
    else:
        сообщение += "❗ Не удалось определить сумму с фото.\n\n"

    сообщение += f"📱 Mbank: `{MBANK_NUMBER}`\n👤 Имя: *{ИМЯ_ВЛАДЕЛЬЦА}*"

    await update.message.reply_text(сообщение, parse_mode="Markdown")

    # Отправляем QR
    if os.path.exists(QR_PATH):
        with open(QR_PATH, "rb") as qr:
            await update.message.reply_photo(photo=InputFile(qr), caption="📸 Сканируй QR-код для оплаты")

# Запуск
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, ручка_фото))
    print("🤖 Бот запущен!")
    app.run_polling()
