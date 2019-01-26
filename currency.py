import member_csv_info
from tempfile import NamedTemporaryFile
import csv
import shutil


# returns the amount of gold a user has
async def get_currency_amount(member_id):
    currency_amount = await member_csv_info.get_user_csv_info(member_id)
    currency_amount = int(currency_amount[1])
    return currency_amount


# updates the user's currency amount
# returns new currency
async def update_currency(member_id, amount):
    old_currency_amount = await get_currency_amount(member_id)
    new_currency_amount = old_currency_amount + int(amount)
    if new_currency_amount < 0:
        new_currency_amount = 0

    file_name = 'members.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['member_id', 'currency_amt', 'is_admin']

    with open(file_name, 'r+') as members_file, tempfile:
        reader = csv.DictReader(members_file, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        for row in reader:
            if row['member_id'] == member_id:
                print('updating row', row['member_id'])
                row['member_id'], row['currency_amt'], row['is_admin'] = member_id, new_currency_amount, row['is_admin']
            row = {'member_id': row['member_id'], 'currency_amt': row['currency_amt'], 'is_admin': row['is_admin']}
            writer.writerow(row)
    shutil.move(tempfile.name, file_name)
    return new_currency_amount


# gives a user gold (not from the giver's bank) if the giver is an admin
async def give_gold(giver_id, recipient_id, amount):
    if await member_csv_info.is_admin(giver_id):
        new_amt = await update_currency(recipient_id, amount)
        return ':angel: God just gave <@!{0}> {1} gold!! New balance: {2} gold :money_mouth: :money_mouth:'.format(recipient_id, amount, new_amt)
    else:
        return 'You do not have the gold giving privilege!'


# checks if the bet amount is greater than the amount of current gold
async def bet_is_enough(member_id, bet_amount):
    current_currency_amt = await get_currency_amount(member_id)
    return current_currency_amt >= bet_amount


# gives user daily gold
# returns a messagae with the new currency amount
async def daily_gold(member_id):
    daily_amt = 125
    new_currency_amt = await update_currency(member_id, daily_amt)
    message = ':money_mouth: The casino gods have awarded you with 125 gold!! Your new balance is {0} gold :money_mouth:'.format(new_currency_amt)
    return message
