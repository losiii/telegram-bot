import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

AFF_LINK = "https://affiliate.iqoption.net/redir/?aff=806057&aff_model=revenue&afftrack="

BLOCKED_COUNTRIES = {
    "US", "CA", "GB", "AU",
    "RU", "UA",
    "DE", "FR", "ES", "IT", "NL", "BE", "PL",
    "SE", "NO", "FI", "DK", "AT", "CH"
}

def get_country():
    try:
        r = requests.get("https://ipapi.co/country/")
        return r.text.strip()
    except:
        return "UNKNOWN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Continue", callback_data="continue")]]
    await update.message.reply_text(
        "👋 Welcome\n\n"
        "This is an educational trading assistant.\n\n"
        "⚠️ No financial advice\n"
        "⚠️ No guarantees\n"
        "⚠️ Trading involves risk",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    country = get_country()

    if country in BLOCKED_COUNTRIES:
        await query.edit_message_text(
            "🚫 This service is not available in your region due to regulations."
        )
        return

    keyboard = [
        [InlineKeyboardButton("I understand", callback_data="accept")],
        [InlineKeyboardButton("Exit", callback_data="exit")]
    ]

    await query.edit_message_text(
        "Important notice:\n\n"
        "• Educational content only\n"
        "• No signals\n"
        "• No investment advice\n\n"
        "Do you accept the risks?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    link = AFF_LINK + f"tg_{user_id}"

    keyboard = [[InlineKeyboardButton("Open platform", url=link)]]

    await query.edit_message_text(
        "✅ You may continue.\n\nAll decisions are your responsibility.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Session ended.")

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_continue, pattern="continue"))
    app.add_handler(CallbackQueryHandler(handle_accept, pattern="accept"))
    app.add_handler(CallbackQueryHandler(handle_exit, pattern="exit"))

    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
