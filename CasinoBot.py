import discord
import CasinoBotToken

import game_coin_flip
import currency

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

    # get user currency amount
    if message.content.startswith(prefix + 'bank'):
        currency_amt = await currency.get_currency_amount(message.author.id)
        msg = '{0.author.mention}, you have {1} gold.'.format(message, currency_amt)
        await client.send_message(message.channel, msg)

    # god given gold
    if message.content.startswith(prefix + 'godgold'):
        print(message.mentions)
        recipient_id = message.mentions[0].id
        await currency.give_gold(client, message.author.id, recipient_id, int(message.content.split()[2]))

    # coin flip
    if message.content.startswith(prefix + 'flip'):
        guess = message.content.split()[1]
        result = await game_coin_flip.coin_flip(guess)
        await client.send_message(message.channel, result)


# prints to the console when the bot is live!
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(CasinoBotToken.get_token())
