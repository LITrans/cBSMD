import pandas as pd
import csv
from iroha import IrohaCrypto
import iroha_functions as irofun
import iroha_config as irocon

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

# create a dictionary to get all users private keys and create user in the cBSMD
with open('user_private_key.csv', mode='w') as user_private_key:
    private_key_writer = csv.writer(user_private_key, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for user in users:
        user_private_key = IrohaCrypto.private_key()
        private_key_writer.writerow([user, str(user_private_key)])
        user_name = user
        user_public_key = IrohaCrypto.derive_public_key(user_private_key)
        irofun.create_account_with_assets(irocon.domain_individual, user_name, user_public_key,
                                          irocon.asset_individual,'493.79')

