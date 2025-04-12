from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")
OWNER_NAME = os.getenv("OWNER_NAME")
MBANK_NUMBER = os.getenv("MBANK_NUMBER")

QR_PATH = "qr.png"  # заранее положи сюда файл с QR-кодом

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    await update.message.reply_text(
        f"Спасибо, отчёт получен!\n\n"
        f"Переведи 30% от суммы на реквизиты:\n\n"
        f"💳 Mbank: {MBANK_NUMBER}\n👤 Имя: {OWNER_NAME}"
    )

    with open(QR_PATH, "rb") as qr:
        await update.message.reply_photo(photo=InputFile(qr), caption="Сканируй QR-код для оплаты")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    app.add_handler(photo_handler)
    print("Bot started...")
    app.run_polling()
