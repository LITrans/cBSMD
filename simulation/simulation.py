import pandas as pd
import datetime
import iroha_config
import time
import csv
import os

# users pool
pool = {}
# if a user make a trip and didn't make it to the pool is possible he can enter the pool in the next slot
pool_eligible = {}

# load all databases. First load the trip database
trip = pd.read_csv("cBSMD_data.csv")
# set an index to make faster lookups
trip_data = trip.set_index('trip_id')
# convert time to string for easy management
trip_data['end_time'] = trip_data['end_time'].astype(str)
# get all users in an array
different_users = trip_data.drop_duplicates('user_id')
users = []
for index, user in different_users.iterrows():
    users.append(user['user_id'])

CARBON_TAX_INIT = 493.79


# pay carbon taxes for each trip
def pay_carbon_tax_and_register_trip(user_identification, tokens_exp):
    user_balance = tax_users_data.loc[user_identification, :]
    tokens_wallet = user_balance['tokens_left']
    tokens_pay = user_balance['tokens_pay_for_trips']
    tax_users_data.at[user_identification, 'tokens_left'] = round(tokens_wallet - tokens_exp, 2)
    tax_users_data.at[user_identification, 'tokens_pay_for_trips'] = round(tokens_pay + tokens_exp, 2)


# register trip no payment need it
def register_trip():
    new_trip = 'new trip'


# buy tokes from pool or government
def buy_tokens(user_identification, tokens_exp):
    # get current balance of users
    user_balance = tax_users_data.loc[user_identification, :]
    tokens_wallet_user = user_balance['tokens_left']
    # counter to get the number of pool token transactions
    pool_transactions = 0
    # counter to get the number of government token transactions
    government_transactions = 0

    users_in_pool = len(pool)

    # buy tokens if the balance is negative
    if tokens_wallet_user - tokens_exp < 0:
        # how many tokens does the user needs
        tokens_buy = abs(tokens_wallet_user - tokens_exp)
        # print(tokens_to_buy)

        # if pool is empty then user will take tokens from government
        if len(pool) == 0:
            tokens_government_user = user_balance['tokens_bought_from_government']
            tax_users_data.at[user_identification, 'tokens_bought_from_government'] = round(tokens_government_user +
                                                                                            tokens_buy, 2)
            tax_users_data.at[user_identification, 'tokens_left'] = round(tokens_wallet_user + tokens_buy, 2)
            government_transactions = government_transactions + 1
        else:
            # tokens taken from the each user in the pool
            token_each_user = round(tokens_buy / users_in_pool, 2)
            # this counter will save the total amount of tokens bought from pool
            tokens_sell = 0
            # print('taken from each user of pool: ', users_in_pool, token_from_each_user, tokens_to_buy)
            for swimmer in list(pool):
                # subtract tokens from each user in pool
                swimmer_balance = tax_users_data.loc[swimmer, :]
                token_swimmer = swimmer_balance['tokens_left']
                token_swimmer_sold = swimmer_balance['tokens_sold']
                current_user_balance = tax_users_data.loc[user_identification, :]
                current_tokens_wallet_user = current_user_balance['tokens_left']
                current_tokens_pool_user = current_user_balance['tokens_bought_from_pool']

                # Users with enough tokens will share all his corresponding part
                if token_swimmer - token_each_user >= 0:
                    # remove the tokes from the swimmer wallet
                    tax_users_data.at[swimmer, 'tokens_left'] = round(token_swimmer - token_each_user, 2)
                    # add the tokes to the other swimmer wallet where he can save money for buying stuff
                    tax_users_data.at[swimmer, 'tokens_sold'] = round(token_swimmer_sold + token_each_user, 2)
                    # add the tokens to the user wallet
                    tax_users_data.at[user_identification, 'tokens_left'] = round(current_tokens_wallet_user +
                                                                                  token_each_user, 2)
                    # count the tokens the user bought from the pool
                    tax_users_data.at[user_identification, 'tokens_bought_from_pool'] = round(current_tokens_pool_user +
                                                                                              token_each_user, 2)
                    tokens_sell = tokens_sell + token_each_user
                    # if the swimmer ran out out tokens in this transaction, he exits the pool
                    if round(token_swimmer - token_each_user, 2) == 0:
                        del pool[swimmer]
                    # count token transactions
                    pool_transactions = pool_transactions + 1
                # Users with not enough tokens will share as much as they can
                else:
                    as_much_tokens = token_swimmer
                    # remove the tokes from the swimmer wallet
                    tax_users_data.at[swimmer, 'tokens_left'] = round(token_swimmer - as_much_tokens, 2)
                    # add the tokes to the other swimmer wallet where he can save money for buying stuff
                    tax_users_data.at[swimmer, 'tokens_sold'] = round(token_swimmer_sold + as_much_tokens, 2)
                    # add the tokens to the user wallet
                    tax_users_data.at[user_identification, 'tokens_left'] = round(current_tokens_wallet_user +
                                                                                  as_much_tokens, 2)
                    # count the tokens the user bought from the pool
                    tax_users_data.at[user_identification, 'tokens_bought_from_pool'] = round(current_tokens_pool_user +
                                                                                              as_much_tokens, 2)
                    tokens_sell = tokens_sell + as_much_tokens
                    # count token transactions
                    pool_transactions = pool_transactions + 1
                    del pool[swimmer]

            # if the user does not collect enough tokens from the pool he will have to buy
            # the remaining tokens from the government
            if tokens_sell < tokens_buy:
                buy_token_government = abs(tokens_sell - tokens_buy)
                current_user_balance = tax_users_data.loc[user_identification, :]
                current_tokens_wallet_user = current_user_balance['tokens_left']
                current_tokens_government_user = current_user_balance['tokens_bought_from_government']
                tax_users_data.at[user_identification, 'tokens_bought_from_government'] = \
                    round(current_tokens_government_user + buy_token_government, 2)
                tax_users_data.at[user_identification, 'tokens_left'] = round(current_tokens_wallet_user +
                                                                              buy_token_government, 2)
                government_transactions = government_transactions + 1

    return pool_transactions, government_transactions


