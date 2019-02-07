import pymysql
import time
import CasinoBotToken


# open database connection
database = pymysql.connect(host='localhost', user='root', password=CasinoBotToken.get_dbpw(), db='casinodb', autocommit=True)
print("Connected to casinodb")


# checks if a user exists in the database
# if the user is not found, addes the user into the database
async def validate_user(member_id, server_id):
    try:
        cursor = database.cursor()
        sql = 'SELECT userID, serverID FROM user ' \
              'WHERE userID = "{0}" AND serverID = "{1}";'.format(member_id, server_id)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            await insert_new_user(member_id, server_id)
    except Exception as e:
        print("!!! Exception !!! User exists: ", e)


async def insert_new_user(member_id, server_id):
    try:
        cursor = database.cursor()
        sql = "INSERT INTO user " \
              "VALUES ({0}, {1}, 0, -1);".format(member_id, server_id)
        cursor.execute(sql)
        print("Added new user {0} to server {1}".format(member_id, server_id))
    except Exception as e:
        print("!!! Exception !!! Insert new user: ", e)


# returns list of user info from the database
# [0] = user (member) id, [1] = server id, [2] = currency amount, [3] = last daily time (secs)
async def db_get_user_info(member_id, server_id):
    try:
        await validate_user(member_id, server_id)
        cursor = database.cursor()
        sql = 'SELECT * FROM user ' \
              'WHERE userID = "{0}" AND serverID = "{1}";'.format(member_id, server_id)
        cursor.execute(sql)
        result = list(cursor.fetchall())[0]
        return result
    except Exception as e:
        print("!!! Exception !!! Get user info: ", e)


# returns information of every member in a server as a list of tupules
# tupule indices: # [0] = user (member) id, [1] = server id, [2] = currency amount, [3] = last daily time (secs)
async def db_get_server_members(server_id):
    try:
        cursor = database.cursor()
        sql = 'SELECT * FROM user ' \
              'WHERE serverID = {0}'.format(server_id)
        cursor.execute(sql)
        results = list(cursor.fetchall())
        return results
    except Exception as e:
        print("!!! Exception !!! Get server members: ", e)


# returns currency amount
async def db_get_currency_amt(member_id, server_id):
    return (await db_get_user_info(member_id, server_id))[2]


# returns the last blessing time (blessing / daily)
async def db_get_last_blessing_time(member_id, server_id):
    return float((await db_get_user_info(member_id, server_id))[3])


# updates the user's currency
# returns the new currency
async def db_set_currency(member_id, server_id, currency_amt):
    try:
        await validate_user(member_id, server_id)
        print("MID: ", member_id, " SID: ", server_id, " CA: ", currency_amt)
        cursor = database.cursor()
        sql = 'UPDATE user ' \
              'SET currencyAmt = {0} ' \
              'WHERE userID = "{1}" AND serverID = "{2}";'.format(currency_amt, member_id, server_id)
        cursor.execute(sql)
        return await db_get_currency_amt(member_id, server_id)
    except Exception as e:
        print("!!! Exception !!! Set currency: ", e)


# sets the last blessing / daily time in seconds since the epoch
# returns the new blessing / daily time
async def db_set_new_blessing_time(member_id, server_id):
    new_time = time.time()
    try:
        await validate_user(member_id, server_id)
        cursor = database.cursor()
        sql = 'UPDATE user ' \
              'SET lastDailyTime = "{0}" ' \
              'WHERE userID = "{1}" AND serverID = "{2}";'.format(new_time, member_id, server_id)
        cursor.execute(sql)
        return await db_get_last_blessing_time(member_id, server_id)
    except Exception as e:
        print("!!! Exception !!! Set last blessing time: ", e)
