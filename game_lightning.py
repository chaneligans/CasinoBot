import random
import currency


# lightning game
# super jackpot: 50000 gold - 1%
# jackpot: 10000 gold - 5% chance
# normal win: 150 - 300 gold - 20% chance
# neutral: nothing happens - 48%
# normal loss: 25-50% - 20%
# jackpot loss: lose 75% - 5%
# super jackpot loss: lose everything - 1%
async def lightning(member_id):
    result = random.randint(1,100)
    lightning_hit = 'Something went wrong. You shouldn\'t be seeing this!'
    win_amount = 0

    if result == 1:
        win_amount = 50000
        await currency.update_currency(member_id, win_amount)
        return ':zap: :zap: :zap: **The lightning is made of gold!** :money_mouth: :money_mouth: You got **{0} gold**. :moneybag: New balance: **{1} gold**'.format(win_amount, await currency.get_currency_amount(member_id))
    elif 2 <= result <= 6:
        win_amount = 10000
        await currency.update_currency(member_id, win_amount)
        return ':zap: :zap: :zap: **The lightning hit a chest near you!** :blush: :blush: You got **{0} gold**. :moneybag: New balance: **{1} gold**'.format(win_amount, await currency.get_currency_amount(member_id))
    elif 7 <= result <= 26:
        win_amount = random.randint(300, 500)
        await currency.update_currency(member_id, win_amount)
        return ':zap: :zap: :zap: Lightning strikes **in front of you**, drawing your attention to **{0} gold on the ground before you**! :laughing: :moneybag: New balance: **{1} gold**'.format(win_amount, await currency.get_currency_amount(member_id))
    elif 27 <= result <= 74:
        return ':zap: :zap: :zap: Lightning strikes somewhere in the distance. Nothing happens. :open_mouth:'
    elif 75 <= result <= 94:
        win_amount = int(await currency.get_currency_amount(member_id) * random.randint(25, 50) / 100)
        await currency.update_currency(member_id, -win_amount)
        return ':zap: :zap: :zap:  **Lightning strikes you!!** You brush it off, but **lose {0} gold**.:cold_sweat: :cold_sweat: :moneybag: New balance: **{1} gold**'.format(win_amount, await currency.get_currency_amount(member_id))
    elif 95 <= result <= 99:
        win_amount = int(await currency.get_currency_amount(member_id) * random.randint(60, 75) / 100)
        await currency.update_currency(member_id, -win_amount)
        return ':zap: :zap: :zap: **Lightning strikes you!!** You **pass out**, and wake up **short of {0} gold**. Someone must\'ve **looted your unconscious body**! :sob: :sob::moneybag: New balance: **{1} gold**'.format(win_amount, await currency.get_currency_amount(member_id))
    elif result == 100:
        win_amount = int(await currency.get_currency_amount(member_id))
        await currency.update_currency(member_id, -win_amount)
        return ':zap: :zap: :zap: **Lightning strikes you!!** You **pass out**, and wake up in a hospital with a **bill totaling up to {0} gold**?! :head_bandage: :scream: :moneybag: New balance: **{1} gold**'.format(win_amount, await currency.get_currency_amount(member_id))
