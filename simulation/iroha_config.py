#!/usr/bin/env python3
import datetime
from iroha import Iroha, IrohaGrpc, IrohaCrypto
import sys
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

# BSMD configuration
######################
# This parameters are for the admin of the BSMD
# Replace localhost with an IP address of a node running the blockchain
NETWORK = IrohaGrpc('localhost:50051')
ADMIN_PRIVATE_KEY = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
IROHA_ADMIN = Iroha('admin@test')
# New users will be created with the default role *user* which consists in the following permissions
# "can_add_signatory",
# "can_get_my_acc_ast",
# "can_get_my_acc_ast_txs",
# "can_get_my_acc_detail",
# "can_get_my_acc_txs",
# "can_get_my_account",
# "can_get_my_signatories",
# "can_get_my_txs",
# "can_grant_can_add_my_signatory",
# "can_grant_can_remove_my_signatory",
# "can_grant_can_set_my_account_detail",
# "can_grant_can_set_my_quorum",
# "can_grant_can_transfer_my_assets",
# "can_receive",
# "can_remove_signatory",
# "can_set_quorum",
# "can_transfer"

DEFAULT_ROLE = 'user'
GOVERNMENT_ID = 'government'
GOVERNMENT_PK_TAX = '8c2a7138e7a9a20952fdbf230b78618189efe2e40cd6ef236d84465050941f9a'
GOVERNMENT_PK_PAYMENTS = 'b5a604656e38a5a5b46567291b630bec7aefed62eda7e2c1001943be4a47221a'

# Domain are groups of accounts. (small caps only)
# This parameters are for setting the characteristics of each domain.
DOMAIN_CARBON_TAX = 'carbontaxes'
DOMAIN_CARBON_PAYMENTS = 'carbonpayments'

# You can create as many assets as you want on each domain as long as the the name of the asset is unique
# Exchange rate 1 carbontax = 1 carboncoin
ASSET_CARBON_TAX = 'carbontax'
ASSET_CARBON_PAYMENTS = 'carboncoin'
ASSET_PRECISION = 2

# EXPERIMENT configuration
######################
# Initial time of the simulation
SIMULATION_STARTS_AT = datetime.datetime(2019, 9, 24, 8, 00, 00)
# Length in seconds of the simulation
LENGTH = 86400 # 24hrs
# Initial amount of carbon tokes everyone start with
CARBON_TAX_INIT = 493.79
# Initial amount of carbon coin everyone start with
CARBON_COIN_INIT = 50000

