import os
import threading

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔑 Подхватываем токен из переменных окружения
BOT_TOKEN = os.environ["BOT_TOKEN"]

# 🌐 Простой веб-сервер для Render — чтобы сервис не засыпал
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

# 🚀 Запускаем Flask-сервер в фоне
threading.Thread(target=run_web).start()

# 🔁 Обработка команды /checkin
async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes!", callback_data="yes"),
            InlineKeyboardButton("❌ No",   callback_data="no")
        ]
    ]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="It’s check-in time! Did you move today?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🔘 Обработка нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"Response: {query.data}")

# 🤖 Точка старта бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()  # автоматически инициализирует, стартует и запускает polling
