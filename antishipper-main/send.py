import telebot

# توکن ربات و شناسه گروه را مشخص کنید
TOKEN = '7508625116:AAFQAgbKV0nKz3kGXsfp-g8Hz5101ZudJx0'
GROUP_CHAT_ID = '-1001938643910'

# ایجاد شیء ربات
bot = telebot.TeleBot(TOKEN)

def send_message_to_group(message):
    try:
        # ارسال پیام به گروه
        bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
        print("sent")
    except Exception as e:
        print(f"error {e}")

def main():
    while True:
        # پیام را از ترمینال دریافت کنید
        message = input("type:")
        send_message_to_group(message)

if __name__ == '__main__':
    main()
