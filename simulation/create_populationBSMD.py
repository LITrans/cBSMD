import pandas as pd
import csv
from iroha import IrohaCrypto
import iroha_functions
import iroha_config

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

# The firs step in the creation of the BSMD is to create a domain and asset for the nodes
# The admin node is in charge of do this, hence all transactions need to be signed by him
# Create a domain domain_carbon_tax with an asset
# create_domain_and_asset(domain_id, default_role, asset_name, asset_precision)

# iroha_functions.create_domain_and_asset(iroha_config.domain_carbon_tax, iroha_config.default_role,
#                                         iroha_config.asset_carbon_tax, iroha_config.asset_precision)

# Create a domain domain_carbon_payments with an asset

# iroha_functions.create_domain_and_asset(iroha_config.domain_carbon_payments, iroha_config.default_role,
#                                         iroha_config.asset_carbon_payments, iroha_config.asset_precision)


# create a dictionary to get all users private keys and create users in the domain_carbon_tax
with open('user_private_keys_carbontaxes.csv', mode='w') as user_private_key:
    private_key_writer = csv.writer(user_private_key, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    private_key_writer.writerow(["user_id", "private_key", "tokens_left", "tokens_pay_for_trips",
                                 "tokens_bought_from_pool", "tokens_bought_from_government", "tokens_sold"])
    for index, user in enumerate(users):
        user_private_key = IrohaCrypto.private_key()
        private_key_writer.writerow([user, str(user_private_key), iroha_config.CARBON_TAX_INIT, 0.0, 0.0, 0.0, 0.0])
        user_name = user
        user_public_key = IrohaCrypto.derive_public_key(user_private_key)
        # iroha_functions.create_account_with_assets(iroha_config.domain_carbon_tax, user_name, user_public_key,
        #                                   iroha_config.asset_carbon_tax, iroha_config.carbontax_init)

# create a dictionary to get all users private keys and create users in the domain_carbon_payments
with open('user_private_keys_carbonpayments.csv', mode='w') as user_private_key:
    private_key_writer = csv.writer(user_private_key, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    private_key_writer.writerow(["user_id", "private_key", "carbon_coins"])
    for index, user in enumerate(users):
        user_private_key = IrohaCrypto.private_key()
        private_key_writer.writerow([user, str(user_private_key), iroha_config.CARBON_COIN_INIT])
        user_name = user
        user_public_key = IrohaCrypto.derive_public_key(user_private_key)
        # iroha_functions.create_account(iroha_config.domain_carbon_payments, user_name, user_public_key)

