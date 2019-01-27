import member_csv_info
import time


# returns the amount of gold a user has
async def get_currency_amount(member_id, server_id):
    currency_amount = await member_csv_info.get_user_csv_currency_amt(member_id, server_id)
    return currency_amount


# updates the user's currency amount
# returns new currency
async def update_currency(member_id, amount, server_id):
    return await member_csv_info.set_currency(member_id, amount, server_id)


# gives a user gold (not from the giver's bank) if the giver is an admin
async def god_gold(giver_id, recipient_id, amount, server_id):
    print(await member_csv_info.is_admin(giver_id, server_id))
    if (await member_csv_info.is_admin(giver_id, server_id)) == True:
        new_amt = await update_currency(recipient_id, amount, server_id)
        return ':angel: God just gave <@!{0}> {1} gold!! New balance: {2} gold :money_mouth: :money_mouth:'.format(recipient_id, amount, new_amt)
    else:
        return ':japanese_goblin: You are not a god!'


# gives a user gold (not from the giver's bank) if the giver is an admin
async def give_gold(giver_id, recipient_id, amount, server_id):
    giver_new_amt = await update_currency(giver_id, -amount, server_id)
    recipient_new_amt = await update_currency(recipient_id, amount, server_id)
    return ':angel: <@!{0}> just gave <@!{1}> {2} gold!!'.format(giver_id, recipient_id, amount)


# checks if the bet amount is greater than the amount of current gold
async def bet_is_enough(member_id, bet_amount, server_id):
    current_currency_amt = await get_currency_amount(member_id, server_id)
    return current_currency_amt >= bet_amount


# gives user daily gold
# returns a messagae with the new currency amount
async def daily_gold(member_id, server_id):
    daily_amt = 125
    hour_in_secs = 60.0 * 60.0
    last_daily_recieved_time = await member_csv_info.get_user_csv_daily_time(member_id, server_id)
    next_available_time = await member_csv_info.get_user_csv_daily_time(member_id, server_id) + hour_in_secs
    if last_daily_recieved_time == -1 or next_available_time < time.time():
        new_currency_amt = await update_currency(member_id, daily_amt, server_id)
        message = ':money_mouth: The casino gods have awarded you with 125 gold!! Your new balance is {0} gold :money_mouth:'.format(new_currency_amt)
        await member_csv_info.set_last_daily_time(member_id, server_id)
    else:
        time_remaining = next_available_time - time.time()
        time_remaining_min = int(time_remaining // 60)
        time_remaining_sec = int(time_remaining % 60)
        message = 'The gods don\'t feel like blessing you right now... Try again in {0} minutes and {1} seconds.'.format(time_remaining_min, time_remaining_sec)
    return message
