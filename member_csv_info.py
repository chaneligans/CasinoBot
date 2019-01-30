import csv
from tempfile import NamedTemporaryFile
import shutil
import time
from pathlib import Path

data_folder = Path('serverdata/')


# tests if the server has a file, creates one if it does not exist
# returns the file name
async def open_file(server_id):
    file_name = data_folder / (server_id + '.csv')
    try:
        with open(file_name) as members_file:
            print('Successfully opened ' + file_name)
    except FileNotFoundError:
        with open(file_name, 'a') as members_file:
            print('Created new file ' + file_name)
            fieldnames = ['member_id', 'currency_amt', 'is_admin', 'last_daily_time']
            writer = csv.DictWriter(members_file, fieldnames=fieldnames)
            writer.writerow({'member_id': 'member_id', 'currency_amt': 'currency_amt', 'is_admin': 'is_admin', 'last_daily_time': 'last_daily_time'})
            print('Added header for ' + file_name)
    finally:
        return file_name

# adds a new user into the members.csv file with 0 gold
# returns the new row in a list
async def add_new_user_info(member_id, server_id):
    file_name = await open_file(server_id)
    with open(file_name, 'a') as members_file:
        fieldnames = ['member_id', 'currency_amt', 'is_admin', 'last_daily_time']
        writer = csv.DictWriter(members_file, fieldnames=fieldnames)
        writer.writerow({'member_id': member_id, 'currency_amt': 0, 'is_admin': False, 'last_daily_time': -1})
    return [member_id, 0, False, -1]


# finds a user in the members.csv file using their id
# returns user information as a list [member_id, currency_amt] if found
# returns 0 otherwise
async def get_user_csv_info(member_id, server_id):
    file_name = await open_file(server_id)
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
        found_user = await add_new_user_info(member_id, server_id)
    return found_user


# returns information of all members in a server
async def get_server_members(server_id):
    file_name = await open_file(server_id)
    first_line = True
    members = []
    for line in open(file_name):
        if first_line:
            first_line = False
            continue
        member = line.strip('\n').split(',')
        if len(member) > 1:
            member_list = [int(member[0]), int(member[1]), member[2], float(member[3])]
            members.append(member_list)
    return members


# returns currency amount
async def get_user_csv_currency_amt(member_id, server_id):
    user = await get_user_csv_info(member_id, server_id)
    currency_amt = int(user[1])
    return currency_amt


# checks if user is an admin
async def is_admin(member_id, server_id):
    user = await get_user_csv_info(member_id, server_id)
    is_admin = user[2]
    print("isadmin: " + is_admin)
    return is_admin


# returns the last daily time
async def get_user_csv_daily_time(member_id, server_id):
    user = await get_user_csv_info(member_id, server_id)
    last_daily_time = float(user[3])
    return last_daily_time


# updates the user's currency amount
# returns new currency
async def set_currency(member_id, amount, server_id):
    old_currency_amount = await get_user_csv_currency_amt(member_id, server_id)
    new_currency_amount = old_currency_amount + int(amount)
    if new_currency_amount < 0:
        new_currency_amount = 0

    file_name = data_folder / (server_id + '.csv')
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['member_id', 'currency_amt', 'is_admin', 'last_daily_time']

    with open(file_name, 'r+') as members_file, tempfile:
        reader = csv.DictReader(members_file, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        for row in reader:
            if row['member_id'] == member_id:
                print('updating row', row['member_id'])
                row['member_id'], row['currency_amt'] = member_id, new_currency_amount
            row = {'member_id': row['member_id'], 'currency_amt': row['currency_amt'], 'is_admin': row['is_admin'], 'last_daily_time': row['last_daily_time']}
            writer.writerow(row)
    shutil.move(tempfile.name, file_name)
    return new_currency_amount


# updates the last time the user recieved their daily gold to the time the function was called
async def set_last_daily_time(member_id, server_id):
    new_time = time.time()
    file_name = data_folder / (server_id + '.csv')
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['member_id', 'currency_amt', 'is_admin', 'last_daily_time']

    with open(file_name, 'r+') as members_file, tempfile:
        reader = csv.DictReader(members_file, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        for row in reader:
            if row['member_id'] == member_id:
                print('updating last daily time for ', row['member_id'])
                row['member_id'], row['currency_amt'], row['is_admin'], row['last_daily_time'] = member_id, row['currency_amt'], row['is_admin'], new_time
            row = {'member_id': row['member_id'], 'currency_amt': row['currency_amt'], 'is_admin': row['is_admin'], 'last_daily_time': row['last_daily_time']}
            writer.writerow(row)
    shutil.move(tempfile.name, file_name)
    return new_time
