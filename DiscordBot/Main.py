import random
import time

import discord
import logging

import DiscordTicTacToe as TicTacToe
import DiscordMenschÄrgereDichNicht as Ludo

from discord.ext import commands

"""
Author: Philipp Nußdorfer
Date: 15.2.2023
Version: 0.1.2
Description: Is a discord bot where a user can challenge other users and play some games with them.
"""

ticTacToe = TicTacToe.CreateGameField()
game_field = ticTacToe.get_game_field()

handler = logging.FileHandler(filename='Discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)


async def tictactoe_game(ctx, player1):

    player_num = random.randint(0, 1)
    player_x = ctx.author
    player_o = player1

    while True:
        if TicTacToe.handle_win_con(game_field, player_x, player_o) == player_x:
            await ctx.send("winner is : ", player_x.name)
            return None
        elif TicTacToe.handle_win_con(game_field, player_x, player_o) == player_o:
            await ctx.send("winner is : ", player_o.name)
            return None

        if TicTacToe.get_player_sym(player_num) == "O":
            await ctx.send("It's " + str(player_o) + " turn")
        else:
            await ctx.send("Its " + str(player_x) + " turn")

        while True:
            num = 0
            await ctx.send("-- 0    1    2")
            for row in game_field:
                msg = "| {} {}".format(num, row)
                await ctx.send(msg)
                num += 1
            try:

                def check(m):
                    return m.channel == ctx.channel and m.author == TicTacToe.get_player(player_num, player_x, player_o)

                await ctx.send("Please input the row of the field or input exit to surrender: ")
                cor_x = await bot.wait_for("message", check=check)

                if cor_x.content == "exit":
                    message = TicTacToe.get_player(player_num, player_x, player_o).name, " has surrendered :flag_white:"
                    await ctx.send(message)
                    return None

                await ctx.send("Please Input the colum of the field: ")
                cor_y = await bot.wait_for("message", check=check)

                cor_x = int(cor_x.content)
                cor_y = int(cor_y.content)

                if 3 > cor_x >= 0 and 3 > cor_y >= 0 and TicTacToe.check_if_free(game_field, cor_x, cor_y):
                    game_field[cor_x][cor_y] = TicTacToe.get_player_sym(player_num)
                    break
            except:
                await ctx.send("Please enter a valid Number")

        player_num = TicTacToe.change_player(player_num)


@bot.command()
async def tictactoe(ctx, member):
    await tictactoe_game(ctx, member)
    await ctx.send("GG")


@bot.command()
async def ask(ctx):
    await ctx.send("How old are you")

    def check(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author

    answer = await bot.wait_for('message', check=check)
    m = "{} is, years old: {}".format(ctx.author, answer.content)
    await ctx.send(m)


bot.run("")

    #import os
    #os.path.join('app', 'subdir', 'dir', 'filename.foo')
    #'app/subdir/dir/filename.foo'
