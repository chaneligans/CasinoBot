import random


async def eight_ball():
    possible_responses = [
        'As I see it, yes'
        'Ask again later'
        'Better not tell you now.'
        'Cannot predict now!'
        'That does not seem likely.'
        'Of course.'
        'Concentrate and ask again'
        'Don’t count on it'
        'It is certain'
        'It is decidedly so'
        'Most likely'
        'My reply is no'
        'My sources say no'
        'Outlook good'
        'Outlook not so good'
        'Reply hazy try again'
        'Signs point to yes'
        'Very doubtful'
        'Without a doubt'
        'You may rely on it'
    ]

    return possible_responses[random.randint(0, len(possible_responses))]
