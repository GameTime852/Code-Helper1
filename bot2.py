import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN2')
# 1. Konfiguracja Intencji
intents = discord.Intents.default()
intents.message_content = True  # Niezbędne do czytania treści (!komenda)
intents.dm_messages = True      # Niezbędne do otrzymywania zdarzeń z DM

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Zalogowano jako {client.user}')

@client.event
async def on_message(message):
    # Ignoruj wiadomości od samego bota
    if message.author == client.user:
        return

    # SPRAWDZENIE: Czy wiadomość jest w DM?
    # Najprostsza metoda: wiadomości w DM nie mają przypisanego serwera (guild)
    is_dm = message.guild is None
    
    # Alternatywna metoda (bardziej ścisła):
    # is_dm = isinstance(message.channel, discord.DMChannel)

    if is_dm:
        # Logika dla komend w DM
        content = message.content.lower() # Ułatwia porównywanie

        if content == '!pomoc':
            await message.channel.send("Jesteśmy w DM! Oto lista komend...")
        
        elif content.startswith('!status'):
            await message.channel.send("System sprawny.")
            
        else:
            await message.channel.send("Nie rozpoznaję tej komendy w wiadomości prywatnej.")

client.run(TOKEN)