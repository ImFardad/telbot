import telebot

# ایجاد یک بات با استفاده از توکن
bot = telebot.TeleBot('7508625116:AAFQAgbKV0nKz3kGXsfp-g8Hz5101ZudJx0')

# ایجاد یک لیست برای ذخیره آی‌دی‌های چت
chat_ids = []

# هندلری که پیام‌های متنی را دریافت می‌کند
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    # اگر آی‌دی چت قبلاً ذخیره نشده باشد، آن را ذخیره می‌کنیم
    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        print(f'New chat added: {chat_id}')
    
    # پاسخ به کاربر
    bot.reply_to(message, "Your chat ID has been saved!")

# کامند برای نمایش همه چت‌ها و آی‌دی‌هایشان
@bot.message_handler(commands=['list_chats'])
def list_chats(message):
    if chat_ids:
        chat_list = "\n".join([str(chat_id) for chat_id in chat_ids])
        bot.reply_to(message, f"List of chat IDs:\n{chat_list}")
    else:
        bot.reply_to(message, "No chat IDs found.")

# شروع polling برای دریافت پیام‌ها
bot.infinity_polling()
