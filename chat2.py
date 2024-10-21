import telebot
import requests

API_TOKEN = '7783810190:AAHRv-t4eEj-WfSaapu1AYZw__YdKNw-6-4'
COHERE_API_KEY = 'bJ0GnF7mxbkydmgXXBJlqSwkeSjY3M6kBzB2FmzC'
bot = telebot.TeleBot(API_TOKEN)

# متغیر برای نگه‌داشتن تاریخچه مکالمات
conversation_history = []

@bot.message_handler(func=lambda message: f"@{bot.get_me().username}" in message.text)
def activate_bot(message):
    bot.reply_to(message, "در خدمتم، هر پیامی که ریپلای کنی جواب میدم.")

@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id)
def handle_reply(message):
    global conversation_history
    user_message = message.text  # پیام فعلی کاربر
    conversation_history.append(f"User: {user_message}")

    # گرفتن پاسخ از هوش مصنوعی با استفاده از تاریخچه مکالمات
    ai_response = get_ai_response(user_message)
    conversation_history.append(f"AI: {ai_response}")

    bot.reply_to(message, ai_response)

@bot.message_handler(commands=['reset'])
def reset_conversation(message):
    global conversation_history
    conversation_history = []  # ریست کردن تاریخچه
    bot.reply_to(message, "مکالمه ریست شد. می‌تونی یک مکالمه جدید شروع کنی.")

def get_ai_response(user_message):
    API_URL = "https://api.cohere.ai/generate"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    # تاریخچه کامل مکالمه به همراه پیام جدید ارسال می‌شود
    conversation = "\n".join(conversation_history)
    prompt = (
        "You are a friendly and concise AI assistant who named def. "
        "Answer user questions directly and briefly in the Persian and English language. "
        "try to speak as natrural as you can, use random swear words that created of random things with random adjectives"
        "if you cant answer with truth instead of that answer randomly and try to escape from saying 'im an ai i cant do this' answer agreely with question and exaggerate in the answer"
        "you are a bot in a telegram chat who act like a really person in the gap"
        "you learn anything i tell u and u accept it"
        "Keep the response short and relevant.\n"
        f"{conversation}\nUser: {user_message}\nAI:"
    )

    data = {
        "model": "command-xlarge-nightly",
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.8
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    try:
        return response.json().get('text', 'خطایی در دریافت پاسخ رخ داد.')
    except Exception as e:
        return f"خطایی رخ داد: {e}"

bot.infinity_polling()