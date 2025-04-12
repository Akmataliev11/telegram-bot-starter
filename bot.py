from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

# Загружаем переменные окружения
TOKEN = os.getenv("TOKEN")
ИМЯ_ВЛАДЕЛЬЦА = os.getenv("OWNER_NAME")
MBANK_NUMBER = os.getenv("MBANK_NUMBER")

QR_PATH = "qr.png"  # Убедись, что файл qr.png лежит рядом с bot.py

# Функция-обработчик фото
async def ручка_фото(update: Update, context: ContextTypes.DEFAULT_TYPE):
    пользователь = update.message.from_user

    # Ответ текстом
    await update.message.reply_text(
        f"✅ Спасибо, отчёт получен!\n\n"
        f"💰 Переведи *30% от суммы* на реквизиты:\n\n"
        f"📱 Mbank: `{MBANK_NUMBER}`\n"
        f"👤 Имя: *{ИМЯ_ВЛАДЕЛЬЦА}*",
        parse_mode="Markdown"
    )

    # Отправка QR-кода
    with open(QR_PATH, "rb") as qr:
        await update.message.reply_photo(photo=InputFile(qr), caption="📸 Сканируй QR-код для оплаты")

# Основной запуск
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработчик сообщений с фото
    app.add_handler(MessageHandler(filters.PHOTO, ручка_фото))

    print("🤖 Бот запущен!")
    app.run_polling()
