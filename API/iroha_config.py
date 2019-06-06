#!/usr/bin/env python3

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

# Domain are groups of accounts.
# This parameters are for setting the characteristics of each domain.
domain_entity = 'entity'
domain_vehicle = 'vehicle'
domain_individual = 'individual'
# You can create as many assets as you want on each domain as long as the the name of the asset is unique
asset_entity = 'entityCoin'
asset_vehicle = 'vehicleCoin'
asset_individual = 'individualCoin'
asset_entity_id = asset_entity + '#' + domain_entity
asset_vehicle_id = asset_vehicle + '#' + domain_vehicle
asset_individual_id = asset_individual + '#' + domain_individual
asset_precision = 2


# To create private and public keys for nodes use
# user_p_key = IrohaCrypto.private_key()
# print('private: ', user_p_key)
# print('public: ', IrohaCrypto.derive_public_key('f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'))
