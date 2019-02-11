import time
from operator import itemgetter
import discord
import casinodb


# returns the amount of gold a user has
async def get_currency_amount(member_id, server_id):
    currency_amount = await casinodb.db_get_currency_amt(member_id, server_id)
    return currency_amount


# updates the user's currency amount
# returns new currency
async def update_currency(member_id, amount, server_id):
    old_amount = await casinodb.db_get_currency_amt(member_id, server_id)
    new_amount = amount + old_amount
    return await casinodb.db_set_currency(member_id, server_id, new_amount)


# gives a user gold (not from the giver's bank) if the giver is an admin
async def god_gold(recipient_id, amount, server_id):
    new_amt = await update_currency(recipient_id, amount, server_id)
    return ':angel: God just gave <@!{0}> {1} gold!! New balance: {2} gold :money_mouth: :money_mouth:'.format(recipient_id, amount, new_amt)


# gives a user gold (not from the giver's bank) if the giver is an admin
async def give_gold(giver_id, recipient_id, amount, server_id):
    if await bet_is_enough(giver_id, amount, server_id):
        giver_new_amt = await update_currency(giver_id, -amount, server_id)
        recipient_new_amt = await update_currency(recipient_id, amount, server_id)
        return ':angel: <@!{0}> just gave <@!{1}> {2} gold!!'.format(giver_id, recipient_id, amount)
    else:
        return '<@!{0}>, you can\'t give <@!{1}> gold you don\'t have...'.format(giver_id, recipient_id)


# checks if the bet amount is greater than the amount of current gold
async def bet_is_enough(member_id, bet_amount, server_id):
    current_currency_amt = await get_currency_amount(member_id, server_id)
    return current_currency_amt >= bet_amount


# gives user daily gold
# returns a messagae with the new currency amount
async def daily_gold(member_id, server_id):
    daily_amt = 125
    hour_in_secs = 60.0 * 60.0
    last_daily_recieved_time = await casinodb.db_get_last_blessing_time(member_id, server_id)
    next_available_time = last_daily_recieved_time + hour_in_secs
    time_remaining = next_available_time - time.time()
    time_remaining_min = int(time_remaining // 60)
    time_remaining_sec = int(time_remaining % 60)

    if last_daily_recieved_time == -1 or time_remaining < 0:
        new_currency_amt = await update_currency(member_id, daily_amt, server_id)
        message = ':money_mouth: The casino gods have awarded you with 125 gold!! Your new balance is {0} gold :money_mouth:'.format(new_currency_amt)
        await casinodb.db_set_new_blessing_time(member_id, server_id)
    else:
        message = 'The gods don\'t feel like blessing you right now... Try again in {0} minutes and {1} seconds.'.format(time_remaining_min, time_remaining_sec)
    return message


# returns a list of the top 5 users with the most gold
async def get_top_five(server_id):
    members = await casinodb.db_get_server_members(server_id)
    get_count = itemgetter(2)
    sorted_list = sorted(members, key=get_count, reverse=True)
    num_members = len(members)
    if num_members < 5:
        top_five = sorted_list[0:num_members]
    else:
        top_five = sorted_list[0:5]
    return top_five


# formats the top 5 list
async def top_five_to_string(server_id, client):
    top_five = await get_top_five(server_id)
    if len(top_five) > 0:
        message = 'Here are the **top '+ str(len(top_five)) + '** users!' \
                  '```diff'
        for i in range(len(top_five)):
            uid = top_five[i][0]
            name = await discord.Client.get_user_info(self=client, user_id=uid)
            message += '\n-{0}. {1} - {2} gold'.format(i+1, name, top_five[i][2])
        return message + '```'
    else:
        return ':worried: No one has any gold! Use **$blessing** to get some! :moneybag:'
