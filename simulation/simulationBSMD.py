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
# load the keys for users in domain carbon taxes
tax_users = pd.read_csv('user_private_keys_carbon_taxes.csv')
tax_users_data = tax_users.set_index('user_id')
# load the keys for users in domain carbon payments
payment_users = pd.read_csv('user_private_keys_carbon_payments.csv')
payment_users_data = payment_users.set_index('user_id')


# pay carbon taxes for each trip
def pay_carbon_tax_and_register_trip(user_identification, trip_user):
    user_pk = tax_users_data.loc[user_identification, 'private_key']
    t_id = trip_user['trip_id']
    s_time = trip_user['start_time']
    e_time = trip_user['end_time']
    m_prime = trip_user['mode_prime']
    t_trip = trip_user['tokens']

    iroha_functions.transfer_assets(iroha_config.DOMAIN_CARBON_TAX, user_identification, user_pk, 'government',
                                    iroha_config.ASSET_CARBON_TAX, t_trip)

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
    iroha_functions.set_detail(iroha_config.DOMAIN_CARBON_TAX, user_identification, user_pk, t_id, json_trip)


start_of_day = iroha_config.SIMULATION_STARTS_AT
print('Simulation starts')
start = time.time()
for second in range(iroha_config.LENGTH):
    current_time_date = start_of_day + datetime.timedelta(0, second)
    current_time = current_time_date.time().strftime('%H:%M:%S')
    if second % 3600 == 0:
        elapsed_time = time.time() - start
        print(current_time, "Elapsed time:", round(elapsed_time / 60, 2), 'minutes')

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

            # pay trip, i.e., remove coins from carbontaxes
            pay_carbon_tax_and_register_trip(user_id, trip)

elapsed_time = time.time() - start
print('Simulation ends in: ', round(elapsed_time / 60, 2), ' minutes')

