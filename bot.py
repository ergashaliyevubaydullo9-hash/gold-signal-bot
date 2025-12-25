import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8362036716:AAEfOZCLByl14tyCP-WDRN7PFiyUSkAoQE8"
API_KEY = "goldapi-76qpsmjl45rja-io"

ALLOWED_USERS = [6042268389]

prices = []

def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": API_KEY}
    r = requests.get(url)
    return float(r.json()["price"])

def calculate_rsi(price):
    prices.append(price)
    if len(prices) < 14:
        return None

    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains[-14:]) / 14 if gains else 1
    avg_loss = sum(losses[-14:]) / 14 if losses else 1

    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ GOLD SIGNAL BOT ISHLAYAPTI")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Bu bot pullik.")
        return

    price = get_gold_price()
    rsi = calculate_rsi(price)

    if rsi is None:
        await update.message.reply_text("⏳ Ma’lumot yig‘ilmoqda...")
        return

    if rsi < 30:
        s = "📈 BUY"
    elif rsi > 70:
        s = "📉 SELL"
    else:
        s = "⏸ WAIT"

    msg = f"""
💰 GOLD SIGNAL
📊 Price: {price}
📈 RSI: {rsi}
📌 Signal: {s}
"""
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, signal))

app.run_polling()
