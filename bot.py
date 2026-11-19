import os
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DB = "tts_coin.db"

def setup():
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0,
            referrer INTEGER
        )
    """)
    con.commit()
    con.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    setup()

    con = sqlite3.connect(DB)
    con.execute(
        "INSERT OR IGNORE INTO users (id) VALUES (?)",
        (user_id,)
    )
    con.commit()
    con.close()

    await update.message.reply_text(
        "⭐ Welcome to TTS Coin!\n\n"
        "Use /balance to see your balance.\n"
        "Use /mine to earn points.\n"
        "Use /invite to invite friends.\n"
        
        "Use /withdraw to request a simulated withdrawal."
    )
    
    async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    result = cur.fetchone()
    con.close()

    amount = result[0] if result else 0

    await update.message.reply_text(
        f"💰 Your balance: {amount:.2f} TTS"
    )


async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    con = sqlite3.connect(DB)
    con.execute(
        "UPDATE users SET balance = balance + 1 WHERE id=?",
        (user_id,)
    )
    
    con.commit()
    con.close()

    await update.message.reply_text("⛏️ You earned 1 TTS point!")async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = await context.bot.get_me()
    user_id = update.effective_user.id

    link = f"https://t.me/{bot.username}?start={user_id}"

    await update.message.reply_text(
        "👥 Invite your friends to TTS Coin!\n\n"
        f"Your invitation link:\n{link}"
    )async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await update.message.reply_text(
        "📤 Withdrawal requests are currently simulated.\n"
        "No real money or cryptocurrency is transferred."
    ) 
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing")

    setup()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("mine", mine))
    app.add_handler(CommandHandler("invite", invite))
    app.add_handler(CommandHandler("withdraw", withdraw))

    print("TTS Coin Bot is running!")
    app.run_polling(stop_signals=None)


if __name__ == "__main__":
    main()
