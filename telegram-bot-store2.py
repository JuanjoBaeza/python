from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# 🔧 Configura tu token y tu ID personal
BOT_TOKEN = "8583365467:AAEJu0wKq3RwNqWyJFBXyK4W7EbhEBA3pfM"
ADMIN_CHAT_ID = -1003233632270  # tu ID de canal (distinto al del bot), donde van a llegar las notificaciones del bot

# 🛍️ Catálogo de productos
products = {
    "camisa": {
        "precio": 25,
        "desc": "Camisa 100% algodón",
        "img": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg",
    },
    "pantalon": {
        "precio": 40,
        "desc": "Pantalón de lino elegante",
        "img": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg",
    },
}


# 📦 /start — muestra el catálogo
async def mostrar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👕 Camisa", callback_data="camisa")],
        [InlineKeyboardButton("👖 Pantalón", callback_data="pantalon")],
    ]
    await update.effective_message.reply_text(
        "🛍 *Catálogo de productos*\n\nElige un tipo de artículo:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


# 🧾 Mostrar detalle del producto + botón "Hablar con vendedor" y "Volver"
async def mostrar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    producto = products.get(query.data)
    if not producto:
        await query.message.reply_text("❌ Producto no encontrado.")
        return

    keyboard = [
        [InlineKeyboardButton("🗣 Hablar con vendedor", callback_data=f"contactar_{query.data}")],
        [InlineKeyboardButton("⬅️ Volver al menú", callback_data="volver_menu")],
    ]

    caption = (
        f"🛍 *{query.data.capitalize()}*\n"
        f"{producto['desc']}\n"
        f"💰 Precio: {producto['precio']} €"
    )

    await query.message.reply_photo(
        photo=producto["img"],
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


# 💬 Enviar mensaje al vendedor
async def contactar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    producto = query.data.split("_", 1)[1]
    user = query.from_user

    await query.message.reply_text("✅ He avisado al vendedor. Te contactarán pronto.")

    mensaje = (
        f"📩 *Nuevo contacto del bot*\n"
        f"👤 {user.first_name} (@{user.username or 'sin usuario'})\n"
        f"🛍 Producto: {producto.capitalize()}\n"
        f"🆔 ID: `{user.id}`"
    )

    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje, parse_mode="Markdown")


# 🔙 Volver al menú principal
async def volver_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("👕 Camisa", callback_data="camisa")],
        [InlineKeyboardButton("👖 Pantalón", callback_data="pantalon")],
    ]

    await query.message.reply_text(
        "⬅️ Has vuelto al menú principal.\n\nElige otro producto:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# 🚀 Lanzar el bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", mostrar_menu))
app.add_handler(CallbackQueryHandler(mostrar_producto, pattern="^(camisa|pantalon)$"))
app.add_handler(CallbackQueryHandler(contactar, pattern="^contactar_"))
app.add_handler(CallbackQueryHandler(volver_menu, pattern="^volver_menu$"))

app.run_polling()