# decide when a node enters, exit o do not enter the pool
def in_or_out_of_pool(user_identification, tokens_exp, current_second):
    # get current balance of the user
    tokens_wallet = tax_users_data.loc[user_identification, 'tokens_left']

    # Exit pool if tokens_wallet - tokens_exp is negative
    if tokens_wallet - tokens_exp < 0:
        if user_identification in pool:
            del pool[user_identification]
    else:
        # simulation starts at 8am
        # morning pool from 8 to 13
        # print(user_id, tokens_wallet - tokens_exp, second)
        if 0 <= current_second < 18000:
            # print(CARBON_TAX_INIT)
            # user still has 80% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.8 * CARBON_TAX_INIT:
                pool[user_identification] = user_identification
            else:
                # if in this slot the user didn't make it to the pool. He is eligible to enter in the next slot since
                # the user already make a trip
                pool_eligible[user_identification] = user_identification
                if user_identification in pool:
                    # print('exit pool ', user_id)
                    del pool[user_identification]

        # noon pool from 13 to 18
        if 18000 <= current_second < 36000:
            # print('noon pool')
            # user still has 60% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.6 * CARBON_TAX_INIT:
                pool[user_identification] = user_identification
            else:
                # if in this slot the user didn't make it to the pool. He is eligible to enter in the next slot since
                # the user already make a trip
                pool_eligible[user_identification] = user_identification
                if user_identification in pool:
                    del pool[user_identification]

        # evening pool from 18 to 8(next day)
        if 36000 <= current_second < 57600:
            # print('evening/next day pool')
            # user still has 20% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.2 * CARBON_TAX_INIT:
                pool[user_identification] = user_identification
            else:
                # if in this slot the user didn't make it to the pool. He is eligible to enter in the next slot since
                # the user already make a trip
                pool_eligible[user_identification] = user_identification
                if user_id in pool:
                    del pool[user_identification]

        # midnight pool from 24 to 8(next day)
        if 57600 <= current_second < iroha_config.LENGTH:
            # print('evening/next day pool')
            # user still has 10% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.1 * CARBON_TAX_INIT:
                pool[user_identification] = user_identification
            else:
                # the last slot does not need a pool_eligible
                if user_id in pool:
                    del pool[user_identification]


