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
# create a domain for carbon tax (tokens)
iroha_functions.create_domain_and_asset(iroha_config.DOMAIN_CARBON_TAX, iroha_config.DEFAULT_ROLE,
                                        iroha_config.ASSET_CARBON_TAX, iroha_config.ASSET_PRECISION)

# create a domain for carbon payments (coins)
iroha_functions.create_domain_and_asset(iroha_config.DOMAIN_CARBON_PAYMENTS, iroha_config.DEFAULT_ROLE,
                                        iroha_config.ASSET_CARBON_PAYMENTS, iroha_config.ASSET_PRECISION)

# create government in both domains. The government stats with tons of assets
government_public_key_tax = IrohaCrypto.derive_public_key(iroha_config.GOVERNMENT_PK_TAX)
iroha_functions.create_account_with_assets(iroha_config.DOMAIN_CARBON_TAX, iroha_config.GOVERNMENT_ID,
                                           government_public_key_tax, iroha_config.ASSET_CARBON_TAX,
                                           '50000000000')
government_public_key_payments = IrohaCrypto.derive_public_key(iroha_config.GOVERNMENT_PK_PAYMENTS)
iroha_functions.create_account_with_assets(iroha_config.DOMAIN_CARBON_PAYMENTS, iroha_config.GOVERNMENT_ID,
                                           government_public_key_payments, iroha_config.ASSET_CARBON_PAYMENTS,
                                           '50000000000')


# create a dictionary to get all users private keys and create users in the domain_carbon_tax
with open('user_private_keys_carbon_taxes.csv', mode='w') as user_private_key:
    private_key_writer = csv.writer(user_private_key, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    private_key_writer.writerow(["user_id", "private_key"])
    for index, user in enumerate(users):
        user_private_key = IrohaCrypto.private_key()
        private_key_writer.writerow([user, str(user_private_key)])
        user_name = user
        user_public_key = IrohaCrypto.derive_public_key(user_private_key)
        iroha_functions.create_account_with_assets(iroha_config.DOMAIN_CARBON_TAX, user_name, user_public_key,
                                                   iroha_config.ASSET_CARBON_TAX, iroha_config.CARBON_TAX_INIT)

# create a dictionary to get all users private keys and create users in the domain_carbon_payments
with open('user_private_keys_carbon_payments.csv', mode='w') as user_private_key:
    private_key_writer = csv.writer(user_private_key, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    private_key_writer.writerow(["user_id", "private_key"])
    for index, user in enumerate(users):
        user_private_key = IrohaCrypto.private_key()
        private_key_writer.writerow([user, str(user_private_key)])
        user_name = user
        user_public_key = IrohaCrypto.derive_public_key(user_private_key)
        iroha_functions.create_account_with_assets(iroha_config.DOMAIN_CARBON_PAYMENTS, user_name, user_public_key,
                                                   iroha_config.ASSET_CARBON_PAYMENTS, iroha_config.CARBON_COIN_INIT)

