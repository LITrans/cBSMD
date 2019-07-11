import pandas as pd
import datetime
import iroha_config
import time

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


# pay carbon taxes for each trip
def pay_carbon_tax_and_register_trip(user_identification, tokens_exp):
    tokens_wallet = tax_users_data.loc[user_identification, 'tokens_left']
    tax_users_data.at[user_identification, 'tokens_left'] = round(tokens_wallet - tokens_exp, 2)


# register trip no payment need it
def register_trip():
    new_trip = 'new trip'


# buy tokes from pool or government
def buy_tokens(user_identification, tokens_exp):
    # get current balance of users
    user_balance = tax_users_data.loc[user_identification, :]
    tokens_wallet_user = user_balance['tokens_left']

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
            # print('taken from government: ', users_in_pool, tokens_to_buy)
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

                # if the user do not have enoguh tokens the he exit the pool
                if token_swimmer - token_each_user <= 0:
                    del pool[swimmer]
                else:
                    # remove the tokes from the swimmer wallet
                    tax_users_data.at[swimmer, 'tokens_left'] = round(token_swimmer - token_each_user, 2)
                    # add the tokes to the other swimmer wallet where he can save money for buying stuff
                    tax_users_data.at[swimmer, 'tokens_sold'] = round(token_swimmer_sold + token_each_user, 2)
                    # add the tokens the swimmer earns by the transaction

                    tax_users_data.at[user_identification, 'tokens_left'] = round(current_tokens_wallet_user +
                                                                                  token_each_user, 2)
                    tax_users_data.at[user_identification, 'tokens_bought_from_pool'] = round(current_tokens_pool_user +
                                                                                              token_each_user, 2)
                    tokens_sell = tokens_sell + token_each_user

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


# decide when a node enters, exit o do not enter the pool
def in_or_out_of_pool(user_identification, tokens_exp, second_current):
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
        if 0 <= second_current < 18000:
            # print('morning pool')
            # user still has 80% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.8 * iroha_config.CARBON_TAX_INIT:
                # print('enter pool: ', user_id)
                pool[user_identification] = user_identification
            else:
                if user_identification in pool:
                    # print('exit pool ', user_id)
                    del pool[user_identification]
                # else:
                    # print('dont_enter pool ', user_id)
        # noon pool from 13 to 18
        if 18000 <= second_current < 36000:
            # print('noon pool')
            # user still has 60% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.6 * iroha_config.CARBON_TAX_INIT:
                pool[user_identification] = user_identification
            else:
                if user_identification in pool:
                    del pool[user_identification]
        # evening pool from 18 to 24
        if 36000 <= second_current < 57600:
            # print('evening/next day pool')
            # user still has 20% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.2 * iroha_config.CARBON_TAX_INIT:
                pool[user_identification] = user_identification
            else:
                if user_id in pool:
                    del pool[user_identification]
        # midnight pool from 24 to 8(next day)
        if 57600 <= second_current < iroha_config.LENGTH:
            # print('evening/next day pool')
            # user still has 20% of tokens to expend
            if tokens_wallet - tokens_exp >= 0.1 * iroha_config.CARBON_TAX_INIT:
                pool[user_identification] = user_identification
            else:
                if user_id in pool:
                    del pool[user_identification]


# loop every second
start_of_day = iroha_config.SIMULATION_STARTS_AT
print('Simulation starts')
start = time.time()
for second in range(iroha_config.LENGTH):
    current_time_date = start_of_day + datetime.timedelta(0,second)
    current_time = current_time_date.time().strftime('%H:%M:%S')

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
            # # get balance of users after all transactions
            # balance = tax_users_data.loc[user_id, : ]
            # tokens_total = balance['tokens_left']
            # tokens_bought_from_pool = balance['tokens_bought_from_pool']
            # tokens_bought_from_government = balance['tokens_bought_from_government']
            # tokens_sold = balance['tokens_sold']
            # print(mode_prime, tokens_trip, tokens_total, tokens_bought_from_pool, tokens_bought_from_government,
            #       tokens_sold)

tax_users_data.to_csv('results (4 slot pool).csv', sep=',', encoding='utf-8')
elapsed_time = time.time() - start
print('Simulation ends in: ', elapsed_time / 60, ' minutes')

