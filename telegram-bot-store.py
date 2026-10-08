from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ⚙️ Configura tus datos
BOT_TOKEN = "8583365467:AAEJu0wKq3RwNqWyJFBXyK4W7EbhEBA3pfM"
ADMIN_CHAT_ID = 2064798090  # ← tu ID personal o el de un grupo

# Productos de ejemplo
products = {
    "camisa": {"precio": 25, "desc": "Camisa 100% algodón", "img": "https://..."},
    "pantalon": {"precio": 40, "desc": "Pantalón de lino", "img": "https://..."}
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👕 Camisa", callback_data="camisa")],
        [InlineKeyboardButton("👖 Pantalón", callback_data="pantalon")]
    ]
    await update.message.reply_text(
        "¡Bienvenido a la tienda! Selecciona un producto:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Botón de producto
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    producto = products[query.data]

    keyboard = [
        [InlineKeyboardButton("🗣 Hablar con vendedor", callback_data=f"contactar_{query.data}")]
    ]
    caption = f"🛍 *{query.data.capitalize()}*\n{producto['desc']}\n💰 Precio: {producto['precio']}€"
    await query.message.reply_photo(
        photo=producto["img"],
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Cuando el usuario pulsa “Hablar con vendedor”
async def contactar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    producto = query.data.split("_", 1)[1]
    user = query.from_user

    # Avisar al usuario
    await query.message.reply_text("✅ He avisado al vendedor. Te contactarán pronto.")

    # Enviar mensaje al vendedor
    mensaje = (
        f"📩 *Nuevo contacto del bot*\n"
        f"👤 {user.first_name} (@{user.username or 'sin usuario'})\n"
        f"🛍 Producto: {producto.capitalize()}\n"
        f"🆔 ID: {user.id}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje, parse_mode="Markdown")

# Si el usuario escribe algo después de iniciar contacto
async def mensaje_cliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reenvía los mensajes del cliente al vendedor."""
    user = update.message.from_user
    text = update.message.text
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📨 Mensaje de {user.first_name} (@{user.username or 'sin usuario'}):\n{text}"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button, pattern="^(camisa|pantalon)$"))
app.add_handler(CallbackQueryHandler(contactar, pattern="^contactar_"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_cliente))

app.run_polling()
