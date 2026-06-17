import telebot
import pyotp
import time
import base64

BOT_TOKEN = "8816143775:AAEU9ljWdNdcwq-NK_-CBmZ8sK9I67xzX7Q"
OKTA_SECRET = "B8F47E45"
ALLOWED_USER_ID = 7363930390

bot = telebot.TeleBot(BOT_TOKEN)

def get_code_message():
    try:
        # Try padding the secret to make it valid base32
        secret = OKTA_SECRET
        # Pad to multiple of 8
        padding = (8 - len(secret) % 8) % 8
        secret_padded = secret + '=' * padding
        totp = pyotp.TOTP(secret_padded)
        code = totp.now()
        remaining = 30 - (int(time.time()) % 30)
        return f"🔐 كود Okta: `{code}`\n⏳ صالح لمدة {remaining} ثانية"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "⛔ مش مسموح لك.")
        return
    bot.reply_to(message, get_code_message(), parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "⛔ مش مسموح لك.")
        return
    bot.reply_to(message, get_code_message(), parse_mode='Markdown')

print("✅ البوت شغال...")
bot.infinity_polling()
