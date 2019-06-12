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
Johannes = 'johannes'  # write al names with small caps
Johannes_private_key = 'e66dcb02367ae45449075839bbfedaf9ae4f9d579cb5601e82e0df341691ae2c'
Johannes_public_key = IrohaCrypto.derive_public_key(Johannes_private_key)
irofun.create_account_with_assets(irocon.domain_individual, Johannes, Johannes_public_key, irocon.asset_individual,
                                  '1000')
#####################
David = 'david'
David_private_key = '2297b39c5331af17731d9bd6e04070e575b7ad9c18ca951cb6d5cd7b2abb240d'
David_public_key = IrohaCrypto.derive_public_key(David_private_key)
irofun.create_account_with_assets(irocon.domain_individual, David, David_public_key, irocon.asset_individual, '1000')
# #####################
# # 1 Vehicle node
# #####################
Fiesta = 'fiesta'
Fiesta_private_key = '68e1e57b6ba06c45247937c3ea534a9560a63e6153a38a6ff0efef99ba774308'
Fiesta_public_key = IrohaCrypto.derive_public_key(Fiesta_private_key)
irofun.create_account_with_assets(irocon.domain_vehicle, Fiesta, Fiesta_public_key, irocon.asset_vehicle, '1000')

####################
######Assets#######
# David send 500 assets to Johannes
irofun.transfer_assets(irocon.domain_individual, Johannes, Johannes_private_key, David, irocon.asset_individual, '500',
                       'carbon debt')


######Transactions#######
# Johannes records his own trip
# First create a json with the information of the trip
transaction_data = dict()
transaction_data['Date'] = '07-03-2019 4:56'
transaction_data['carbon emitted'] = 500
transaction_data['trip porpoise'] = 'leisure'
transaction_data['creator'] = 'Johannes'
j = json.dumps(transaction_data)
j_in_ledger = str(j)
jsonTrip = j_in_ledger.replace('"','')
irofun.set_detail(irocon.domain_individual, Johannes, Johannes_private_key, 'Trip', jsonTrip)


# A vehicle records a trip in Johannes's profile
# First Johannes grants Fiesta to record trips on his behalf
irofun.grants_access_to_set_details(irocon.domain_individual, Johannes, Johannes_private_key, irocon.domain_vehicle,
                                    Fiesta)
# Vehicle creates the trip in a Json file
transaction_data = dict()
transaction_data['Date'] = '07-07-2019 14:56'
transaction_data['carbon emitted'] = 1000
transaction_data['trip porpoise'] = 'work'
transaction_data['creator'] = 'Fiesta'
j = json.dumps(transaction_data)
j_in_ledger = str(j)
jsonTrip = j_in_ledger.replace('"','')
# Vehicle set records the trip in Johannes profile
irofun.set_detail_to_node(irocon.domain_vehicle,Fiesta,Fiesta_private_key,irocon.domain_individual,Johannes, 'Trip',
                          jsonTrip)



















