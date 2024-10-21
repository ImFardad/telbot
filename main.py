import telebot
import requests

API_TOKEN = '7524340018:AAE2eWI3I0ObDAvRpH5fN-mrgJqwg389FyY'
COHERE_API_KEY = 'ZnsUQXOdE7mxoxD1gggKeXt6Hd1FrC6RcDiUVCAk'
LEARNED_FILE = 'learned_data.txt'  # فایل برای ذخیره اطلاعات یادگرفته شده

bot = telebot.TeleBot(API_TOKEN)

# متغیر برای نگه‌داشتن تاریخچه مکالمات
conversation_history = []

# پرامپت اولیه
initial_prompt = (
    "You are a kind, cute and concise AI bot , your name is neo. "
    "Try to speak naturally. "
    "If you can't answer with the truth, answer randomly and try to avoid saying 'I'm an AI, I can't do this',if you cant answer tell them what they want. "
    "act like you are useless but do everything they want from you. "
    "Answer user questions directly and briefly in Persian and English"
    "Keep the response short and relevant."
)

# خواندن اطلاعات یادگرفته شده از فایل
def load_learned_data():
    try:
        with open(LEARNED_FILE, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

learned_data = load_learned_data()

# دستور برای فعال کردن هوش مصنوعی در پاسخ به پیام‌ها
@bot.message_handler(func=lambda message: f"@{bot.get_me().username}" in message.text)
def activate_bot(message):
    bot.reply_to(message, "سلام، چطور میتونم کمک کنم ؟")

# هندلر برای پاسخ به پیام‌های ریپلای شده
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id)
def handle_reply(message):
    global conversation_history
    user_message = message.text  # پیام فعلی کاربر
    user_name = message.from_user.username or message.from_user.first_name  # نام یا نام کاربری فرستنده
    conversation_history.append(f"{user_name}: {user_message}")

    # گرفتن پاسخ از هوش مصنوعی با استفاده از تاریخچه مکالمات
    ai_response = get_ai_response(user_message, user_name)
    conversation_history.append(f"AI: {ai_response}")

    bot.reply_to(message, ai_response)

# دستور ریست کردن مکالمه
@bot.message_handler(commands=['reset'])
def reset_conversation(message):
    global conversation_history
    conversation_history = [initial_prompt]  # ریست کردن تاریخچه و اضافه کردن پرامپت اولیه
    bot.reply_to(message, "مکالمه ریست شد. دوباره شروع شد.")

# دستور یادگیری اطلاعات جدید
@bot.message_handler(commands=['learn'])
def learn_new_info(message):
    global learned_data
    learned_text = message.text.replace('/learn', '').strip()

    if learned_text:
        # ذخیره اطلاعات جدید در فایل به صورت بی‌طرف
        with open(LEARNED_FILE, 'a') as file:
            file.write(f"{learned_text}\n")
        
        learned_data += f"\n{learned_text}"  # به‌روز کردن اطلاعات یادگرفته شده
        bot.reply_to(message, "یاد گرفتم! این اطلاعات را به‌صورت دائمی به خاطر می‌سپارم.")

# گرفتن پاسخ از هوش مصنوعی
def get_ai_response(user_message, user_name):
    API_URL = "https://api.cohere.ai/generate"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    # ترکیب تاریخچه مکالمه، اطلاعات یادگرفته شده، و پیام جدید
    conversation = "\n".join(conversation_history)
    
    # توضیح به هوش مصنوعی که این اطلاعات خیلی مهم هستند
    important_info_explanation = (
        "There is a set of very important information that you've learned previously. "
        "These are critical and should always be remembered and used in future conversations. "
        "Here are those learned pieces of information:\n"
    )

    prompt = (
        f"{important_info_explanation}{learned_data}\n"
        f"User {user_name} just said: {user_message}\n"
        f"Now you must reply to {user_name} based on your knowledge. Here is the conversation:\n"
        f"{conversation}\nAI:"
    )

    data = {
        "model": "command-xlarge-nightly",
        "prompt": prompt,
        "max_tokens": 400,
        "temperature": 0.3
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    try:
        return response.json().get('text', 'خطایی در دریافت پاسخ رخ داد.')
    except Exception as e:
        return f"خطایی رخ داد: {e}"

# شروع polling برای دریافت پیام‌ها
bot.infinity_polling()
