import random

import discord
from discord.ext.commands import Bot

import casinodb
import about
import currency
import CasinoBotToken
import game_eightball
import game_coin_flip
import game_dice_roll
import game_lightning
import game_rock_paper_scissors
import sponsors

BOT_PREFIX = ("$", 'cas', 'casino')
TOKEN = CasinoBotToken.get_token()

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

# says hello
@client.command(name='hello',
                description='Says hello!',
                brief='Will you say hi back to me?',
                aliases=['hi', 'hey'],
                pass_context=True)
async def hello(context):
    msg = ', hello! :wave:'
    await client.say(context.message.author.mention + msg)


##### TESTING #####


# outputs the user's id for testing
@client.command(pass_context=True)
async def user_id(context):
    msg = 'Your id is: {0}'.format(context.message.author.id)
    await client.say(msg)


# outputs the server's id for testing
@client.command(pass_context=True)
async def server_id(context):
    msg = 'This server\'s id is: {0}'.format(context.message.server.id)
    await client.say(msg)


# get the user name from the id
@client.command(pass_context=True)
async def get_user(context):
    uid = context.message.content.split()[1]
    await client.say('<@!{0}>'.format(uid))


##### CURRENCY #####


# outputs the user's currency amount
@client.command(name='bank',
                description='displays the amount of gold you\'ve accumulated.',
                brief='displays the amount of gold you\'ve accumulated.',
                aliases=['$', 'bal', 'balance', 'money'],
                pass_context=True)
async def bank(context):
    currency_amt = await currency.get_currency_amount(context.message.author.id, context.message.server.id)
    msg = '{0.author.mention}, you have **{1} gold**.'.format(context.message, currency_amt)
    await client.say(msg)


# displays the users with the most gold (up to 5)
@client.command(name='top',
                description='displays the users with the most gold!',
                brief='displays the users with the most gold!',
                pass_context=True)
async def top(context):
    msg = await currency.top_five_to_string(context.message.server.id, client)
    await client.say(msg)


# admin gives people gold
@client.command(name='godgold',
                description='God gives you gold!!! Admin only command',
                brief='God gives you gold!!! Admin only command',
                pass_context=True)
async def godgold(context):
    try:
        if context.message.author.server_permissions.administrator:
            recipient_id = context.message.mentions[0].id
            msg = await currency.god_gold(recipient_id, int(context.message.content.split()[2]), context.message.server.id)
        else:
            msg = "You are not a god!"
        await client.say(msg)
    except IndexError:
        await client.say(context.message.author.mention + ', :anger: Error: Invalid input!! :anger:')
    except ValueError:
        await client.say(context.message.author.mention + ', :anger: You did not enter a number!! :anger:')
    except Exception as e:
        await client.say(context.message.author.mention + ', :anger: {0}: Something went wrong. :anger:'.format(e))


# users give each other gold
@client.command(name='givegold',
                pass_context=True,
                description='[@recipient] - give gold to your friends!',
                brief='[@recipient] - give gold to your friends!',
                alias=['give', 'donate'])
async def givegold(context):
    try:
        recipient_id = context.message.mentions[0].id
        msg = await currency.give_gold(context.message.author.id, recipient_id, int(context.message.content.split()[2]),
                                       context.message.server.id)
        await client.say(msg)
    except Exception as e:
        msg = 'Something went wrong!!! [{0}] Try again :('.format(e)
        await client.say(msg)


# give users gold every hour
@client.command(name='blessing',
                pass_context=True,
                description='will the gods grant you a blessing?',
                brief='will the gods grant you a blessing?',
                alias=['daily'])
async def blessing(context):
    result = await currency.daily_gold(context.message.author.id, context.message.server.id)
    msg = '{0}, {1}'.format(context.message.author.mention, result)
    await client.say(msg)


##### ABOUT / HELP #####


# displays about / help
# help
@client.event
async def on_message(message):
    for prefix in BOT_PREFIX:
        if message.content.startswith(prefix + 'help') or message.content.startswith(prefix + ' help'):
            msg = await about.about()
            await client.send_message(message.channel, embed=msg)
    await client.process_commands(message)


###### GAMES #####

# 8ball game
@client.command(name='8ball',
                description='Answers a yes/no question.',
                brief='Answers from the beyond.',
                aliases=['8', 'eightball'],
                pass_context=True)
async def eight_ball(context):
    msg = game_eightball.eightball()
    await client.say(context.message.author.mention + ',' + random.choice(msg))


