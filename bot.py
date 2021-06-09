import os
from discord.ext import commands
from game_lib import update_board, input_check, init_game

token = os.environ['TOKEN']

game_map = {}

async def print_board(ctx, board):
    response = """ ```
    $ # # # $ # # # $ # # # $
    #       #       #       #
    #   {}   #   {}   #   {}   #
    #       #       #       #
    $ # # # $ # # # $ # # # $ 
    #       #       #       #
    #   {}   #   {}   #   {}   #
    #       #       #       #
    $ # # # $ # # # $ # # # $ 
    #       #       #       #
    #   {}   #   {}   #   {}   #
    #       #       #       #
    $ # # # $ # # # $ # # # $ 

    ```
    """.format(board[0][0], board[0][1], board[0][2], 
                board[1][0], board[1][1], board[1][2], 
                board[2][0], board[2][1], board[2][2])
    await ctx.send(response)

# Basic bot set up
bot = commands.Bot(command_prefix='$')

@bot.command()
async def start(ctx):
    if ctx.author.name in game_map:
        await ctx.send("You have a game already")
        await print_board(ctx, board)
    else:
        # Show game
        board, depth = init_game()
        game_map[ctx.author.name] = [board,depth]
        await ctx.send("Bring it on <@{}> !!!".format(ctx.author.id))
        await print_board(ctx, board)

@bot.command()
async def take(ctx, x, y):
    global game_map
    if ctx.author.name not in game_map:
        await ctx.send("Sorry you did not start a game yet")
    else:
        board, depth = game_map[ctx.author.name]
        pos_x, pos_y = input_check(x, y)
        if pos_x == -1 :
            await ctx.send("Input is invalid, should be between 0 and 2")
        else:
            new_board, new_depth, winner = update_board(board, depth, pos_x, pos_y)
            if (winner == -1) :
                await ctx.send("The place has been taken, please choose another one")
            elif (winner == 'x'):
                await ctx.send("Yay you won <@{}>".format(ctx.author.id))
                game_map.pop(ctx.author.name)
            elif (winner == 'o'):
                await ctx.send("LMAO you lost the game <@{}>".format(ctx.author.id))
                game_map.pop(ctx.author.name)
            elif (winner == 1):
                await ctx.send("Ops tie game <@{}>".format(ctx.author.id))
                game_map.pop(ctx.author.name)
            else:
                game_map[ctx.author.name] = [new_board, new_depth]
            await print_board(ctx, board)

@bot.command()
async def reset(ctx):
    global game_map
    if ctx.author.name not in game_map:
         await ctx.send("You have no game to reset")
    else:
        game_map.pop(ctx.author.name)
        await ctx.send("The game has been reset!")


bot.run(token)

