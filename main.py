main.pyimport sqlite3
import random
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ዳታቤዝ ማዋቀር
def init_db():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance REAL)')
    conn.commit()
    conn.close()

def register_user(user_id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0.0))
    conn.commit()
    conn.close()

# ቶከንህን እዚህ አስገባ (አዲሱን ቶከን አምጣ)
TOKEN = '8729088665:AAHKD50l-Z8ePRv-yBeZy2QeCQ6IUyyeE0U' 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    register_user(user_id)
    keyboard = [
        ['Play Ludo 🎲', 'Play Bingo 1234'],
        ['Deposit 💰', 'Withdraw 💰'],
        ['Transfer ↔️', 'My Profile 👤'],
        ['Transactions 📜', 'Balance 💰']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("እንኳን ወደ Plus Game በደህና መጡ! 🎲", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    if text == 'Balance 💰':
        conn = sqlite3.connect('game_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        balance = row[0] if row else 0.0
        conn.close()
        await update.message.reply_text(f'የእርስዎ ሂሳብ፦ {balance} ብር ነው')
    elif text == 'Play Ludo 🎲':
        keyboard = [[InlineKeyboardButton("ከ 2 ሰው ጋር 👥", callback_data='2_players')],
                    [InlineKeyboardButton("ከ 4 ሰው ጋር 👥👥", callback_data='4_players')]]
        await update.message.reply_text("ሉዶን ስንት ሰው መጫወት ይፈልጋሉ?", reply_markup=InlineKeyboardMarkup(keyboard))
    elif text == 'Play Bingo 1234':
        await update.message.reply_text(f'🎰 ቢንጎ ጨዋታ! የእርስዎ ቁጥር፦ {random.randint(1000, 9999)}')
    else:
        await update.message.reply_text(f'እርስዎ የጫኑት፦ {text}')

if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
