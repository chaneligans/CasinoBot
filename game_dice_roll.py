import currency
import random

# dice roll game
async def dice_roll(member_id, bet_amount, num_sides, guess, server_id):
    if await currency.bet_is_enough(member_id, bet_amount, server_id):
        if num_sides < 2:
            return ':game_die: Invalid number of sides!!! :angry:'
        if not str(guess).isdigit():
            return ':game_die:  You did not enter a number!!! :angry:'
        if 0 > guess > num_sides:
            return ':game_die:  Invalid guess!!! :angry:'
        side = random.randint(1, num_sides)
        message = '\n:game_die: The die landed on... :game_die: '
        if guess == side:
            if num_sides > 4:
                win_amount = int(bet_amount + (bet_amount * .2))
                new_currency = await currency.update_currency(member_id, win_amount, server_id)
            else:
                win_amount = bet_amount
                new_currency = await currency.update_currency(member_id, win_amount, server_id)
            message += '**{0}**!!! :tada: :tada: You **won {1} gold**!!! :moneybag: New Balance: **{2} gold**'.format(side, win_amount, new_currency)
        else:
            win_amount = -bet_amount
            new_currency = await currency.update_currency(member_id, win_amount, server_id)
            message += '**{0}**!!! :sob: :sob: You **lost {1} gold**... :moneybag: New Balance: **{2} gold**'.format(side, -win_amount, new_currency)
        if 0 < win_amount < 1000:
            message += '\n\n:gem: Hint: Want to win big next time? :stuck_out_tongue_winking_eye: ' \
                       '\nIf you roll with sides **greater than 6**, you recieve **extra gold** if you win!! :money_mouth: :money_mouth: :money_mouth: '
        if win_amount < 0:
            message += '\n\n:gem: Hint: Want to **win your money back**? :stuck_out_tongue_winking_eye: ' \
                       '\nIf you roll with sides **greater than 4**, you recieve **20% extra gold** if you win!! :money_mouth: :money_mouth: :money_mouth: '
        return message
    else:
        return ':x: :moneybag: :x:  You do not have enough gold! :cold_sweat: :cold_sweat: '
