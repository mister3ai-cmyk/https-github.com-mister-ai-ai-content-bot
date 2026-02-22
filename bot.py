import telebot
import requests

TOKEN = '8428631139:AAGLXn9QbPkLCbT-gu959261Uq4XxrvY9fA'  # твой токен

GROK_API_KEY = ''  # ← если есть ключ от x.ai — вставь сюда

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я AIContent_1bot. Напиши тему — сгенерирую идею для видео: заголовок, хук, скрипт 60 сек, хэштеги, монетизация.")

@bot.message_handler(func=lambda message: True)
def generate_content(message):
    text = message.text.strip()
    
    if GROK_API_KEY:
        headers = {
            'Authorization': f'Bearer {GROK_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'grok-beta',
            'messages': [{
                'role': 'user',
                'content': f"Сгенерируй идею для YouTube/TikTok на тему: '{text}'. Обязательно включи: крутой заголовок, хук (первые 5 сек), полный скрипт на 60 сек, 5-7 хэштегов, идеи монетизации."
            }]
        }
        try:
            resp = requests.post('https://api.x.ai/v1/chat/completions', headers=headers, json=data)
            resp.raise_for_status()
            answer = resp.json()['choices'][0]['message']['content']
            bot.reply_to(message, answer)
        except Exception as e:
            bot.reply_to(message, f"Ошибка Grok API: {str(e)}\nПока простой вариант.")
            bot.reply_to(message, f"Тема: {text}\nЗаголовок: Как {text} изменит всё\nХук: 'Представь, что...'\nХэштеги: #AI #Viral #Future")
    else:
        bot.reply_to(message, f"Тема: {text}\n\nЗаголовок: Как {text} изменит твою жизнь\nХук: 'Представь, что...'\nСкрипт: (напиши, что хочешь — я подскажу)\nХэштеги: #AI #Content #Viral #Shorts")

bot.polling()