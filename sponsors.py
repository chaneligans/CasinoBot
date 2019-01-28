import random

# Austin Min - $phun
# displays a random pun
async def phun():
    puns_list = ['What do you call a fake noodle? An Impasta.',
                 'How does a penguin build it\'s house? Igloos it together.',
                 'What do you call a Mexican who has lost his car? Carlos.',
                 'I\'ll call you later. Don\'t call me later, call me 𝖈𝖆𝖘𝖎𝖓𝖔💸.',
                 'A furniture store keeps calling me. All I wanted was one night stand.',
                 'I don’t play soccer because I enjoy the sport. I’m just doing it for kicks.',
                 'Did I tell you the time I fell in love during a backflip? I was heels over head.']
    pun_index = random.randint(0, len(puns_list) - 1)
    return puns_list[pun_index]


# Ronald Kem - $kem
# to be decided
async def kem():
    return 'Ronald has yet to decide what this command will do.'


# Collin Chao - $playin
# to be decided
async def playin():
    return 'Collin has yet to decide what this command will do.'
