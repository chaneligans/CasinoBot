import discord
from tempfile import NamedTemporaryFile
import CasinoBotToken
import random
import csv
import shutil

client = discord.Client()
global prefix
prefix = '$'


# this function responds to users based on the command (if the command exists)
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # says hello
    if message.content.startswith(prefix + 'hello'):
        msg = 'Hello {0.author.mention} :wave:!'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(prefix + 'id'):
        await client.send_message(message.channel, message.author.id)

    # get user currency amount
    if message.content.startswith(prefix + 'bank'):
        currency_amt = await get_currency_amount(message.author.id)
        msg = '{0.author.mention}, you have {1} gold.'.format(message, currency_amt)
        await client.send_message(message.channel, msg)

    # god given gold
    if message.content.startswith(prefix + 'godgold'):
        print(message.mentions)
        recipient_id = message.mentions[0].id
        await give_gold(message.channel, message.author.id, recipient_id, int(message.content.split()[2]))


    # coin flip
    if message.content.startswith(prefix + 'flip'):
        guess = message.content.split()[1]
        await coin_flip(message.channel, guess)



# prints to the console when the bot is live!
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# adds a new user into the members.csv file with 0 gold
# returns the new row in a list
async def add_new_user_info(member_id):
    with open('members.csv', 'a') as members_file:
        fieldnames = ['member_id', 'currency_amt', 'is_admin']
        writer = csv.DictWriter(members_file, fieldnames=fieldnames)
        writer.writerow({'member_id': member_id, 'currency_amt': 0, 'is_admin': False})
    return [member_id, 0, False]


# finds a user in the members.csv file using their id
# returns user information as a list [member_id, currency_amt] if found
# returns 0 otherwise
async def get_user_csv_info(member_id):
    file_name = 'members.csv'
    first_line = True
    found_user = 0
    for line in open(file_name):
        if first_line:
            first_line = False
            continue
        split_line = line.split(',')
        if split_line[0] == member_id:
            found_user = split_line
            print('found!', split_line)
    if found_user == 0:
        found_user = await add_new_user_info(member_id)
    return found_user


#checks if user is an admin
async def is_admin(member_id):
    member_info = await get_user_csv_info(member_id)
    return member_info[2]


# returns the amount of gold a user has
async def get_currency_amount(member_id):
    currency_amount = await get_user_csv_info(member_id)
    currency_amount = currency_amount[1]
    return currency_amount


# updates the user's currency amount
# returns new currency
async def update_currency(member_id, amount):
    old_currency_amount = await get_currency_amount(member_id)
    new_currency_amount = int(old_currency_amount) + amount
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
async def give_gold(channel, giver_id, recipient_id, amount):
    if await is_admin(giver_id):
        await update_currency(recipient_id, amount)
        await client.send_message(channel, 'God just gave <@!{0}> {1} gold!!'.format((await client.get_user_info(recipient_id)).id, amount))
    else:
        await client.send_message(channel, 'You do not have the gold giving privilege!')


# coin flip game
async def coin_flip(channel, guess):
    msg_win = 'You win:bangbang: :tada:'
    msg_lose = 'You lose:bangbang: :sob:'
    guess_correct = False
    coin_num = random.randint(1, 2)

    if guess != 'heads' and guess != 'tails':
        await client.send_message(channel, 'Invalid input, try again! :anger:')
        return

    if coin_num == 1:
        await client.send_message(channel, 'The coin landed on heads!')
        if guess == 'heads':
            guess_correct = True
    elif coin_num == 2:
        await client.send_message(channel, 'The coin landed on tails!')
        if guess == 'tails':
            guess_correct = True

    if guess_correct == True:
        await client.send_message(channel, msg_win)
    else:
        await client.send_message(channel, msg_lose)





client.run(CasinoBotToken.get_token())
