import pandas as pd


# load the database
data = pd.read_csv("cBSMD_data.csv")
# set an index to make faster lookups
data_indexed = data.set_index('trip_id')
# convert time to string for easy management
data_indexed['end_time'] = data_indexed['end_time'].astype(str)



# get all users in an array
different_users = data_indexed.drop_duplicates('user_id')
users = []
for index, user in different_users.iterrows():
    users.append(user['user_id'])
print(users)