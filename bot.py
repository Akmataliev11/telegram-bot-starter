import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
OWNER_NAME = os.getenv("OWNER_NAME")
MBANK_NUMBER = os.getenv("MBANK_NUMBER")
QR_PATH = "qr.png"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "✅ Спасибо, отчёт получен!\n\n"
        "Переведи 30% от суммы на реквизиты:\n\n"
        f"📱 Mbank: `{MBANK_NUMBER}`\n"
        f"👤 Имя: *{OWNER_NAME}*"
    )

    await update.message.reply_text(message, parse_mode="Markdown")

    if os.path.exists(QR_PATH):
        with open(QR_PATH, "rb") as qr:
            await update.message.reply_photo(photo=InputFile(qr), caption="📸 QR-код для оплаты")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🤖 Бот запущен!")
    app.run_polling()
