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
socio = pd.read_csv("TTS2016PersonFile_id.csv")
hh = pd.read_csv("houshold.csv")
# set an index to make faster lookups
trip_data = trip.set_index('trip_id')
socio_data = socio.set_index('id')
hh_data = hh.set_index('hhld_num')
# convert time to string for easy management
trip_data['end_time'] = trip_data['end_time'].astype(str)
# get all users in an array
different_users = trip_data.drop_duplicates('user_id')
users = []
for index, user in different_users.iterrows():
    users.append(user['user_id'])

CARBON_TAX_INIT = 493.79


# pay carbon taxes for each trip
def pay_carbon_tax_and_register_trip(user_identification, tokens_exp, total_trips, trips_start, trip_ends, used_modes):
    user_balance = tax_users_data.loc[user_identification, :]
    tokens_wallet = user_balance['tokens_left']
    tokens_pay = user_balance['tokens_pay_for_trips']
    trip_prev = user_balance['total_trips']
    t_start = user_balance['trips_start']
    t_end = user_balance['trip_ends']
    m = user_balance['used_modes']
    hh_id = user_identification // 10
    tax_users_data.at[user_identification, 'tokens_left'] = round(tokens_wallet - tokens_exp, 2)
    tax_users_data.at[user_identification, 'tokens_pay_for_trips'] = round(tokens_pay + tokens_exp, 2)
    if trip_prev == 0:
        tax_users_data.at[user_identification, 'total_trips'] = total_trips
        tax_users_data.at[user_identification, 'trips_start'] = str(trips_start)
        tax_users_data.at[user_identification, 'trip_ends'] = str(trip_ends)
        tax_users_data.at[user_identification, 'used_modes'] = str(used_modes)
        # , , , , , , , , , , , , , , , , , , id
        # check if key is in file
        try:
            tax_users_data.at[user_identification, 'age'] = socio_data.at[user_identification, 'age']
            tax_users_data.at[user_identification, 'sex'] = socio_data.at[user_identification, 'sex']
            tax_users_data.at[user_identification, 'driver_lic'] = socio_data.at[user_identification, 'driver_lic']
            tax_users_data.at[user_identification, 'tran_pass'] = socio_data.at[user_identification, 'tran_pass']
            tax_users_data.at[user_identification, 'emp_stat'] = socio_data.at[user_identification, 'emp_stat']
            tax_users_data.at[user_identification, 'occupation'] = socio_data.at[user_identification, 'occupation']
            tax_users_data.at[user_identification, 'no_work'] = socio_data.at[user_identification, 'no_work']
            tax_users_data.at[user_identification, 'stu_stat'] = socio_data.at[user_identification, 'stu_stat']
            tax_users_data.at[user_identification, 'region_emp'] = socio_data.at[user_identification, 'region_emp']
            tax_users_data.at[user_identification, 'pd_emp'] = socio_data.at[user_identification, 'pd_emp']
            tax_users_data.at[user_identification, 'gta06_emp'] = socio_data.at[user_identification, 'gta06_emp']
            tax_users_data.at[user_identification, 'gtyp_emp'] = socio_data.at[user_identification, 'gtyp_emp']
            tax_users_data.at[user_identification, 'free_park'] = socio_data.at[user_identification, 'free_park']
            tax_users_data.at[user_identification, 'region_sch'] = socio_data.at[user_identification, 'region_sch']
            tax_users_data.at[user_identification, 'pd_sch'] = socio_data.at[user_identification, 'pd_sch']
            tax_users_data.at[user_identification, 'gta06_sch'] = socio_data.at[user_identification, 'gta06_sch']
            tax_users_data.at[user_identification, 'gtyp_sch'] = socio_data.at[user_identification, 'gtyp_sch']
            tax_users_data.at[user_identification, 'n_pers_tri'] = socio_data.at[user_identification, 'n_pers_tri']
            tax_users_data.at[user_identification, 'n_tran_tri'] = socio_data.at[user_identification, 'n_tran_tri']
            tax_users_data.at[user_identification, 'expf'] = socio_data.at[user_identification, 'expf']
            # house hold data
            tax_users_data.at[user_identification, 'hhld_id'] = hh_id
            tax_users_data.at[user_identification, 'region_hhl'] = hh_data.at[hh_id, 'region_hhl']
            tax_users_data.at[user_identification, 'pd_hhld'] = hh_data.at[hh_id, 'pd_hhld']
            tax_users_data.at[user_identification, 'gta06_hhld'] = hh_data.at[hh_id, 'gta06_hhld']
            tax_users_data.at[user_identification, 'gtyp_hhld'] = hh_data.at[hh_id, 'gtyp_hhld']
            tax_users_data.at[user_identification, 'dwell_type'] = hh_data.at[hh_id, 'dwell_type']
            tax_users_data.at[user_identification, 'trip_week'] = hh_data.at[hh_id, 'trip_week']
            tax_users_data.at[user_identification, 'trip_day'] = hh_data.at[hh_id, 'trip_day']
            tax_users_data.at[user_identification, 'n_person'] = hh_data.at[hh_id, 'n_person']
            tax_users_data.at[user_identification, 'n_vehicle'] = hh_data.at[hh_id, 'n_vehicle']
            tax_users_data.at[user_identification, 'n_licence'] = hh_data.at[hh_id, 'n_licence']
            tax_users_data.at[user_identification, 'n_emp_ft'] = hh_data.at[hh_id, 'n_emp_ft']
            tax_users_data.at[user_identification, 'n_emp_pt'] = hh_data.at[hh_id, 'n_emp_pt']
            tax_users_data.at[user_identification, 'n_emp_home'] = hh_data.at[hh_id, 'n_emp_home']
            tax_users_data.at[user_identification, 'n_student'] = hh_data.at[hh_id, 'n_student']
            tax_users_data.at[user_identification, 'n_hhld_tri'] = hh_data.at[hh_id, 'n_hhld_tri']
            tax_users_data.at[user_identification, 'hhld_expf'] = hh_data.at[hh_id, 'expf']
        except:
            tripetr = 0


    else:
        tax_users_data.at[user_identification, 'total_trips'] = total_trips + trip_prev
        tax_users_data.at[user_identification, 'trips_start'] = str(t_start) + ';' + str(trips_start)
        tax_users_data.at[user_identification, 'trip_ends'] = str(t_end) + ';' + str(trip_ends)
        tax_users_data.at[user_identification, 'used_modes'] = str(m) + ';' + str(used_modes)


