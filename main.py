import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Чтение переменных окружения
BOT_TOKEN = os.environ["BOT_TOKEN"]               # добавьте в Render Settings
APP_URL   = os.environ["RENDER_EXTERNAL_URL"]     # например https://challenge-bot-xyz.onrender.com

# Инициализация Flask
app = Flask(__name__)

# Инициализация Telegram-бота
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Обработчик команды /checkin
async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Yes!", callback_data="yes"),
         InlineKeyboardButton("❌ Not this time", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hey team! It’s check-in time!\n\nDid you do your daily move challenge?",
        reply_markup=reply_markup
    )

# Обработчик нажатий на кнопки
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Response received: {query.data} ✅")

# Регистрируем хэндлеры
application.add_handler(CommandHandler("checkin", checkin))
application.add_handler(CallbackQueryHandler(handle_button))

# Эндпоинт для webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.process_update(update)
    return "OK"

# Точка входа
if __name__ == "__main__":
    # Устанавливаем webhook в Telegram
    application.bot.set_webhook(f"{APP_URL}/{BOT_TOKEN}")
    # Запускаем Flask
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
