#!/usr/bin/env python3
import sys
from iroha import IrohaCrypto
import iroha_functions as irofun
import iroha_config as irocon
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

# Network setup. All operations in the setup are made by the admin

#########################################################################################
# The firs step in the creation of the BSMD is to create a domain and asset for the nodes
# The admin node is in charge of do this, hence all transactions need to be signed by him
# 1. You can create a domain with an asset
# create_domain_and_asset(domain_id, default_role, asset_name, asset_precision)
irofun.create_domain_and_asset(irocon.domain_vehicle, irocon.default_role, irocon.asset_vehicle, irocon.asset_precision)

# # 2. You can create a domain with no assets
irofun.create_domain(irocon.domain_individual, irocon.default_role)
#
# # 3. You can add an asset to a domain already created. In 2 we have created the domain *individual*, no we can create
# # an asset for individuals
irofun.create_asset(irocon.domain_individual, irocon.asset_individual, irocon.asset_precision)


# ########################################################################################
# # The second step is the creation of passive Nodes (also called accounts).
# # First define the name of the passive node
# node1_name = 'sandro'  # small caps for name
# # Nodes need public and private keys for signing transactions. The private key is used to derive the public key.
# # Private key is never shared and nodes will sign the ledger with the public key
# # To create private and public keys for passive nodes use
# # Ideally you should create private key with node2_private_key = IrohaCrypto.private_key(). For the sake of the example
# # the private key is hardcoded so it is easy to reproduce de example
# node1_private_key = '4d5c17de889044ff43d522123d7584dc96f9d1fe6cfd90860a2d9c1f58d38824'
#
# node1_public_key = IrohaCrypto.derive_public_key(node1_private_key)
#
# # Admin node can create user accounts in a specific domain and add some assets to his account.
# # We will create a user in the individual domain
# irofun.create_account_with_assets(irocon.domain_individual, node1_name, node1_public_key, irocon.asset_individual,
#                                   '1000')
#
# # Also is possible to create user accounts with no assets. But first define the name and the private and public keys
# # We will create a user in the vehicle domain
# node2_name = 'gol'
# node2_private_key = '0dee25b65cc30c2dea0ced919e6c613489de801de1544bba9c3d97fac18d7ec4'
# node2_public_key = IrohaCrypto.derive_public_key(node2_private_key)
# irofun.create_account(irocon.domain_vehicle, node2_name, node2_public_key)
# # We can add some assets to the user
# irofun.create_assets_for_user(irocon.domain_vehicle, node2_name, irocon.asset_vehicle, '5000')
#
#
#
