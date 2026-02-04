import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

print("Bot is starting...")

@client.event
async def on_ready():
    print(f'Zalogowano jako {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f'Otrzymano wiadomość od {message.author}: {message.content}')
    if message.content.startswith('!ping'):
        await message.channel.send(f'Pong od {message.author}')
    if message.content.startswith('Cześć'):
        await message.channel.send(f'Cześć, {message.author.display_name}! Jak mogę Ci pomóc?')

client.run(TOKEN)