# register trip no payment need it
def register_trip():
    new_trip = 'new trip'


# ############################################3
# ############################################3
# ############################################3
# SIMULATION
# #############################################3
# #############################################3
token_variation = [0.9, 0.95, 1, 1.05, 1.10]
# token_variation = [1]
for token_per in token_variation:
    CARBON_TAX_INIT = round(493.79 * token_per, 2)
    # create a dictionary to get all users private keys and create users in the domain_carbon_tax
    with open('user_carbon_taxes.csv', mode='w') as user_carbon_tax:
        user_carbon_tax_writer = csv.writer(user_carbon_tax, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        user_carbon_tax_writer.writerow(["user_id", "initial_tokens", "tokens_left", "tokens_pay_for_trips",
                                         "total_trips", "trips_start", "trip_ends", "used_modes", 'age', 'sex',
                                         'driver_lic', 'tran_pass', 'emp_stat', 'occupation', 'no_work', 'stu_stat',
                                         'region_emp', 'pd_emp', 'gta06_emp', 'gtyp_emp', 'free_park', 'region_sch',
                                         'pd_sch', 'gta06_sch', 'gtyp_sch', 'n_pers_tri', 'n_tran_tri', 'expf',
                                         'hhld_id', 'region_hhl', 'pd_hhld', 'gta06_hhld', 'gtyp_hhld',
                                         'dwell_type', 'trip_week', 'trip_day', 'n_person', 'n_vehicle', 'n_licence',
                                         'n_emp_ft', 'n_emp_pt', 'n_emp_home', 'n_student', 'n_hhld_tri', 'hhld_expf'])
        for index, user in enumerate(users):
            user_carbon_tax_writer.writerow([user, CARBON_TAX_INIT, CARBON_TAX_INIT, 0.0, 0.0, '-', '-', '-', '-', '-',
                                             '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                                             '-', '-', '-',
                                             '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                                             '-', '-', '-', '-', '-'])

    # load the keys for users in domain carbon_taxes
    tax_users = pd.read_csv('user_carbon_taxes.csv')
    tax_users_data = tax_users.set_index('user_id')

    print(token_per)
    simulation_statistics = pd.DataFrame(columns=['time', 'tokens trip tx', 'trip tx', 'total tx'])
    start_of_day = iroha_config.SIMULATION_STARTS_AT
    print('Simulation starts')
    start = time.time()

    for second in range(iroha_config.LENGTH):
    # for second in range(1000):
        current_time_date = start_of_day + datetime.timedelta(0, second)
        current_time = current_time_date.time().strftime('%H:%M:%S')
        if second % 3600 == 0:
            elapsed_time = time.time() - start
            print(current_time, "Elapsed time:", round(elapsed_time / 60, 2), 'minutes')

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

                # pay trip, i.e., remove coins from carbontaxes
                pay_carbon_tax_and_register_trip(user_id, tokens_trip, 1, start_time, end_time, mode_prime)
                trip_tx_sec = trip_tx_sec + 1
        if len(trips) != 0:
            simulation_statistics = simulation_statistics.append({'time': current_time,
                                                                  'tokens trip tx': trip_tx_sec,
                                                                  'trip tx': len(trips),
                                                                  'total tx': trip_tx_sec + len(trips)
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

