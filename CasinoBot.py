import discord
import CasinoBotToken

import game_rock_paper_scissors
import game_lightning
import game_coin_flip
import currency
import about

client = discord.Client()
global prefix
prefix = '$'


# this function responds to users based on the command (if the command exists)
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # says hello
    if message.content.startswith(prefix + 'hello'):
        msg = 'Hello {0.author.mention} :wave:!'.format(message)
        await client.send_message(message.channel, msg)

    # outputs the author's id (for testing)
    if message.content.startswith(prefix + 'id'):
        await client.send_message(message.channel, message.author.id)

    # outputs the server's id (for testing)
    if message.content.startswith(prefix + 'serverid'):
        await client.send_message(message.channel, message.server.id)

    # get user currency amount
    if message.content.startswith(prefix + 'bank'):
        currency_amt = await currency.get_currency_amount(message.author.id, message.server.id)
        msg = '{0.author.mention}, you have {1} gold.'.format(message, currency_amt)
        await client.send_message(message.channel, msg)

    # god given gold
    if message.content.startswith(prefix + 'godgold'):
        try:
            recipient_id = message.mentions[0].id
            msg = await currency.god_gold(message.author.id, recipient_id, int(message.content.split()[2]), message.server.id)
            await client.send_message(message.channel, msg)
        except IndexError:
            await client.send_message(message.channel, message.author.mention + ', :anger: Error: Invalid input!! :anger:')
        except ValueError:
            await client.send_message(message.channel, message.author.mention + ', :anger: You did not enter a number!! :anger:')
        except:
            await client.send_message(message.channel, message.author.mention + ', :anger: Error: Something went wrong. :anger:')

    # god given gold
    if message.content.startswith(prefix + 'givegold'):
        try:
            recipient_id = message.mentions[0].id
            msg = await currency.give_gold(message.author.id, recipient_id, int(message.content.split()[2]), message.server.id)
            await client.send_message(message.channel, msg)
        except IndexError:
            msg = 'Something went wrong!!! Try again :('
            await client.send_message(message.channel, msg)


    # daily gold
    if message.content.startswith(prefix + 'blessing'):
        msg = message.author.mention + ', ' + await currency.daily_gold(message.author.id, message.server.id)
        await client.send_message(message.channel, msg)

    # help
    if message.content.startswith(prefix + 'help'):
        msg = await about.about()
        await client.send_message(message.channel, embed=msg)

    # coin flip
    if message.content.startswith(prefix + 'flip'):
        try:
            guess = message.content.split()[1]
            bet_amount = message.content.split()[2]
            bet_amount = int(bet_amount)
            result = await game_coin_flip.coin_flip(message.author.id, guess, bet_amount, message.server.id)
            await client.send_message(message.channel, message.author.mention + ', ' + result)
        except IndexError:
            await client.send_message(message.channel, message.author.mention + ', :anger: Error: Invalid input!! :anger:')
        except ValueError:
            await client.send_message(message.channel, message.author.mention + ', :anger: You did not enter a number!! :anger:')

    # lightning game
    if message.content.startswith(prefix + 'lightning'):
        msg = message.author.mention + ': ' + await game_lightning.lightning(message.author.id, message.server.id)
        await client.send_message(message.channel, msg)

    # rock paper scissors
    if message.content.startswith(prefix + 'rps'):
        try:
            user_message = message.content.split()
            shot = user_message[1]
            bet_amount = int(user_message[2])
            result = await game_rock_paper_scissors.rock_paper_scissors(message.author.id, shot, bet_amount, message.server.id)
            msg = '{0}\n{1.author.mention}{2}\n{3}'.format(result[0], message, result[1], result[2])
            await client.send_message(message.channel, msg)
        except IndexError:
            await client.send_message(message.channel, message.author.mention + ', :anger: Error: Invalid input!! :anger:')
        except ValueError:
            await client.send_message(message.channel, message.author.mention + ', :anger: You did not enter a number!! :anger:')



# prints to the console when the bot is live!
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    client.change_status(game=(discord.Game(name="my prefix is $")))
    print('------')

client.run(CasinoBotToken.get_token())
