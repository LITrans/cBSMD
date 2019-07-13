import pandas as pd
# import modin.pandas as pd
import datetime
import iroha_config
import time
import iroha_functions
import json

# users pool
pool = {}
# if a user make a trip and didn't make it to the pool is possible he can enter the pool in the next slot
pool_eligible = {}

# load all databases. First load the trip database
trip_data = pd.read_csv("cBSMD_data.csv")
# convert time to string for easy management
trip_data['end_time'] = trip_data['end_time'].astype(str)
# load the keys for users in domain carbontaxes
tax_users = pd.read_csv('user_private_keys_carbontaxes.csv')
tax_users_data = tax_users.set_index('user_id')
# load the keys for users in domain carbonpayments
payment_users = pd.read_csv('user_private_keys_carbonpayments.csv')
payment_users_data = payment_users.set_index('user_id')


# pay carbon taxes for each trip
def pay_carbon_tax_and_register_trip(user_identification, trip_user):
    user_pk = tax_users_data.loc[user_identification, 'private_key']
    t_id = trip_user['trip_id']
    s_time = trip_user['start_time']
    e_time = trip_user['end_time']
    m_prime = trip_user['mode_prime']
    t_trip = trip_user['tokens']

    iroha_functions.transfer_assets(iroha_config.domain_carbon_tax, user_identification, user_pk, 'government',
                                    iroha_config.asset_carbon_tax, t_trip)

    transaction_data = dict()
    transaction_data['start'] = s_time
    transaction_data['end'] = e_time
    transaction_data['mode'] = m_prime
    transaction_data['tokens'] = t_trip
    transaction_data['trip porpoise'] = 'leisure'
    transaction_data['creator'] = user_identification
    j = json.dumps(transaction_data)
    j_in_ledger = str(j)
    json_trip = j_in_ledger.replace('"', '')
    iroha_functions.set_detail(iroha_config.domain_carbon_tax, user_identification, user_pk, t_id, json_trip)


# register trip no payment need it
def register_trip(user_identification, trip_user):
    user_pk = tax_users_data.loc[user_identification, 'private_key']
    t_id = trip_user['trip_id']
    s_time = trip_user['start_time']
    e_time = trip_user['end_time']
    m_prime = trip_user['mode_prime']
    t_trip = trip_user['tokens']

    transaction_data = dict()
    transaction_data['start'] = s_time
    transaction_data['end'] = e_time
    transaction_data['mode'] = m_prime
    transaction_data['tokens'] = t_trip
    transaction_data['trip porpoise'] = 'leisure'
    transaction_data['creator'] = user_identification
    j = json.dumps(transaction_data)
    j_in_ledger = str(j)
    json_trip = j_in_ledger.replace('"', '')
    iroha_functions.set_detail(iroha_config.domain_carbon_tax, user_identification, user_pk, t_id, json_trip)


# buy tokes from pool or government
def buy_tokens(user_identification, tokens_exp):
    # get current balance of users
    user_pk = tax_users_data.loc[user_identification, 'private_key']
    tokens_wallet_user = iroha_functions.get_balance(iroha_config.domain_carbon_tax, user_identification, user_pk)

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
            # user buy tokens from government. First user send coins to government
            user_pk_payments = payment_users_data.loc[user_identification, 'private_key']
            iroha_functions.transfer_assets(iroha_config.domain_carbon_payments, user_identification, user_pk_payments,
                                            'government', tokens_buy, 'coins for tokens')
            # then the user receive tokens from government
            iroha_functions.transfer_assets(iroha_config.domain_carbon_tax, 'government', iroha_config.government_pk,
                                            user_identification, iroha_config.asset_carbon_tax, tokens_buy,
                                            'tokens for coins')
        else:
            # tokens taken from the each user in the pool
            token_each_user = round(tokens_buy / users_in_pool, 2)
            # print('taken from each user of pool: ', users_in_pool, token_from_each_user, tokens_to_buy)
            for swimmer in list(pool):
                # get the balance from each swimmer
                swimmer_pk = tax_users_data.loc[swimmer_pk, 'private_key']
                token_swimmer = iroha_functions.get_balance(iroha_config.domain_carbon_tax, swimmer, swimmer_pk)

                # Users with enough tokens will share all his corresponding part
                if token_swimmer - token_each_user >= 0:
                    # swimmer send tokens to user
                    iroha_functions.transfer_assets(iroha_config.domain_carbon_tax, swimmer, swimmer_pk,
                                                    user_identification, iroha_config.asset_carbon_tax, token_each_user,
                                                    'token from pool')
                    tokens_sell = tokens_sell + token_each_user
                    # if swimmer ran out of tokens he exits the pool
                    if round(token_swimmer - token_each_user, 2) == 0:
                        del pool[swimmer]
                # Users with not enough tokens will share as much as they can
                else:
                    iroha_functions.transfer_assets(iroha_config.domain_carbon_tax, swimmer, swimmer_pk,
                                                    user_identification, iroha_config.asset_carbon_tax, token_swimmer,
                                                    'token from pool')
                    tokens_sell = tokens_sell + token_swimmer
                    # swimmer ran out of tokes so he exit the pool
                    del pool[swimmer]

            # if the user does not collect enough tokens from the pool he will have to buy
            # the remaining tokens from the government
            if tokens_sell < tokens_buy:
                buy_token_government = abs(tokens_sell - tokens_buy)
                # user buy tokens from government. First user send coins to government
                user_pk_payments = payment_users_data.loc[user_identification, 'private_key']
                iroha_functions.transfer_assets(iroha_config.domain_carbon_payments, user_identification,
                                                user_pk_payments, 'government', buy_token_government,
                                                'coins for tokens')
                # then the user receive tokens from government
                iroha_functions.transfer_assets(iroha_config.domain_carbon_tax, 'government',
                                                iroha_config.government_pk, user_identification,
                                                iroha_config.asset_carbon_tax, buy_token_government, 'tokens for coins')


