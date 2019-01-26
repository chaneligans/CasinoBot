import discord
import CasinoBotToken
import random

client = discord.Client()
global prefix
prefix = '$'


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(prefix + 'hello'):
        msg = 'Hello {0.author.mention} :wave:!'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(prefix + 'flip'):
        guess = message.content.split()[1]
        await coin_flip(message.channel, guess)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


async def coin_flip(channel, guess):
    msg_win = 'You win!'
    msg_lose = 'You lose!'
    guess_correct = False
    coin_num = random.randint(1, 2)

    if guess != 'heads' and guess != 'tails':
        await client.send_message(channel, 'Invalid input, try again! :anger:')
        return

    if coin_num == 1:
        await client.send_message(channel, 'The coin landed on heads!')
        if guess == 'heads':
            guess_correct = True
    elif coin_num == 2:
        await client.send_message(channel, 'The coin landed on tails!')
        if guess == 'tails':
            guess_correct = True

    if guess_correct == True:
        await client.send_message(channel, msg_win)
    else:
        await client.send_message(channel, msg_lose)





client.run(CasinoBotToken.get_token())
