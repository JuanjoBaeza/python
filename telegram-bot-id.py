from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8583365467:AAEJu0wKq3RwNqWyJFBXyK4W7EbhEBA3pfM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # `effective_user` funciona siempre, aunque no haya `message`
    user = update.effective_user
    chat = update.effective_chat

    if user and chat:
        text = (
            f"👋 Hola, {user.first_name or 'usuario'}!\n\n"
            f"🆔 Tu ID personal es: `{user.id}`\n"
            f"💬 Chat ID actual: `{chat.id}`"
        )
        await update.effective_message.reply_text(text, parse_mode="Markdown")
    else:
        print("⚠️ No se pudo obtener el usuario o chat.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
