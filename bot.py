import sys
sys.path.append('parsers')
import discord
from discord.ext import commands, tasks
import config
import asyncio
import emoji_parser
from discord.utils import get
#ssimport cats_parser

vk_prom_message = 'Напоминаем что у нас есть группа в VK https://vk.com/pw_tma'

WORKING_MODE = ["developer", [None]] # None can be replaced with different channels on the discord server

daily_poll_message = ""

isDailyOn = None


with open('README.md') as file:
    readme_file = file.read()[0:541]

emojis = list(emoji_parser.emoji_dict.values())
client = discord.Client()
bot = commands.Bot(command_prefix = "/")

@client.event
async def on_message(message):
    if message.author == client.user:
        return None


@bot.command()
async def messageCount(ctx):
    if ctx.message.content == '/messageCount' :
        message_toOutput = 'Example: /messageCount some random words\n Counted\
            characters: 17'
    else:
        counted_chars = len(ctx.message.content[14:])
        message_toOutput = f'Counted characters: {counted_chars}' #get everything after inputing command
    emb = discord.Embed(colour = discord.Color.blurple())
    emb.add_field(name = ctx.author.name, value = message_toOutput)
    await ctx.send(embed = emb)


@bot.command()
async def readme(ctx):
    emb = discord.Embed(colour = discord.Color.blurple())
    emb.add_field(name = ctx.author.name, value = readme_file)
    await ctx.send(embed = emb)


@bot.command()
async def poll(ctx, question = None):
    full_message = ctx.message.content
    try:
        if question == None:
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field(name = ctx.author.name, value = "Вопрос был указан некорректно.\nПример: `Вопрос ? Аргумент1! Аргумент2! Арг...!`.\nПервые 2 аргумента должны быть обязательно указаны")
            await ctx.send(embed = emb)
            return False
        else:
            full_message = full_message.split("!")[0].split('?') + full_message.split("!")[1:-1]
            full_message[0] = full_message[0][5:] +'?'
            if len(full_message) == 2 :
                emb = discord.Embed(colour = discord.Color.red())
                emb.add_field(name = ctx.author.name, value ='Аргументы были указаны некорректно.\nПример: `(Вопрос ? Аргумент1!, Аргумент2!)`')
                await ctx.send(embed = emb)
            else:
                full_message = ctx.message.content
                full_message = full_message.split("!")[0].split('?') + full_message.split("!")[1:-1]
                full_message[0] = full_message[0][full_message[0].index(' '):] +'?'
                if len(full_message) >21:
                    emb = discord.Embed(colour = discord.Color.red())
                    emb.add_field(name = ctx.author.name, value = "Допускаеться кол-во вариантов(от 2 - 20)")
                    await ctx.send(embed = emb)
                    return False
                emb = discord.Embed(title = f"Голосование от: {ctx.author.name}",colour=discord.Color.blue())
        
                value_for_field = ''

                for x in range(1,len(full_message)):
                    value_for_field += emojis[x+1] +  full_message[x] + '\n'

                emb.add_field(name = full_message[0], value = value_for_field)
                message = await ctx.send(embed = emb)
                for x in range(1,len(full_message)):
                    await message.add_reaction(emojis[x+1])
                return value_for_field
    except:
        emb = discord.Embed(colour = discord.Color.red())
        emb.add_field(name = ctx.author.name, value = "Вопрос был указан некорректно.\nПример: `Вопрос ? Аргумент1! Аргумент2! Арг...!`.\nПервые 2 аргумента должны быть обязательно указаны")
        await ctx.send(embed = emb)
        return False


@bot.command()
async def stop_daily(ctx):
    global isDailyOn
    isDailyOn = False


async def call_daily(ctx, question = None, iter = None, setup = None):
    if setup:
        await daily_poll(ctx, question, iter)
    else:
        print("daily function is off")


@bot.command()
async def daily_poll(ctx, question = None, iter = None):
    global isDailyOn
    isDailyOn = True
    #task = asyncio.create_task(cancel_me())
    if iter != None:
        emb = discord.Embed(title = f"Голосование от: {ctx.author.name}",colour = discord.Color.blue())
        emb.add_field(name = "Хотите отключить 24 часовой опрос?", value = "Введите комманду /stop_daily .\nЕсли захотите возобновить опрос, используйте комманду /daily_poll")
        await ctx.send(embed = emb)
    #await message.add_reaction(emojis[emojis.index(":x:")]) # get Cross emoji
    await poll(ctx, question)
    await asyncio.sleep(60**2*24)
    await call_daily(ctx, question, iter = None, setup = isDailyOn)

@bot.command()
async def vk_prom(ctx):
    while True:
        await ctx.send(vk_prom_message)
        await asyncio.sleep(60**2)


bot.run(config.TOKEN)
