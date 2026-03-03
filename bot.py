import telebot
import anthropic
from telebot.types import LabeledPrice
from flask import Flask
import threading

TOKEN = '8428631139:AAGLXn9QbPkLCbT-gu959261Uq4XxrvY9fA'
CLAUDE_API_KEY = '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'

bot = telebot.TeleBot(TOKEN)
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# =============== FLASK ДЛЯ RENDER ===============
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот AIContent_1bot работает 24/7 ✅"

def run_bot():
    bot.infinity_polling()

# =============== ОСНОВНОЙ КОД ===============
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Я AIContent_1bot. Напиши тему — сгенерирую идею для видео!")

@bot.message_handler(func=lambda message: True)
def generate_content(message):
    text = message.text.strip()
    bot.send_chat_action(message.chat.id, 'typing')

    prompt = f"Сгенерируй идею для YouTube/TikTok на тему: '{text}'. Включи: заголовок, хук (5 сек), полный скрипт 60 сек, визуалы, 5-7 хэштегов, идеи монетизации. Отвечай на русском, стильно."

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1200,
            temperature=0.8,
            system="Ты креативный генератор идей для видео контента.",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.content[0].text
        bot.reply_to(message, f"✨ **Твоя идея от Claude:**\n\n{answer}\n\nХочешь полный сценарий + визуалы + план монетизации? Жми ниже на оплату (100 Stars).")

        send_premium_invoice(message.chat.id, text)

    except Exception as e:
        bot.reply_to(message, f"Ошибка Claude: {str(e)}\nПопробуй позже.")

def send_premium_invoice(chat_id, topic):
    title = "Премиум сценарий"
    description = f"Полный сценарий + визуалы + монетизация для темы: {topic}"
    payload = f"premium_{topic[:20].replace(' ', '_')}"
    currency = "XTR"
    prices = [LabeledPrice(label="Полный премиум-пак", amount=100)]

    bot.send_invoice(
        chat_id, title, description, payload, "", currency, prices,
        start_parameter="premium-content", need_name=False, need_phone_number=False,
        need_email=False, need_shipping_address=False, is_flexible=False
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.reply_to(message, "✅ Оплата прошла! Вот твой премиум-пак:\n\n"
                          "🚀 Полный сценарий + визуалы + план монетизации\n"
                          "📸 Динамичный монтаж, переходы, неон-эффекты\n"
                          "💰 Продажа чек-листа, партнёрка, бренд-дилы\n\n"
                          "Спасибо! Пиши новую тему.")

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)