# select from the pool_eligible which nodes can enter the pool
def update_pool(current_second):
    # noon slot
    if current_second == 18000:
        for user_eligible in list(pool_eligible):
            user_tokens_left = tax_users_data.at[user_eligible, 'tokens_left']
            if user_tokens_left >= 0.6 * CARBON_TAX_INIT:
                pool[user_eligible] = user_eligible
                del pool_eligible[user_eligible]
    # evening slot
    if current_second == 36000:
        for user_eligible in list(pool_eligible):
            user_tokens_left = tax_users_data.at[user_eligible, 'tokens_left']
            if user_tokens_left >= 0.2 * CARBON_TAX_INIT:
                pool[user_eligible] = user_eligible
                del pool_eligible[user_eligible]
    # midnight slot
    if current_second == 57600:
        for user_eligible in list(pool_eligible):
            user_tokens_left = tax_users_data.at[user_eligible, 'tokens_left']
            if user_tokens_left >= 0.1 * CARBON_TAX_INIT:
                pool[user_eligible] = user_eligible
                del pool_eligible[user_eligible]


# ############################################3
# ############################################3
# ############################################3
# SIMULATION
# #############################################3
# #############################################3
token_variation = [0.9, 0.95, 1, 1.05, 1.10]
for token_per in token_variation:
    CARBON_TAX_INIT = round(493.79 * token_per, 2)
    # create a dictionary to get all users private keys and create users in the domain_carbon_tax
    with open('user_carbon_taxes.csv', mode='w') as user_carbon_tax:
        user_carbon_tax_writer = csv.writer(user_carbon_tax, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        user_carbon_tax_writer.writerow(["user_id", "tokens_left", "tokens_pay_for_trips", "tokens_bought_from_pool",
                                         "tokens_bought_from_government", "tokens_sold"])
        for index, user in enumerate(users):
            user_carbon_tax_writer.writerow([user, CARBON_TAX_INIT, 0.0, 0.0, 0.0, 0.0])

    # load the keys for users in domain carbon_taxes
    tax_users = pd.read_csv('user_carbon_taxes.csv')
    tax_users_data = tax_users.set_index('user_id')

    print(token_per)
    simulation_statistics = pd.DataFrame(columns=['time', 'users in pool', 'users in eligible pool', 'tokens pool tx',
                                                  'tokens government tx', 'tokens trip tx', 'trip tx', 'total tx'])
    start_of_day = iroha_config.SIMULATION_STARTS_AT
    print('Simulation starts')
    start = time.time()

    for second in range(iroha_config.LENGTH):
        current_time_date = start_of_day + datetime.timedelta(0, second)
        current_time = current_time_date.time().strftime('%H:%M:%S')
        if second % 3600 == 0:
            elapsed_time = time.time() - start
            print(current_time, "Elapsed time:", round(elapsed_time / 60, 2), 'minutes')

        # every new slot we look in the eligible pool for users that could enter
        update_pool(second)

        # counter of pool token transactions per second
        pool_tx_sec = 0
        # counter of government token transactions per second
        gov_tx_sec = 0
        # counter of trip token transactions per second
        trip_tx_sec = 0

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
                pool_tx, government_tx = buy_tokens(user_id, tokens_trip)
                pool_tx_sec = pool_tx_sec + pool_tx
                gov_tx_sec = gov_tx_sec + government_tx

                # pay trip, i.e., remove coins from carbontaxes
                if tokens_trip != 0:
                    pay_carbon_tax_and_register_trip(user_id, tokens_trip)
                    trip_tx_sec = trip_tx_sec + 1
                else:
                    register_trip()
        if len(trips) != 0:
            simulation_statistics = simulation_statistics.append({'time': current_time,
                                                                  'users in pool' : len(pool),
                                                                  'users in eligible pool': len(pool_eligible),
                                                                  'tokens pool tx': pool_tx_sec,
                                                                  'tokens government tx': gov_tx_sec,
                                                                  'tokens trip tx': trip_tx_sec,
                                                                  'trip tx': len(trips),
                                                                  'total tx': pool_tx_sec + gov_tx_sec + trip_tx_sec +
                                                                              len(trips)
                                                                  },
                                                                 ignore_index=True)

    # save simulation token statistics
    tax_users_data.to_csv('economics_' + str(token_per) + '_.csv', sep=',', encoding='utf-8')
    # save statistics of the simulation
    simulation_statistics.to_csv('statistics_' + str(token_per) + '_.csv', sep=',', encoding='utf-8')
    elapsed_time = time.time() - start
    print('Simulation ends in: ', round(elapsed_time / 60, 2), ' minutes')
    # users pool
    pool = {}
    # if a user make a trip and didn't make it to the pool is possible he can enter the pool in the next slot
    pool_eligible = {}
    os.remove("user_carbon_taxes.csv")

