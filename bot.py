import discord
import asyncio
import random
import math
import time
import re
from discord.ext import commands

bot = commands.Bot(command_prefix='>', self_bot=True)

pokemon_db = set()


class Pokemon:
    def __init__(self, order, level, name, iv):
        self.order = order
        self.level = level
        self.name = name
        self.iv = iv

    def __repr__(self):
        return f'{self.order} {self.level} {self.name} {self.iv}'

    def __str__(self):
        return f'{self.order} {self.level} {self.name} {self.iv}'

    def __eq__(self, other):
        return self.order == other.order and self.level == other.level and self.name == other.name and self.iv == other.iv

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.order, self.level, self.name, self.iv))


def get_pokemon_name(message):
    with open('pokemon.txt', 'r') as f:
        pokemon = f.read().split('|')
        viable = []
        message = message.content.replace('\\_', '@')
        message = message[:-1]
        for p in pokemon:
            if len(p) == len(message[15:]):
                for i in range(len(p)):
                    if p[i] != message[15:][i] and message[15:][i] != '@':
                        break
                else:
                    viable.append(p)

        return viable


def get_random_characters():
    import string
    return ''.join(random.choice(string.ascii_letters) for i in range(25))


@bot.event
async def on_message(message):
    if message.author.id == 716390085896962058 and message.embeds and message.embeds[0].title.endswith('appeared!'):
        await asyncio.sleep(0.75 + math.sin(time.time()) * 0.5)
        await message.channel.send('<@716390085896962058> h')

    if message.author.id == 716390085896962058 and message.content.startswith('The pokémon is '):
        await asyncio.sleep(0.9 + math.sin(time.time()) * 0.5)
        pokemon_list = get_pokemon_name(message)
        # try each name await message.channel.send(f'<@716390085896962058> c {pokemon_name}')
        for pokemon_name in pokemon_list:
            await message.channel.send(f'<@716390085896962058> c {pokemon_name}')
            await asyncio.sleep(0.9 + math.sin(time.time()) * 0.5)


@bot.event
async def on_ready():
    # ping him and ask for p
    await bot.get_channel(CHANNEL_ID_GOES_HERE).send('<@716390085896962058> p')
    await asyncio.sleep(0.9 + math.sin(time.time()) * 0.5)
    # get all pokemon
    found_Max = False
    page = 1
    while not found_Max:
        await asyncio.sleep(2 + math.sin(time.time()) * 0.5)
        # in the embed msg 716390085896962058 sent, get the description
        desc = bot.get_channel(
            CHANNEL_ID_GOES_HERE).last_message.embeds[0].description
        # split by line breaks
        desc = desc.split('\n')
        found = 0
        # add this page to database
        for pokemon_line in desc:
            found += 1
            pokemon_order = re.search(r'(\d+)`', pokemon_line).group(1)
            pokemon_level = re.search(r'Lvl\. (\d+)', pokemon_line).group(1)
            pokemon_name = re.search(r'<:_:\d+> (\w+)', pokemon_line).group(1)
            pokemon_iv = re.search(r'(\d+\.\d+)%', pokemon_line).group(1)

            pokemon_db.add(Pokemon(pokemon_order, pokemon_level,
                                   pokemon_name, pokemon_iv))

        if found < 20:
            found_Max = True

        # if not last page, go to next page
        if not found_Max:
            await asyncio.sleep(4 + math.sin(time.time()) * 0.5)
            page += 1
            await bot.get_channel(CHANNEL_ID_GOES_HERE).send(f'<@716390085896962058> p {page}')

    # send trade to me
    await asyncio.sleep(2 + math.sin(time.time()) * 0.5)
    await bot.get_channel(CHANNEL_ID_GOES_HERE).send(f'<@716390085896962058> t <@BOT_OWNER_ID_GOES_HERE>')
    await asyncio.sleep(10 + math.sin(time.time()) * 0.5)
    # add all pokemon to database
    for pokemon in pokemon_db:
        await asyncio.sleep(2 + math.sin(time.time()) * 0.5)
        await bot.get_channel(CHANNEL_ID_GOES_HERE).send(f'<@716390085896962058> t a {pokemon.order}')
        await asyncio.sleep(2 + math.sin(time.time()) * 0.5)
    # confirm trade
    await asyncio.sleep(2 + math.sin(time.time()) * 0.5)
    await bot.get_channel(CHANNEL_ID_GOES_HERE).send(f'<@716390085896962058> t c')
    await asyncio.sleep(2 + math.sin(time.time()) * 0.5)

    await bot.get_channel(CHANNEL_ID_GOES_HERE).send('<@716390085896962058> bal')
    await asyncio.sleep(0.9 + math.sin(time.time()) * 0.5)
    await bot.get_channel(CHANNEL_ID_GOES_HERE).send('<@716390085896962058> p')
    await asyncio.sleep(0.9 + math.sin(time.time()) * 0.5)
    X = 0
    while True:
        await asyncio.sleep(2.55 + math.sin(time.time()) * 0.5)
        await bot.get_channel(CHANNEL_ID_GOES_HERE).send(get_random_characters())
        X += 1

        if X % 100 == 0:
            await bot.get_channel(CHANNEL_ID_GOES_HERE).send('<@716390085896962058> bal')
            await asyncio.sleep(0.9 + math.sin(time.time()) * 0.5)
            await bot.get_channel(CHANNEL_ID_GOES_HERE).send('<@716390085896962058> p')
            X = 0

bot.run('TOKEN_GOES_HERE')
