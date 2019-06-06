#!/usr/bin/env python3
import sys
from iroha import IrohaCrypto
import iroha_functions as irofun
import iroha_config as irocon
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

#########################################################################################
# The firs step in the creation of the BSMD is to create a domain and asset for the nodes
# The admin node is in charge of do this, hence all transactions need to be signed by him
# 1. You can create a domain with an asset
# create_domain_and_asset(domain_id, default_role, asset_name, asset_precision)
irofun.create_domain_and_asset(irocon.domain_vehicle, irocon.default_role, irocon.asset_vehicle, irocon.asset_precision)

# 2. You can create a domain with no assets
irofun.create_domain(irocon.domain_individual, irocon.default_role)

# 3. You can add an asset to a domain already created. In 2 we have created the domain *individual*, no we can create
# an asset for individuals
irofun.create_asset(irocon.domain_individual,irocon.asset_individual,irocon.asset_precision)


########################################################################################
# The second step is the creations of passive Nodes (also called accounts).
# First define the name of the passive node
node_name = 'Moto'
# Nodes need a public and private key for signing transactions. The private key are use to derive the public key.
# private key are never shared and nodes will sign the ledger with the public key
# To create private and public keys for passive nodes use
node_private_key = IrohaCrypto.private_key()
node_public_key = IrohaCrypto.derive_public_key(node_private_key)









#################################
# workers nodes setup
################################
# create an account in the network
# create_account_user('Tommy', 'key', 'federated', '5', fedcoin#federated)
iroha_functions.create_account_user(iroha_config.worker1_name, iroha_config.worker1_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker2_name, iroha_config.worker2_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker3_name, iroha_config.worker3_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker4_name, iroha_config.worker4_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker5_name, iroha_config.worker5_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker6_name, iroha_config.worker6_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker7_name, iroha_config.worker5_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker8_name, iroha_config.worker8_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)
iroha_functions.create_account_user(iroha_config.worker9_name, iroha_config.worker9_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)

##################################
# chief node setup
# ################################
# create an account in the network
iroha_functions.create_account_user(iroha_config.chief_name, iroha_config.chief_public_key, iroha_config.domain_id,
                                    '1000', iroha_config.asset_id)

##################################
# grant access
# ################################
# grant access so worker nodes can share us his information
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker1_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker2_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker3_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker4_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker5_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker6_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker7_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key, iroha_config.worker8_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_chief, iroha_config.chief_account_id,
                                             iroha_config.chief_private_key,iroha_config.worker9_account_id)

# grant access so worker node can share us his information
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker1,iroha_config.worker1_account_id,
                                             iroha_config.worker1_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker2, iroha_config.worker2_account_id,
                                             iroha_config.worker2_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker3, iroha_config.worker3_account_id,
                                             iroha_config.worker3_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker4, iroha_config.worker4_account_id,
                                             iroha_config.worker4_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker5, iroha_config.worker5_account_id,
                                             iroha_config.worker5_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker6, iroha_config.worker6_account_id,
                                             iroha_config.worker6_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker7, iroha_config.worker7_account_id,
                                             iroha_config.worker7_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker8, iroha_config.worker8_account_id,
                                             iroha_config.worker8_private_key, iroha_config.chief_account_id)
iroha_functions.grants_access_to_set_details(iroha_config.iroha_worker9, iroha_config.worker9_account_id,
                                             iroha_config.worker9_private_key, iroha_config.chief_account_id)

print('**********************************')
print('**********************************')
print('The BSMD is created and iroha_configured')
print('**********************************')
print('**********************************')
