import discord
from discord import app_commands
import os
from flask import Flask
from threading import Thread

# --- Веб-сервер ---
app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# --- Настройки ---
CHANNEL_ID = 1483887310771847296
ANNOUNCE_CHANNEL_ID = 1483338410583396474

GIF_URL = "https://cdn.discordapp.com/attachments/1312367256038019092/1483904073110523974/homelander-appreciate-smile.gif_1.gif?ex=69bc48dc&is=69baf75c&hm=45acb995801854b8278e89b893964b82f4a3cd7c73bd0b16c9f8c9bfefb0d0e6&"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# --- Приветствие ---
@client.event
async def on_ready():
    guild = discord.Object(id=1483338409677164627)
    await tree.sync(guild=guild)
    print(f"Бот запущен: {client.user}")

@client.event
async def on_member_join(member):
    channel = client.get_channel(CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        embed = discord.Embed(
            title=f"👋 Добро пожаловать на сервер {member.guild.name}!",
            description=(
                f"Привет, {member.mention}! Рады тебя видеть 🎉\n\n"
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

# --- Команда /announce ---
@tree.command(name="announce", description="Отправить объявление в общий чат", guild=discord.Object(id=1483338409677164627))
@app_commands.describe(текст="Текст объявления", гифка="Ссылка на GIF")
async def announce(interaction: discord.Interaction, текст: str, гифка: str = None):
    channel = client.get_channel(ANNOUNCE_CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        embed = discord.Embed(
            title="📢 Объявление!",
            description=текст,
            color=0xFF5733
        )
        if гифка:
            embed.set_image(url=гифка)
        await channel.send(embed=embed)
        await interaction.response.send_message("✅ Объявление отправлено!", ephemeral=True)

client.run(os.environ['TOKEN'])
