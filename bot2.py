# import discord
# from discord.ext import commands
# from dotenv import load_dotenv 
# import os 
# import json

# load_dotenv()
# TOKEN = os.getenv("TOKEN2")

# intents = discord.Intents.default()
# intents.message_content = True

# def zaladuj_wyniki():
#     if os.path.exists("wyniki.txt"):
#         try:
#             with open("wyniki.txt", "r") as f:
#                 return json.load(f)
#         except (json.JSONDecodeError,ValueError):
#             return {}
#     return {}
# def zapisz_wyniki():
#     with open("wyniki.txt", "w") as f:
#         json.dump(lista, f, indent = 4)

# lista = zaladuj_wyniki()

# bot = commands.Bot(command_prefix='!', intents=intents)

# <@&1468670397762502902>.event
# async def on_ready():
#     print(f'Zalogowaliśmy się jako {bot.user}')

# <@&1468670397762502902>.command()
# async def hej(ctx):
#     await ctx.send(f'Cześć, jestem bot{bot.user}!')

# <@&1468670397762502902>.event
# async def on_message(message):
#     if message.author.bot:
#         return
#     user_id = str(message.author.id)
#     if user_id in lista:
#         lista[user_id] += 1
#     else:
#         lista[user_id] = 1

#     print(f"używkownik {message.author} ma teraz {lista[user_id]} punktów!")
#     await bot.process_commands(message)

# <@&1468670397762502902>.command()
# async def lvl(ctx):
#     user_id = str(ctx.author.id)
#     await ctx.send(f'Czesc, masz poziom{lista[user_id]}!')

# <@&1468670397762502902>.command()
# async def heh(ctx, count_heh = 5):
#     await ctx.send("he" * count_heh)

# try:
#     bot.run(TOKEN)
# finally:
#     zapisz_wyniki()