import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN2 = os.getenv('TOKEN2')

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(name='Programuję...', type=discord.ActivityType.watching)
client = discord.Client(activity=activity, intents=intents)

emoji = '👋'

idRoli_menedzera = 1468680846637666385


@client.event
async def on_ready():
    print(f'Zalogowano jako {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if any(role.id == idRoli_menedzera for role in message.author.roles):
            if message.content.lower().startswith('!stop'):
                await message.channel.send(f'**{message.author.display_name}** zatrzymał bota!')
                await client.close()
    print(f'Otrzymano wiadomość od {message.author}: {message.content}')
    if not message.author.bot:  
        if message.content.startswith('!ping'):
            await message.channel.send(f'Pong od {message.author}')
        elif message.content.lower().startswith('cześć'):
            await message.add_reaction(emoji)
            await message.author.send('**Cześć!** 👋')
            await message.channel.send(f'Cześć, **{message.author.display_name}**! Jak mogę Ci pomóc?')
        elif message.content.lower().startswith('hej'):
            await message.add_reaction(emoji)
            await message.author.send('**Hej!** 👋')
            await message.channel.send(f'Hej, **{message.author.display_name}**! Jak mogę Ci pomóc?')

client.run(TOKEN2)