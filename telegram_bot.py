import os
from datetime import date

from dotenv import load_dotenv
from supabase import create_client
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


# Load environment variables
load_dotenv()

# Supabase connection
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(url, key)

# Telegram bot token
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Authorized Telegram users
ALLOWED_USER_IDS = {
    1317894846,   # Your Telegram ID
    5270973018,   # Mom's Telegram ID
}




async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Check whether the user is authorized
    user = update.effective_user

    if user is None or user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text(
            "❌ You are not authorized to use this bot."
        )
        return

    message = update.message.text.strip()

    # Split message
    parts = message.split()

    message = update.message.text.strip()

    # Split the message
    parts = message.split()

    # Check message format
    if len(parts) < 2:
        await update.message.reply_text(
            "❌ Please use this format:\n\n"
            "Renu 5000\n\n"
            "Or:\n"
            "Renu 5000 cement"
        )
        return

    # Worker name
    worker_name = parts[0]

    # Payment amount
    try:
        amount = float(parts[1])
    except ValueError:
        await update.message.reply_text(
            "❌ Amount must be a number.\n\n"
            "Example:\n"
            "Renu 5000"
        )
        return

    # Description
    description = " ".join(parts[2:])

    # Today's date
    payment_date = date.today().isoformat()

    # Payment data
    data = {
        "worker_name": worker_name,
        "amount": amount,
        "payments_date": payment_date,
        "description": description
    }

    # Save to Supabase
    supabase.table("payments").insert(data).execute()

    # Send confirmation
    await update.message.reply_text(
        f"✅ Payment saved!\n\n"
        f"Worker: {worker_name}\n"
        f"Amount: ₹{amount:,.2f}\n"
        f"Date: {payment_date}\n"
        f"Description: {description or '-'}"
    )


# Create Telegram application
application = Application.builder().token(telegram_token).build()

# Listen for messages
application.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

print("🤖 Telegram bot is running...")

# Start the bot
application.run_polling()