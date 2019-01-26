import discord

client = discord.Client()
prefix = '$'

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(prefix + 'hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run('NTM4NTMxMzY4NTM2Mzc1MzA2.Dy1XOA.VEaHYhsjTy456Ge_g0OUCBktYEg')
