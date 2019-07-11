#!/usr/bin/env python3
import datetime
from iroha import Iroha, IrohaGrpc
import sys
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

# BSMD configuration
######################
# This parameters are for the admin of the BSMD
# Replace localhost with an IP address of a node running the blockchain
network = IrohaGrpc('localhost:50051')
admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
iroha_admin = Iroha('admin@test')
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
default_role = 'user'

# Domain are groups of accounts. (small caps only)
# This parameters are for setting the characteristics of each domain.
domain_carbon_tax = 'carbontaxes'
domain_carbon_payments = 'carbonpayments'

# You can create as many assets as you want on each domain as long as the the name of the asset is unique
# Exchange rate 1 carbontax = 1 carboncoin
asset_carbon_tax = 'carbontax'
asset_carbon_payments = 'carboncoin'
asset_precision = 2

# EXPERIMENT configuration
######################
# Initial time of the simulation
SIMULATION_STARTS_AT = datetime.datetime(2019, 9, 24, 8, 00, 00)
# Length in seconds of the simulation
LENGTH = 86400 # 24hrs
# Initial amount of carbon tokes everyone start with
CARBON_TAX_INIT = 493.79
# Initial amount of carbon coin everyone start with
CARBON_COIN_INIT = 0
