import discord
from discord.ext import commands
import sys
import asyncio

# --- الإعدادات النهائية (تأكد من وضع التوكن الجديد هنا) ---
TOKEN = 'MTQ4MTgzMjI3MjI1MTQ1NzUzNw.Gk7yyM.a6pjzJIkKji7Ar0e6aTUVFk4UveG98M1HxnnjU'
TARGET_CHANNEL_ID = 1481769127478820895
GIF_URL = 'https://media.discordapp.net/attachments/967844912991187004/969022806958432287/0E7D4173-7CEB-40AC-AE6F-BC1AA9694D53.gif?ex=69b3fa10&is=69b2a890&hm=079afcf269b6550ab84c8a62c51be2b94334ec61f140b9252794826fc7f454b9&='

# إعداد الصلاحيات (Intents)
intents = discord.Intents.default()
intents.message_content = True  # ضروري جداً لرؤية الرسائل
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# متغير لمنع التكرار (Cooldown) لضمان عدم الإرسال المتكرر
last_msg_time = 0

@bot.event
async def on_ready():
    print(f'--- البوت يعمل الآن بنجاح ---')
    print(f'الاسم: {bot.user.name}')
    print(f'مراقبة القناة: {TARGET_CHANNEL_ID}')
    print(f'-----------------------')
    sys.stdout.flush()

@bot.event
async def on_message(message):
    global last_msg_time
    
    # التأكد أن الرسالة في القناة الصحيحة وليست من البوت نفسه
    if message.channel.id == TARGET_CHANNEL_ID and message.author != bot.user:
        
        # نظام حماية (Cooldown): يمنع الإرسال أكثر من مرة كل ثانيتين
        current_time = asyncio.get_event_loop().time()
        if current_time - last_msg_time < 2.0:
            return
            
        last_msg_time = current_time

        try:
            # إرسال صورة الـ GIF
            await message.channel.send(GIF_URL)
            print(f'تم الرد على رسالة من {message.author}')
            sys.stdout.flush()
        except Exception as e:
            print(f'خطأ في الإرسال: {e}')
            sys.stdout.flush()

    # معالجة الأوامر الأخرى إن وجدت
    await bot.process_commands(message)

# تشغيل البوت
if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"خطأ في التشغيل: {e}")
