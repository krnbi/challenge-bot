from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from flask import Flask
import threading
import os

# 🔑 Токен твоего бота
BOT_TOKEN = "7702678827:AAGLhDvODKSpPP5wA-NGh3iwpe0Ampu5pwE"

# 🌐 Flask-сервер для Render
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

# 🚀 Запускаем Flask в отдельном потоке
threading.Thread(target=run_web).start()

# 🟢 Показываем, что бот жив
print("Бот запущен и слушает команды...")

# 🔁 Обработка команды /checkin
async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"Chat ID is: {chat_id}")  # Вывод в консоль

    keyboard = [
        [
            InlineKeyboardButton("✅ Yes!", callback_data="yes"),
            InlineKeyboardButton("❌ Not this time", callback_data="no")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text="Hey team! It’s check-in time!\n\nDid you do your daily move challenge?",
        reply_markup=reply_markup
    )

# 🔘 Ответ на нажатие кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=f"Response received: {query.data} ✅"
    )

# 🤖 Запуск Telegram-бота
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("checkin", checkin))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