# coin flip
@client.command(name='coin_flip',
                aliases=['flip'],
                description='[heads / tails] [bet amount] - bet on the flip of a coin.',
                brief='[heads / tails] [bet amount] - bet on the flip of a coin.',
                pass_context=True)
async def coin_flip(context):
    try:
        guess = context.message.content.split()[1]
        bet_amount = context.message.content.split()[2]
        bet_amount = int(bet_amount)
        result = await game_coin_flip.coin_flip(context.message.author.id, guess, bet_amount, context.message.server.id)
        await client.say(context.message.author.mention + ', ' + result)
    except IndexError:
        await client.say(context.message.author.mention + ', :anger: Error: Invalid input!! :anger:')
    except ValueError:
        await client.say(context.message.author.mention + ', :anger: You did not enter a number!! :anger:')


# lightning game
@client.command(name='lightning',
                description='lightning strikes!',
                brief='lightning strikes!',
                pass_context=True)
async def lightning(context):
    msg = context.message.author.mention + ': ' + await game_lightning.lightning(context.message.author.id,
                                                                                 context.message.server.id)
    await client.say(msg)


# rock paper scissors
@client.command(name='rps',
                description='[rock / paper / scissors] [bet amount]- rock paper scissors!',
                brief='[rock / paper / scissors] [bet amount]- rock paper scissors!',
                pass_context=True)
async def rps(context):
    try:
        user_message = context.message.content.split()
        shot = user_message[1]
        bet_amount = int(user_message[2])
        result = await game_rock_paper_scissors.rock_paper_scissors(context.message.author.id, shot, bet_amount,
                                                                    context.message.server.id)
        msg = '{0}\n{1.author.mention}{2}\n{3}'.format(result[0], context.message, result[1], result[2])
        await client.say(msg)
    except IndexError:
        await client.say(context.message.author.mention + ', :anger: Error: Invalid input!! :anger:')
    except ValueError:
        await client.say(context.message.author.mention + ', :anger: You did not enter a number!! :anger:')


# dice roll
@client.command(name='roll',
                description='[num sides] [guess] [bet amount]- bet on the roll of a die.',
                brief='[num sides] [guess] [bet amount]- bet on the roll of a die.',
                pass_context=True,
                alias=['dice', 'rolldice', 'diceroll'])
async def roll(context):
    try:
        user_message = context.message.content.split()
        num_sides = int(user_message[1])
        guess = int(user_message[2])
        bet_amount = int(user_message[3])
        result = await game_dice_roll.dice_roll(context.message.author.id, bet_amount, num_sides, guess,
                                                context.message.server.id)
        msg = context.message.author.mention + ', ' + result
        await client.say(msg)
    except IndexError:
        await client.say(context.message.author.mention + ', :anger: Error: Invalid input!! :anger:')
    except ValueError:
        await client.say(context.message.author.mention + ', :anger: You did not enter a number!! :anger:')


##### SPONSOR FUNCTIONS #####

# Austin $phun
@client.command(name='phun')
async def phun():
    await client.say(await sponsors.phun())


# Ronald $kem
@client.command(name='kem')
async def kem():
    await client.say(await sponsors.kem())


# Collin $playin
@client.command(name='playin')
async def playin():
    await client.say(await sponsors.playin())


# Phoenix $fb
@client.command(name='flipbattle',
                aliases=['fb', 'bf', 'battleflip'])
async def flipbattle():
    await client.say(await sponsors.flipbattle())


# Phoenix $fb
@client.command(name='db',
                pass_context=True)
async def db(context):
    await casinodb.db_get_user_info(context.message.author.id, context.message.server.id)


@client.event
async def on_server_join(server):
    print('Joined new server ', server.name)
    print('Now running on {0} servers!\n'.format(len(client.servers)))
    msg = ':money_mouth: :money_mouth: Thanks for adding me to **{0}**! My **prefixes** are **{1}**. If you need' \
          ' help with anything, enter **{2}help**! :money_with_wings:'.format(server.name, BOT_PREFIX, BOT_PREFIX[0])

    for channel in server.channels:
        if not isinstance(channel.type, int):
            if channel.permissions_for(server.me).send_messages and (channel.type.name == "text"):
                await client.send_message(channel, msg)
                break

##### ON READY #####


# prints to the console when the bot is online
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('Running on {0} server(s)!'.format(len(client.servers)))
    print(client.user.id)
    help_msg = '{0}help'.format(BOT_PREFIX[0])
    await client.change_presence(game=discord.Game(name=help_msg))
    print('------')

client.run(TOKEN)
