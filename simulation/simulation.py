import pandas as pd
import datetime

# load the database
data = pd.read_csv("cBSMD_data.csv")
# set an index to make faster lookups
data_indexed = data.set_index('trip_id')
# convert time to string for easy management
data_indexed['end_time'] = data_indexed['end_time'].astype(str)


# loop every second
start_of_day = datetime.datetime(2019, 9, 24, 00, 00, 00)
print('Simulation starts')
# Seconds in a day 86400
# exmple of three trip in a second 36270, 36275
for i in range(86400):
    current_time_date = start_of_day + datetime.timedelta(0,i)
    current_time = current_time_date.time().strftime('%H:%M:%S')
    # print(current_time)
    # get rows in panda for current time
    trips = data_indexed.loc[data_indexed['end_time'] == str(current_time)]
    # only count the seconds where a trip end
    if not trips.empty:
        # print(trips)
        # loop all trips in the second
        for index, trip in trips.iterrows():
            # user_id, start_time, end_time, trip_id, mode_prime, tokens
            user_id = trip['user_id']
            start_time = trip['start_time']
            end_time = trip['end_time']
            mode_prime = trip['mode_prime']
            tokens = trip['tokens']
            print(user_id, start_time, end_time, mode_prime, tokens)


