import discord
from discord.ext import commands
import sys
import asyncio
import os
from flask import Flask
from threading import Thread

# --- إعداد خادم الويب لمنع إغلاق البوت (Keep Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل الآن بنجاح 24/7!"

def run():
    # Render يمرر البورت تلقائياً عبر متغير البيئة PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- الإعدادات النهائية ---
# قراءة التوكن من متغيرات البيئة (أكثر أماناً)
TOKEN = os.environ.get('DISCORD_TOKEN')
TARGET_CHANNEL_ID = 1481769127478820895
GIF_URL = 'https://media.discordapp.net/attachments/967844912991187004/969022806958432287/0E7D4173-7CEB-40AC-AE6F-BC1AA9694D53.gif?ex=69b3fa10&is=69b2a890&hm=079afcf269b6550ab84c8a62c51be2b94334ec61f140b9252794826fc7f454b9&='

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

last_msg_time = 0

@bot.event
async def on_ready():
    print(f'--- البوت يعمل الآن بنظام Keep Alive ---')
    print(f'الاسم: {bot.user.name}')
    print(f'مراقبة القناة: {TARGET_CHANNEL_ID}')
    print(f'-----------------------')
    sys.stdout.flush()

@bot.event
async def on_message(message):
    global last_msg_time
    if message.channel.id == TARGET_CHANNEL_ID and message.author != bot.user:
        current_time = asyncio.get_event_loop().time()
        if current_time - last_msg_time < 2.0:
            return
        last_msg_time = current_time
        try:
            await message.channel.send(GIF_URL)
            print(f'تم الرد على رسالة من {message.author}')
            sys.stdout.flush()
        except Exception as e:
            print(f'خطأ في الإرسال: {e}')
            sys.stdout.flush()
    await bot.process_commands(message)

# تشغيل البوت مع خادم الويب
if __name__ == '__main__':
    if not TOKEN:
        print("خطأ: لم يتم العثور على DISCORD_TOKEN في متغيرات البيئة!")
        sys.exit(1)
        
    keep_alive()  # تشغيل خادم الويب في الخلفية
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"خطأ في التشغيل: {e}")
