import telebot
from yt_dlp import YoutubeDL
import os

BOT_TOKEN = "8901804767:AAH-EIOGV0EQBYxurwdPE8KLLew8GAt9DPw"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي أي رابط فيديو (يوتيوب، تيك توك، إنستغرام...) وسأقوم بتحميله وإرساله لك.")

@bot.message_handler(func=lambda message: True)
def download_and_send_video(message):
    url = message.text

    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح.")
        return

    msg = bot.reply_to(message, "جاري معالجة الرابط وتحميل الفيديو... انتظر قليلاً ⏳")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.%(ext)s',
        'max_filesize': 45 * 1024 * 1024,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل بنجاح بواسطة بوتك! 🎉")

        os.remove('video.mp4')
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"عذراً، حدث خطأ أثناء التحميل: {str(e)}", message.chat.id, msg.message_id)
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

bot.infinity_polling()
