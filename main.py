import telebot
import time
# توکن بات تلگرام
TOKEN = '7508625116:AAFQAgbKV0nKz3kGXsfp-g8Hz5101ZudJx0'
bot = telebot.TeleBot(TOKEN)

# زمان و تعداد "شیپ" ها
last_ship_time = None
ship_count = 0


# تابعی برای پاسخ به پیام‌ها
@bot.message_handler(func=lambda message: 'شیپ' in message.text.lower())
def respond_to_ship(message):
    global last_ship_time, ship_count

    current_time = time.time()

    # اگر اولین بار است یا بیشتر از 15 ثانیه از آخرین "شیپ" گذشته باشد
    if last_ship_time is None or current_time - last_ship_time > 15:
        ship_count = 1
        bot.reply_to(message, 'هیس')
    # اگر در کمتر از 15 ثانیه "شیپ" دوم گفته شود
    elif ship_count == 1:
        ship_count = 2
        bot.reply_to(message, 'باز گفت. آدم باش!')
    # اگر باز هم در کمتر از 15 ثانیه "شیپ" سوم گفته شود
    elif ship_count == 2:
        bot.reply_to(message, 'نگو داری حالمو بد میکنی')
        ship_count = 3
    elif ship_count == 3:
        bot.reply_to(message, 'حالم بهم خورد عوضی')
        ship_count = 4
    elif ship_count == 4:
        bot.reply_to(message, 'چقد حال بهم زن شدی!!!')
        ship_count = 1

    # به‌روزرسانی زمان آخرین "شیپ"
    last_ship_time = current_time


# اجرای بات
print("Bot is listening...")
bot.polling()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)