# decide when a node enters, exit o do not enter the pool
def in_or_out_of_pool(user_identification, tokens_exp, current_second):
    # get current balance of the user
    user_pk = tax_users_data.loc[user_identification, 'private_key']
    tokens_wallet = iroha_functions.get_balance(iroha_config.domain_carbon_tax, user_identification, user_pk)

    # Exit pool if tokens_wallet - tokens_exp is negative
    if tokens_wallet - tokens_exp < 0:
        if user_identification in pool:
            del pool[user_identification]
    else:
        # simulation starts at 8am
        # morning pool from 8 to 13
        # print(user_id, tokens_wallet - tokens_exp, second)
        if 0 <= current_second < 18000:
            # print('morning pool')
            # user still has 80% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.8 * iroha_config.CARBON_TAX_INIT:
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
            if tokens_wallet - tokens_exp >= 0.6 * iroha_config.CARBON_TAX_INIT:
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
            if tokens_wallet - tokens_exp >= 0.2 * iroha_config.CARBON_TAX_INIT:
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
            if tokens_wallet - tokens_exp >= 0.1 * iroha_config.CARBON_TAX_INIT:
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
            user_pk = tax_users_data.loc[user_eligible, 'private_key']
            user_tokens_left = iroha_functions.get_balance(iroha_config.domain_carbon_tax, user_eligible, user_pk)
            if user_tokens_left >= 0.6 * iroha_config.CARBON_TAX_INIT:
                pool[user_eligible] = user_eligible
                del pool_eligible[user_eligible]
    # evening slot
    if current_second == 36000:
        for user_eligible in list(pool_eligible):
            user_pk = tax_users_data.loc[user_eligible, 'private_key']
            user_tokens_left = iroha_functions.get_balance(iroha_config.domain_carbon_tax, user_eligible, user_pk)
            if user_tokens_left >= 0.2 * iroha_config.CARBON_TAX_INIT:
                pool[user_eligible] = user_eligible
                del pool_eligible[user_eligible]
    # midnight slot
    if current_second == 57600:
        for user_eligible in list(pool_eligible):
            user_pk = tax_users_data.loc[user_eligible, 'private_key']
            user_tokens_left = iroha_functions.get_balance(iroha_config.domain_carbon_tax, user_eligible, user_pk)
            if user_tokens_left >= 0.1 * iroha_config.CARBON_TAX_INIT:
                pool[user_eligible] = user_eligible
                del pool_eligible[user_eligible]


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

    # get rows in panda for current time
    trips = trip_data.loc[trip_data['end_time'] == str(current_time)]
    # only count the seconds where a trip end
    if not trips.empty:
        # print(trips)
        # loop all trips in the second
        for num_rows, trip in trips.iterrows():
            # user_id, start_time, end_time, trip_id, mode_prime, tokens
            trip_id = trip['trip_id']
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
                pay_carbon_tax_and_register_trip(user_id, tokens_trip, trip)
                trip_tx_sec = trip_tx_sec + 1
            else:
                register_trip(user_id, trip)

elapsed_time = time.time() - start
print('Simulation ends in: ', round(elapsed_time / 60, 2), ' minutes')

