import pandas as pd
import datetime
import iroha_config

# users pool
pool = {}

# load all databases. First load the trip database
trip = pd.read_csv("cBSMD_data.csv")
# set an index to make faster lookups
trip_data = trip.set_index('trip_id')
# convert time to string for easy management
trip_data['end_time'] = trip_data['end_time'].astype(str)
# load the keys for users in domain carbontaxes
tax_users = pd.read_csv('user_private_keys_carbontaxes.csv')
tax_users_data = tax_users.set_index('user_id')
# load the keys for users in domain carbonpayments
payment_users = pd.read_csv('user_private_keys_carbonpayments.csv')
payment_users_data = payment_users.set_index('user_id')

# Enter pool if byt
# 8am: <20% have consume. 8am in seconds are from second 28800 to second 46800
# 1pm: <40% have consume. 1pm in seconds are from second 46800 to second 64800
# 6pm: <80% have consume. 6pm in seconds are from second 64800 to second 86400


# pay carbon taxes for each trip
def pay_carbon_tax_and_register_trip(user_identification, tokens_exp):
    tokens_wallet = tax_users_data.loc[user_identification, 'carbon_tax']
    tax_users_data.at[user_identification, 'carbon_tax'] = round(tokens_wallet - tokens_exp, 2)


# register trip no payment need it
def register_trip():
    new_trip = 'new trip'


# buy tokes from pool or government
def buy_tokens(user_identification, tokens_exp):
    # get current balance of users
    user_balance = tax_users_data.loc[user_id, :]
    tokens_wallet = user_balance['carbon_tax']
    tokens_from_pool = user_balance['tokens_from_pool']
    tokens_from_government = user_balance['tokens_from_government']
    users_in_pool = len(pool)

    # buy tokens if the balance is negative
    if tokens_wallet - tokens_exp < 0:
        # how many tokens does the user needs
        tokens_to_buy = abs(tokens_wallet - tokens_exp)
        # print(tokens_to_buy)

        # if pool is empty then user will take tokens from government
        if len(pool) == 0:
            tax_users_data.at[user_identification, 'tokens_from_government'] = round(tokens_from_government + tokens_to_buy, 2)
            tax_users_data.at[user_identification, 'carbon_tax'] = round(tokens_wallet + tokens_to_buy, 2)
            # print('taken from government: ', users_in_pool, tokens_to_buy)
        else:
            # tokens taken from the each user in the pool
            token_from_each_user = round(tokens_to_buy / users_in_pool, 2)
            # print('taken from each user of pool: ', users_in_pool, token_from_each_user, tokens_to_buy)
            for swimmers in pool:
                # subtract tokens from each user in pool
                token_swimmers = tax_users_data.at[swimmers, 'carbon_tax']
                current_tokens = tax_users_data.at[user_identification, 'carbon_tax']
                current_tokens_from_pool = tax_users_data.at[user_identification, 'tokens_from_pool']
                tax_users_data.at[swimmers, 'carbon_tax'] = round(token_swimmers - token_from_each_user, 2)
                tax_users_data.at[user_identification, 'carbon_tax'] = round(current_tokens + token_from_each_user, 2)
                tax_users_data.at[user_identification, 'tokens_from_pool'] = round(current_tokens_from_pool + token_from_each_user, 2)

                # para mañana si el integrante del pool no tiene los tokens suficinetes no se le quitan y el resto lo
                # tinene que comprar usuario que necesita tokens.

                # Ver que existen usuarios que quedan debiendo tokens al final de dia. Examina los casos

            
        # pool_lengt


# decide when a node enters, exit o do not enter the pool
def in_or_out_of_pool(user_identification, tokens_exp, second_current):
    # get current balance of the user
    tokens_wallet = tax_users_data.loc[user_identification, 'carbon_tax']
    # tokens_wallet = user_balance['carbon_tax']

    # morning pool
    # print(user_id, tokens_wallet - tokens_exp, second)
    if 0 <= second_current < 46800:
        # user still has 80% of tokens to expend
        if tokens_wallet - tokens_exp >= 0.8 * iroha_config.carbontax_init:
            # print('enter pool: ', user_id)
            pool[user_identification] = user_identification
        else:
            if user_identification in pool:
                # print('exit pool ', user_id)
                del pool[user_identification]
            # else:
                # print('dont_enter pool ', user_id)
    # noon pool
    if 46800 <= second_current < 64800:
        # user still has 60% of tokens to expend
        if tokens_wallet - tokens_exp >= 0.6 * iroha_config.carbontax_init:
            pool[user_identification] = user_identification
        else:
            if user_identification in pool:
                del pool[user_identification]
    # evening pool
    if 64800 <= second_current < 86400:
        # user still has 20% of tokens to expend
        if tokens_wallet - tokens_exp >= 0.2 * iroha_config.carbontax_init:
            pool[user_identification] = user_identification
        else:
            if user_id in pool:
                del pool[user_identification]
    # print(len(pool))





# loop every second
start_of_day = datetime.datetime(2019, 9, 24, 00, 00, 00)
print('Simulation starts')
# add all users to the pool
# load the database
# data = pd.read_csv("cBSMD_data.csv")
# different_users = data.drop_duplicates('user_id')
# for index, user in different_users.iterrows():
#     pool[user['user_id']] = user['user_id']

# Seconds in a day 86400
# example of three trip in a second 36270, 36275
for second in range(86400):
    print(second)
    current_time_date = start_of_day + datetime.timedelta(0,second)
    current_time = current_time_date.time().strftime('%H:%M:%S')
    # print(current_time)
    # get rows in panda for current time
    trips = trip_data.loc[trip_data['end_time'] == str(current_time)]
    # only count the seconds where a trip end
    if not trips.empty:
        # print(trips)
        # loop all trips in the second
        for num_rows, trip in trips.iterrows():
            # user_id, start_time, end_time, trip_id, mode_prime, tokens
            user_id = trip['user_id']
            start_time = trip['start_time']
            end_time = trip['end_time']
            mode_prime = trip['mode_prime']
            tokens_trip = trip['tokens']

            # check if user can enter the pool given the amount of tokens he has left considering the current trip
            in_or_out_of_pool(user_id, tokens_trip, second)

            # buy tokens only if need it
            buy_tokens(user_id, tokens_trip)

            # pay trip, i.e., remove coins from carbontaxes
            if tokens_trip != 0:
                pay_carbon_tax_and_register_trip(user_id, tokens_trip)
            else:
                register_trip()

            # get balance of users after all transactions
            user_balance = tax_users_data.loc[user_id, : ]
            tokens_total = user_balance['carbon_tax']
            tokens_bought_from_pool = user_balance['tokens_from_pool']
            tokens_bought_from_government = user_balance['tokens_from_government']
            # print(mode_prime, tokens_trip, tokens_total, tokens_bought_from_pool, tokens_bought_from_government)

tax_users_data.to_csv('results', sep=',', encoding='utf-8')

