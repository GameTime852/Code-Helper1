import asyncio
import discord
import os
from dotenv import load_dotenv
import random
from discord.ext import commands
import json
import math
from easy_pil import Editor, load_image, Font, Canvas
import io

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

activity = discord.Activity(name='Programuję...', type=discord.ActivityType.playing)
bot = commands.Bot(command_prefix='/', intents=intents)

emoji = '👋'

idRoli_menedzera = [1468680846637666385]
admin_ids = [
    1267468021073449042,
    1460331130837270592  
]

def is_owner(ctx):
    # Wpisz tutaj swoje ID użytkownika Discord (jako liczbę)
    YOUR_ID = admin_ids
    return ctx.author.id == YOUR_ID

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

    try:
        # Synchronizacja globalna (może zająć trochę czasu, zanim komendy pojawią się w Discordzie)
        synced = await bot.tree.sync()
        print(f'Zsynchronizowano {len(synced)} komend(y) typu slash.')
    except Exception as e:
        print(f'Wystąpił błąd podczas synchronizacji: {e}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    is_dm = message.guild is None
    
    user_id = str(message.author.id)
    if user_id in lista:
        lista[user_id] = lista[user_id] + 1
    else:
        lista[user_id] = 1

    print(f"używkownik {message.author} ma teraz {lista[user_id]} punktów!")
    await bot.process_commands(message)
    
    # Alternatywna metoda (bardziej ścisła):
    # is_dm = isinstance(message.channel, discord.DMChannel)

    if is_dm:
        # Logika dla komend w DM
        await bot.change_presence(activity=discord.Activity(name="Ogląda DM-y", type=discord.ActivityType.watching))

        if message.author.id not in admin_ids and not any(role.id in idRoli_menedzera for role in message.author.roles):
            # Opcja A: Odpisz, że brak dostępu
            await message.channel.send("⛔ Nie masz uprawnień do korzystania z tego bota na DM, spróbuj na serwerze https://discord.gg/F8aaHAhQ.")
            print(f"Nieautoryzowana próba użycia przez: {message.author} ({message.author.id})")
            return
        
        if message.content.lower().startswith('!stop'):
            await message.channel.send("Zamykam bota...")
            await bot.close()
    
    elif any(role.id == idRoli_menedzera for role in message.author.roles):
            await bot.change_presence(activity=discord.Activity(name="Ogląda wiadomości na serwerze", type=discord.ActivityType.watching))
            if message.content.lower().startswith('!stop'):
                await message.channel.send(f'**{message.author.display_name}** zatrzymał bota!')
                await bot.close()
    #print(f'Otrzymano wiadomość od {message.author}: {message.content}')
    if not is_dm:
         await bot.change_presence(activity=discord.Activity(name="Ogląda wiadomości na serwerze", type=discord.ActivityType.watching))
    if not message.author.bot:  
        if message.content.lower().startswith('cześć'):
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
    await bot.change_presence(status=discord.Status.idle)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    await channel.send(f'Witaj, **{member.name}**!')
    await channel.send(f'Miło nam, że tu jesteś!')


def zaladuj_wyniki():
    if os.path.exists("wyniki.txt"):
        try:
            with open("wyniki.txt", "r") as f:
                return json.load(f)
        except (json.JSONDecodeError,ValueError):
            return {}
    return {}
def zapisz_wyniki():
    with open("wyniki.txt", "w") as f:
        json.dump(lista, f, indent = 4)

lista = zaladuj_wyniki()


@bot.tree.command(name="lvl", description="Sprawdź swój poziom!")
async def lvl(interaction: discord.Interaction, user: str = None):
    if user is None:
        user_id = str(interaction.user.id)
        name_usera = interaction.user.display_name
    else:
        name_usera = user

    xp_usera = lista[user_id]

    awatar_img = load_image(interaction.user.display_avatar.url)
    awatar = Editor(awatar_img).resize((250, 250)).circle_image()
    tlo = Editor("images/image.png")
    tlo.paste(awatar, (125, 125))

    profil_czcionki_1 = Font.poppins(size=100, variant="bold")
    profil_czcionki_2 = Font.poppins(size=50, variant="light")

    tlo.text((350, 450), str(name_usera), font = profil_czcionki_1, color="black")
    tlo.text((700, 300), f"Poziom: {math.floor(xp_usera / 10)}", font = profil_czcionki_2, color="black")

    plik = discord.File(fp = tlo.image_bytes, filename = "poziom.png")
    await interaction.response.send_message(file=plik)


    lvl = lista[user_id] / 10
    lvl10 = math.floor(lvl) 
    await interaction.response.send_message(f'Cześć, **{name_usera}**! Masz poziom **{lvl10}**!')

@bot.tree.command(name="heh", description="Wysyła 'he' określoną liczbę razy.")
async def heh(interaction: discord.Interaction, count_heh: int = 5):
    await interaction.response.send_message("he" * count_heh)

@bot.tree.command(name="clear", description="Usuwa określoną liczbę wiadomości (domyślnie 10000).")
async def clear(interaction: discord.Interaction, limit: int = 10000):
    """Usuwa określoną liczbę wiadomości."""
    
    # Usuwamy wiadomość z komendą (!clear) + podaną liczbę wiadomości
    await interaction.response.defer()
    await interaction.channel.purge(limit=limit + 1)
    
    # Opcjonalnie: potwierdzenie usunięcia
    if limit == 10000:
        msg = await interaction.channel.send(f'Usunięto wszystkie wiadomości. ✅')
    else:
        msg = await interaction.channel.send(f'Usunięto {limit} wiadomości. ✅')
    
    await msg.delete(delay=3) # Usuwa potwierdzenie po 3 sekundach
@bot.tree.command(name="cls_logs", description="Czyści konsolę.")
@commands.is_owner()
async def cls_logs(interaction: discord.Interaction):
    os.system('cls' if os.name == 'nt' else 'clear')
    await interaction.response.send_message('Konsola wyczyszczona! ✅')
@bot.tree.command(name="spam", description="Wysyła spam określoną liczbę razy.")
async def spam(interaction: discord.Interaction, count: int = 10):
    await interaction.response.defer()
    for i in range(count):
        await interaction.channel.send(f'Spam {i+1}/{count}')

@bot.tree.command(name="stop", description="Zatrzymuje bota.")
@commands.is_owner()
async def stop(interaction: discord.Interaction, cooldown: int = 0):
    await interaction.response.send_message(f'Zamykam bota za {cooldown} sekund...')
    await asyncio.sleep(cooldown)
    await interaction.channel.send(f'**{interaction.user.display_name}** zatrzymał bota!')
    print(f'**{interaction.user.display_name}** zatrzymał bota!')
    await bot.close()
@bot.tree.command(name="dm", description="Wysyła wiadomość do użytkownika.")
async def dm(interaction: discord.Interaction, user: discord.User, *, message: str):
    try:
        await user.send(message)
        await interaction.response.send_message(f'Wiadomość wysłana do {user.display_name}! ✅')
    except Exception as e:
        await interaction.response.send_message(f'Nie można wysłać wiadomości do {user.display_name}. ❌\nBłąd: {e}')
@bot.tree.command(name="kick", description="Wyrzuca użytkownika z serwera.")
@commands.is_owner()
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str = "Brak podanego powodu"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f'**{member.display_name}** został wyrzucony! ✅\nPowód: {reason}')
    except Exception as e:
        await interaction.response.send_message(f'Nie można wyrzucić **{member.display_name}**. ❌\nBłąd: {e}')

try:
    bot.run(TOKEN)
finally:
    zapisz_wyniki()