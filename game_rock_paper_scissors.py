import random
import currency


# rock paper scissors game
async def rock_paper_scissors(member_id, shot, bet_amount, server_id):
    if await currency.bet_is_enough(member_id, bet_amount, server_id):
        casino_shot = random.randint(1, 3)

        if shot != 'rock' and shot != 'paper' and shot != 'scissors' or not str(bet_amount).isdigit():
            return 'Invalid input, try again! :anger:'

        user_result = ':anger: Error: Invalid input!! :anger:'
        status = ''
        status_tie = 'It\'s a tie...'

        casino = '𝖈𝖆𝖘𝖎𝖓𝖔💸: '
        user = ': '
        rock = ':right_facing_fist:'
        paper = ':hand_splayed:'
        scissors = ':v:'

        # rock
        if casino_shot == 1:
            casino_result = casino + rock
            if shot == 'rock':
                user_result = user + rock
                status = status_tie
            elif shot == 'paper':
                user_result = user + paper
                await currency.update_currency(member_id, bet_amount, server_id)
                status = 'You won **{0} gold**! :tada: :tada: :moneybag: New Balance: **{1} gold**!'.format(bet_amount * 2, await currency.get_currency_amount(member_id, server_id))
            elif shot == 'scissors':
                user_result = user + scissors
                await currency.update_currency(member_id, -bet_amount, server_id)
                status = 'You lost **{0} gold**! :sob: :sob: :moneybag: New Balance: **{1} gold**!'.format(bet_amount, await currency.get_currency_amount(member_id, server_id))
        # paper
        elif casino_shot == 2:
            casino_result = casino + paper
            if shot == 'rock':
                await currency.update_currency(member_id, -bet_amount, server_id)
                user_result = user + rock
                status = 'You lost **{0} gold**! :tada: :tada: :moneybag: New Balance: **{1} gold**!'.format(bet_amount, await currency.get_currency_amount(member_id, server_id))
            elif shot == 'paper':
                user_result = user + paper
                status = status_tie
            elif shot == 'scissors':
                user_result = user + scissors
                await currency.update_currency(member_id, bet_amount, server_id)
                status = 'You won **{0} gold**! :tada: :tada: :moneybag: New Balance: **{1} gold**!'.format(bet_amount * 2, await currency.get_currency_amount(member_id, server_id))
        # scissors
        else:
            casino_result = casino + scissors
            if shot == 'rock':
                user_result = user + rock
                await currency.update_currency(member_id, bet_amount, server_id)
                status = 'You won **{0} gold**! :tada: :tada: :moneybag: New Balance: **{1} gold**!'.format(bet_amount * 2, await currency.get_currency_amount(member_id, server_id))
            elif shot == 'paper':
                await currency.update_currency(member_id, -bet_amount, server_id)
                user_result = user + paper
                status = 'You lost **{0} gold**! :tada: :tada: :moneybag: New Balance: **{1} gold**!'.format(bet_amount, await currency.get_currency_amount(member_id, server_id))
            elif shot == 'scissors':
                user_result = user + scissors
                status = status_tie

        return [casino_result, user_result, status]
    else:
        return ':x: :moneybag: :x:  You do not have enough gold! :cold_sweat: :cold_sweat: '
