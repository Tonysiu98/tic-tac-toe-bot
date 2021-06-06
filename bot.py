import os
from discord.ext import commands
import random
from game_lib import print_board, update_board, current_player, reset_game, input_check


token = os.environ['TOKEN']


free_pos = [ i for i in range(9)]

player_pos = {'x':[], 'o':[]}

def reset_game():
    global current_player, board, free_pos, player_pos
    current_player = None
    board = [str(i) for i in range(9)]
    free_pos = [ i for i in range(9)]
    player_pos = {'x':[], 'o':[]}


# Function to check if any player has won
def check_win(player_pos, cur_player):
    # All possible winning combinations
    soln = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
 
    # Loop to check if any winning combination is satisfied
    for x in soln:
        if all(y in player_pos[cur_player] for y in x):
 
            # Return True if any winning combination satisfies
            return True
    # Return False if no combination is satisfied       
    return False       
 
# Function to check if the game is drawn
def check_draw(player_pos):
    if len(player_pos['x']) + len(player_pos['o']) == 9:
        return True
    return False
    
async def board_update(ctx, pos):
    global board, player_pos
    # Updating grid status 
    board[pos] = "x"
    
    # Updating player positions
    player_pos["x"].append(pos)

    if check_win(player_pos, "x"):
            await print_board(ctx, board)
            await ctx.send("Player won")
            reset_game()
            return
    free_pos.remove(pos)

    bot_move = random.choice(free_pos)

    board[bot_move] = "o"

    player_pos["o"].append(bot_move)

    free_pos.remove(bot_move)

    if check_win(player_pos, "o"):
            await print_board(board)
            await ctx.send("bot won")
            reset_game()
            return
    await print_board(ctx, board)

# Basic bot set up
bot = commands.Bot(command_prefix='$')

@bot.command()
async def start(ctx):
    global current_player
    if current_player != None:
        await ctx.send("Current player is {}, please wait".format(current_player))
    else:
        await ctx.send("Bring it on {} !!!".format(ctx.author.name))
        await print_board(ctx)
        current_player = ctx.author.name

@bot.command()
async def take(ctx, x, y):
    global current_player, board
    if current_player != ctx.author.name:
        await ctx.send("Sorry this is not your game yet >//<")
    else:
        pos_x, pos_y = input_check(x, y)
        if pos_x == -1 :
            await ctx.send("Input is invalid, should be between 0 and 2")
        else:
            await update_board(ctx, pos_x, pos_y)

@bot.command()
async def reset(ctx):
    if (ctx.author.name != current_player):
         await ctx.send("You cannot reset the game as you are the current player")
    reset_game()
    await ctx.send("The game has been reset!")

bot.run(token)
