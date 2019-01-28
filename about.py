import discord


# displays information about the bot as well as current commands
async def about():
    about_message = '```fix' \
                    '\nHello! I am 𝖈𝖆𝖘𝖎𝖓𝖔💸, formally known as 𝑪𝒂𝒔𝒊𝒏𝒐𝑩𝒐𝒕!' \
                    '\nI was created by my cool mommy, 𝒄𝒉𝒂𝒏𝒆𝒍#8258 using 𝗱𝗶𝘀𝗰𝗼𝗿𝗱.𝗽𝘆.' \
                    '\nIf you 𝒍𝒐𝒗𝒆 me, consider donating to my mommy!' \
                    '\nvenmo: @𝒄𝒉𝒂𝒏𝒆𝒍𝒛𝒛𝒛 :)```'
    commands = '\n```yaml' \
               '\n$𝗵𝗲𝗹𝗹𝗼 - says hello!' \
               '\n$𝗯𝗮𝗻𝗸 - displays the amount of gold you\'ve accumulated.' \
               '\n$𝗯𝗹𝗲𝘀𝘀𝗶𝗻𝗴 - will the gods grant you a blessing?' \
               '\n$𝗴𝗶𝘃𝗲𝗴𝗼𝗹𝗱 [@recipient] - give gold to your friends!' \
               '\n$𝗵𝗲𝗹𝗽 - displays this message.' \
               '\n$𝘁𝗼𝗽 - displays the users with the most gold!```'
    games = '```diff' \
            '\n-$𝗳𝗹𝗶𝗽 [heads / tails] [bet amount] - bet on the flip of a coin.' \
            '\n-$𝗹𝗶𝗴𝗵𝘁𝗻𝗶𝗻𝗴 - lightning strikes!' \
            '\n-$𝗿𝗼𝗹𝗹 [num sides] [guess] [bet amount]- bet on the roll of a die.' \
            '\n-$𝗿𝗽𝘀 [rock / paper / scissors] [bet amount]- rock paper scissors!' \
            '```'
    sponsors = 'Special shoutout to my sponsors!!!' \
               '\n```md' \
               '\n# Ronald K. - $𝗸𝗲𝗺 - [to be decided]' \
               '\n# Austin M. - $𝗽𝗵𝘂𝗻 - displays a pun' \
               '\n# Collin C. - $𝗽𝗹𝗮𝘆𝗶𝗻 - [to be decided]' \
               '\n```'
    embed = discord.Embed(title="𝖈𝖆𝖘𝖎𝖓𝖔💸 Help", description='Help is here!!!',  color=0xFFFFFF)
    embed.add_field(name="About", value=about_message, inline=False)
    embed.add_field(name="Commands", value=commands, inline=False)
    embed.add_field(name="Games", value=games, inline=False)
    embed.add_field(name="Sponsors", value=sponsors, inline=False)
    return embed
