import csv


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


# checks if user is an admin
async def is_admin(member_id):
    member_info = await get_user_csv_info(member_id)
    return member_info[2]
