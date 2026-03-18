import discord
import os
import time
import logging
from flask import Flask
from threading import Thread

logging.basicConfig(level=logging.INFO)

# --- Веб-сервер для UptimeRobot ---
app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# --- Настройки бота ---
CHANNEL_ID = 1483887310771847296

GIF_URL = "https://cdn.discordapp.com/attachments/1312367256038019092/1483904073110523974/homelander-appreciate-smile.gif_1.gif?ex=69bc48dc&is=69baf75c&hm=45acb995801854b8278e89b893964b82f4a3cd7c73bd0b16c9f8c9bfefb0d0e6&"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Бот запущен: {client.user}")

@client.event
async def on_member_join(member):
    channel = client.get_channel(CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        embed = discord.Embed(
            title=f"👋 Добро пожаловать на сервер {member.guild.name}!",
            description=(
                f"Привет, {member.mention}! Рады видеть тебя здесь 🎉\n\n"
                f"📌 Обязательно прочитай правила сервера\n"
                f"🎮 Желаем приятного времяпровождения!\n"
                f"💬 Не стесняйся — представься в чате"
            ),
            color=0x5865F2
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=GIF_URL)
        embed.set_footer(text=f"Ты {member.guild.member_count}-й участник сервера!")
        await channel.send(embed=embed)

while True:
    try:
        client.run(os.environ['TOKEN'])
    except Exception as e:
        logging.error(f"Бот упал с ошибкой: {e}")
        logging.info("Перезапуск через 5 секунд...")
        time.sleep(5)
