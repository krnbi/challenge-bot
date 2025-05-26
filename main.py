from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from keep_alive import keep_alive  # для 24/7

# 🔑 Токен твоего бота
BOT_TOKEN = "7702678827:AAGLhDvODKSpPP5wA-NGh3iwpe0Ampu5pwE"

# 🚀 Запускаем веб-сервер для UptimeRobot
keep_alive()

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

# 🧠 Запуск бота
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("checkin", checkin))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
