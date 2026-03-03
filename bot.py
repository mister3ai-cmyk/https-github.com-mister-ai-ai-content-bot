import telebot
import anthropic
from telebot.types import LabeledPrice
from flask import Flask
import threading

TOKEN = '8428631139:AAGLXn9QbPkLCbT-gu959261Uq4XxrvY9fA'
CLAUDE_API_KEY = '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'

bot = telebot.TeleBot(TOKEN)
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# Flask для Render порта
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает 24/7 ✅"

def run_bot():
    bot.infinity_polling()

# Основной код бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Я AIContent_1bot. Напиши тему — сгенерирую идею для видео с заголовком, хуком, скриптом 60 сек, хэштегами и монетизацией.")

@bot.message_handler(func=lambda message: True)
def generate_content(message):
    text = message.text.strip()

    bot.send_chat_action(message.chat.id, 'typing')

    prompt = (
        f"Сгенерируй идею для YouTube/TikTok на тему: '{text}'. "
        f"Включи: крутой заголовок, хук (первые 5 сек), полный скрипт на 60 сек с описанием визуалов и монтажа, 5-7 хэштегов, идеи монетизации. "
        f"Отвечай на русском языке, стильно и цепляюще."
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1200,
            temperature=0.8,
            system="Ты креативный генератор идей для видео контента.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.content[0].text

        bot.reply_to(message, f"✨ **Твоя идея от Claude:**\n\n{answer}\n\nХочешь полный сценарий + визуалы + план монетизации? Жми ниже на оплату (100 Stars).")

        title = "Премиум сценарий"
        description = f"Полный сценарий + визуалы + монетизация для темы: {text}"
        payload = f"premium_{text[:20].replace(' ', '_')}"
        currency = "XTR"
        prices = [LabeledPrice(label="Полный премиум-пак", amount=100)]

        bot.send_invoice(
            message.chat.id,
            title,
            description,
            payload,
            "",
            currency,
            prices,
            start_parameter="premium-content",
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False
        )

    except Exception as e:
        print(f"Claude error: {e}")
        bot.reply_to(message, f"Ошибка Claude: {str(e)}\nПока простой вариант...")

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.reply_to(message, "✅ Оплата прошла! Вот твой премиум-пак:\n\n"
                          "🚀 Полный сценарий + визуалы + план монетизации\n"
                          "📸 Динамичный монтаж, переходы через маски, неон-эффекты\n"
                          "💰 Продажа чек-листа, партнёрка, бренд-дилы\n\n"
                          "Спасибо! Пиши новую тему.")

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)