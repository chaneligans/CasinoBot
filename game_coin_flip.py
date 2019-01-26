import random
import currency


# coin flip game
async def coin_flip(member_id, guess, bet_amount):
    if currency.bet_is_enough(member_id, bet_amount):
        msg_result = 'Something\'s wrong! You shouldn\'t be seeing this.'
        guess_correct = False
        coin_num = random.randint(1, 2)

        if guess != 'heads' and guess != 'tails':
            return 'Invalid input, try again! :anger:'

        if coin_num == 1:
            msg_result = 'The coin landed on heads!'
            if guess == 'heads':
                guess_correct = True
        elif coin_num == 2:
            msg_result = 'The coin landed on tails!'
            if guess == 'tails':
                guess_correct = True

        if guess_correct:
            win_amount = bet_amount * 2
            new_balance = await currency.update_currency(member_id, win_amount)
            message = '{0} You win {1}:bangbang: :tada:\nYour new balance is {2} gold!'.format(msg_result, win_amount, new_balance)
            return message
        else:
            win_amount = bet_amount * -2
            new_balance = await currency.update_currency(member_id, win_amount)
            message = '{0} You lose {1}... :sob:\nYour new balance is {2} gold!'.format(msg_result, win_amount, new_balance)
            return message
    else:
        return 'You do not have enough gold!'
