import asyncio
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

activity = discord.Activity(name='Programuję...', type=discord.ActivityType.playing)
client = discord.Client(activity=activity, intents=intents)

emoji = '👋'

idRoli_menedzera = 1468680846637666385
admin_ids = [
    1267468021073449042,  # Tu wklej swoje ID (usuń 1 po testach :)
    1460331130837270592   # Ewentualnie ID drugiego admina
]



@client.event
async def on_ready():
    print(f'Zalogowano jako {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    is_dm = message.guild is None
    
    # Alternatywna metoda (bardziej ścisła):
    # is_dm = isinstance(message.channel, discord.DMChannel)

    if is_dm:
        # Logika dla komend w DM
        
        if message.author.id not in admin_ids:
            # Opcja A: Odpisz, że brak dostępu
            await message.channel.send("⛔ Nie masz uprawnień do korzystania z tego bota na DM, spróbuj na serwerze https://discord.gg/F8aaHAhQ.")
            print(f"Nieautoryzowana próba użycia przez: {message.author} ({message.author.id})")
            return
        
        content = message.content.strip()
        args = content.split()
        command = args[0].lower()
        
        if not command == '!status':
            await client.change_presence(status=discord.Status.online)
        if not command == '!activity':
            await client.change_presence(activity=discord.Activity(name="Ogląda DM-y", type=discord.ActivityType.watching))

        if command == '!status':
            if len(args) > 1:
                if args[1] == 'online':
                    await message.channel.send("Ustawiam status na online...")
                    await client.change_presence(status=discord.Status.online)
                elif args[1] == 'idle':
                    await message.channel.send("Ustawiam status na idle...")    
                    await client.change_presence(status=discord.Status.idle)
                elif args[1] == 'dnd':
                    await message.channel.send("Ustawiam status na dnd...")
                    await client.change_presence(status=discord.Status.dnd)
                elif args[1] == 'invisible':
                    await message.channel.send("Ustawiam status na invisible...")
                    await client.change_presence(status=discord.Status.invisible)
                else:
                    await message.channel.send("Nieznany status. Dostępne: online, idle, dnd, invisible.")
        if command == '!activity':
            if len(args) > 2:
                if args[1] == 'watching':
                    new_activity = ' '.join(args[2:])
                    await message.channel.send(f"Ustawiam aktywność na {new_activity}...")
                    await client.change_presence(activity=discord.Activity(name=new_activity, type=discord.ActivityType.watching))
                elif args[1] == 'listening':
                    new_activity = ' '.join(args[2:])
                    await message.channel.send(f"Ustawiam aktywność na {new_activity}...")
                    await client.change_presence(activity=discord.Activity(name=new_activity, type=discord.ActivityType.listening))
                elif args[1] == 'clear':
                    await client.change_presence(activity=None)
                elif args[1] == 'playing':
                    new_activity = ' '.join(args[2:])
                    await message.channel.send(f"Ustawiam aktywność na {new_activity}...")
                    await client.change_presence(activity=discord.Activity(name=new_activity, type=discord.ActivityType.playing))
                elif args[1] == 'competing':
                    new_activity = ' '.join(args[2:])
                    await message.channel.send(f"Ustawiam aktywność na {new_activity}...")
                    await client.change_presence(activity=discord.Activity(name=new_activity, type=discord.ActivityType.competing))
                else:
                    await message.channel.send("Nieznany typ aktywności. Dostępne: watching, listening, clear, playing, competing.")
        elif content.startswith('!stop'):
            await message.channel.send("Zamykam bota...")
            await client.close()

    
    elif any(role.id == idRoli_menedzera for role in message.author.roles):
            await client.change_presence(activity=discord.Activity(name="Ogląda Wiadomości na serwerze", type=discord.ActivityType.watching))
            if message.content.lower().startswith('!stop'):
                await message.channel.send(f'**{message.author.display_name}** zatrzymał bota!')
                await client.close()
    print(f'Otrzymano wiadomość od {message.author}: {message.content}')
    if not message.author.bot:  
        await client.change_presence(activity=discord.Activity(name="Ogląda Wiadomości na serwerze", type=discord.ActivityType.watching))
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
    # SPRAWDZENIE: Czy wiadomość jest w DM?
    # Najprostsza metoda: wiadomości w DM nie mają przypisanego serwera (guild)

    await asyncio.sleep(60)
    await client.change_presence(status=discord.Status.idle)

@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    await channel.send(f'Witaj, **{member.name}**!')
    await channel.send(f'Miło nam, że tu jesteś!')

# SPRAWDZENIE: Czy wiadomość jest w DM?
    # Najprostsza metoda: wiadomości w DM nie mają przypisanego serwera (guild)


client.run(TOKEN)