#!/usr/bin/env python3
import sys
from iroha import IrohaCrypto
import iroha_functions as irofun
import iroha_config as irocon
import json
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


# For running this example first run the setup.py file

# We will create 3 nodes to demonstrate functions of the BSMD.
#####################
# 2 Individual nodes
#####################
Johannes = 'Johannes'
Johannes_private_key = IrohaCrypto.private_key()
Johannes_public_key = IrohaCrypto.derive_public_key(Johannes_private_key)
irofun.create_account_with_assets(irocon.domain_individual, Johannes, Johannes_public_key, irocon.asset_individual,
                                  '1000')
# #####################
# David = 'David'
# David_private_key = IrohaCrypto.private_key()
# David_public_key = IrohaCrypto.derive_public_key(Johannes_private_key)
# irofun.create_account_with_assets(irocon.domain_individual, David, David_public_key, irocon.asset_individual, '1000')
# #####################
# # 2 Vehicle nodes
# #####################
# Fiesta = 'Fiesta'
# Fiesta_private_key = IrohaCrypto.private_key()
# Fiesta_public_key = IrohaCrypto.derive_public_key(Johannes_private_key)
# irofun.create_account_with_assets(irocon.domain_vehicle, Fiesta, Fiesta_public_key, irocon.asset_vehicle, '1000')
# #####################
#
# ######Assets#######
# # David send 500 assets to Johannes
# irofun.transfer_assets(irocon.domain_individual, David, David_private_key, Johannes, irocon.asset_individual,'500',
#                        'Carbon debt')
#
# ######Transactions#######
# # Johannes records his own trip
# # First create a json with the information of the trip
# transaction_data = dict()
# transaction_data['Date'] = '07-03-2019 4:56'
# transaction_data['carbon emitted'] = 500
# transaction_data['trip porpoise'] = 'leisure'
# transaction_data['creator'] = 'Johannes'
# j = json.dumps(transaction_data)
# j_in_ledger = str(j)
# jsonTrip = j_in_ledger.replace('"','')
# irofun.set_detail(irocon.domain_individual, Johannes, Johannes_private_key, 'Trip', jsonTrip)
#
#
# # A vehicle records a trip in Johannes's profile
# # First Johannes grants Fiesta to record trips on his behalf
# irofun.grants_access_to_set_details(irocon.domain_individual, Johannes, Johannes_private_key, irocon.domain_vehicle,
#                                     Fiesta)
# # Vehicle creates the trip in a Json file
# transaction_data = dict()
# transaction_data['Date'] = '07-07-2019 14:56'
# transaction_data['carbon emitted'] = 1000
# transaction_data['trip porpoise'] = 'work'
# transaction_data['creator'] = 'Fiesta'
# j = json.dumps(transaction_data)
# j_in_ledger = str(j)
# jsonTrip = j_in_ledger.replace('"','')
# # Vehicle set records the trip in Johannes profile
# irofun.set_detail_to_node(irocon.domain_vehicle,Fiesta,Fiesta_private_key,irocon.domain_individual,Johannes, 'Trip',
#                           jsonTrip)
#
#
#
#
#
#


















