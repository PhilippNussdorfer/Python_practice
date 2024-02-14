import discord
from discord.ext import commands
from calculator.Interpreater import Iterpreter

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='§', intents=intents)
#client = discord.Client(intents=intents)


#@client.event
#async def on_message(msg):
#    if msg.author != client.user:
#        if msg.content.startswith('hello'):
#            await msg.channel.send('Hello!')


@bot.command()
async def calc(ctx, num: float, operator, sec_num: float):
    result = await Iterpreter().interpret(operation=operator, num=num, sec_num=sec_num)
    print(f"result: {result}")
    await ctx.send(result)


@bot.command()
async def test(ctx):
    await ctx.send("it work's")


bot.run('')
#client.run('')
