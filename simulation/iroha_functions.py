#!/usr/bin/env python3
from iroha.primitive_pb2 import can_set_my_account_detail
from iroha import IrohaCrypto, Iroha
import binascii
import iroha_config
import sys
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """
    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result
    return tracer



@trace
def send_transaction_and_print_status(transaction):
    """
    Send a transaction to the Blockchain (BSMD)
    :param transaction: Transaction we are sending to the BSMD
    :return: null:
    """
    print('This print will make the transactions run slower. When developing is useful to have this for debugging')
    print('Comment all prints in function send_transaction_and_print_status to make faster transactions')
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    iroha_config.NETWORK.send_tx(transaction)
    for status in iroha_config.NETWORK.tx_status_stream(transaction):
        print(status)


@trace
def create_domain_and_asset(domain, default_role, asset_name, asset_precision):
    """
    Creates a domain and an asset in the domain
    :param domain: name of the domain, e.g. entity, vehicle, individual
    :param default_role: default role users have, e.g., user
    :param asset_name: name of the asset, e.g., entityCoin
    :param asset_precision: number of decimals accepted in the asset
    :return: null
    """
    print(domain, default_role, asset_name, asset_precision)
    commands = [iroha_config.IROHA_ADMIN.command('CreateDomain',
                                                 domain_id=domain,
                                                 default_role=default_role),
                iroha_config.IROHA_ADMIN.command('CreateAsset',
                                                 asset_name=asset_name,
                                                 domain_id=domain,
                                                 precision=asset_precision)]

    tx = IrohaCrypto.sign_transaction(iroha_config.IROHA_ADMIN.transaction(commands), iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def create_domain(domain, default_role):
    """
    Creates a domain
    :param domain: name of the domain, e.g. entity, vehicle, individual
    :param default_role: default role users have, e.g., user
    :return:
    """
    print(domain, default_role)
    tx = iroha_config.IROHA_ADMIN.transaction(
        [iroha_config.IROHA_ADMIN.command('CreateDomain',
                                          domain_id=domain,
                                          default_role=default_role)])

    IrohaCrypto.sign_transaction(tx, iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

@trace
def create_asset(domain, asset_name, asset_precision):
    """
    Creates an asset in the domain_id
    :param domain: name of the domain, e.g. entity, vehicle, individual
    :param asset_name: name of the asset, e.g., entityCoin
    :param asset_precision: number of decimals accepted in the asset
    :return:
    """
    tx = iroha_config.IROHA_ADMIN.transaction(
        [iroha_config.IROHA_ADMIN.command('CreateAsset',
                                          asset_name=asset_name,
                                          domain_id=domain,
                                          precision=asset_precision)])
    IrohaCrypto.sign_transaction(tx, iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

@trace
def create_account_with_assets(domain, name, public_key, asset_name, asset_qty):
    """
    Create a personal account. This function works in three steps
        1. Create an account with a name, in a domain and a public key
        2. The admin create credit (assets) for the account (credit is created only if the user
           buy it)
        3. The admin transfer the credit to the user
    :param domain: (str) Name of the domain the user wants to join
    :param name: (str) Name of the node we are creating
    :param public_key: (str) public key of the node
    :param asset_name: Name of asset the node buy
    :param asset_qty: (float) Quantity of assets the node buy
    :return: null:

    Usage example:
    create_account_user('Tommy', 'key', 'federated', '5', fedcoin#federated)
    """
    asset_id = asset_name + '#' + domain
    # 1. Create account
    tx = iroha_config.IROHA_ADMIN.transaction(
        [iroha_config.IROHA_ADMIN.command('CreateAccount',
                       account_name=name,
                       domain_id=domain,
                       public_key=public_key)])
    IrohaCrypto.sign_transaction(tx, iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

    # 2. Create credit for the user
    tx = iroha_config.IROHA_ADMIN.transaction([iroha_config.IROHA_ADMIN.command('AddAssetQuantity',
                                          asset_id=asset_id,
                                          amount=asset_qty)])
    IrohaCrypto.sign_transaction(tx, iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

    # 3. Transfer credit to the user
    dest_account_id = name + '@' + domain
    tx = iroha_config.IROHA_ADMIN.transaction([
        iroha_config.IROHA_ADMIN.command('TransferAsset',
                      src_account_id='admin@test',
                      dest_account_id=dest_account_id,
                      asset_id=asset_id,
                      description='initial credit',
                      amount=asset_qty)])
    IrohaCrypto.sign_transaction(tx, iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

@trace
def create_assets_for_user(domain, name, asset_name, asset_qty):
    """
    Create a personal account. This function works in three steps
        1. Create an account with a name, in a domain and a public key
        2. The admin create credit (assets) for the account (credit is created only if the user
           buy it)
        3. The admin transfer the credit to the user
    :param domain: (str) Name of the domain the user wants to join
    :param name: (str) Name of the node we are creating
    :param asset_name: (str) Name of asset the node buy
    :param asset_qty: (float) Quantity of assets the node buy
    :return: null:
    """
    asset_id = asset_name + '#' + domain
    tx = iroha_config.IROHA_ADMIN.transaction([iroha_config.IROHA_ADMIN.command('AddAssetQuantity',
                                          asset_id=asset_id,
                                          amount=asset_qty)])
    IrohaCrypto.sign_transaction(tx, iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

    dest_account_id = name + '@' + domain
    tx = iroha_config.IROHA_ADMIN.transaction([
        iroha_config.IROHA_ADMIN.command('TransferAsset',
                      src_account_id='admin@test',
                      dest_account_id=dest_account_id,
                      asset_id=asset_id,
                      description='asset created for node',
                      amount=asset_qty)])
    IrohaCrypto.sign_transaction(tx, iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


@trace
def create_account(domain, name, public_key):
    """
    Create a personal account.
    :param domain: (str) Name of the domain the user wants to join
    :param name: (str) Name of the node we are creating
    :param public_key: (str) public key of the node
    :return: null:
    """
    # 1. Create account
    tx = iroha_config.IROHA_ADMIN.transaction(
        [iroha_config.IROHA_ADMIN.command('CreateAccount',
                       account_name=name,
                       domain_id=domain,
                       public_key=public_key)])
    IrohaCrypto.sign_transaction(tx, iroha_config.ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)



@trace
def get_balance(domain, name, private_key):
    """
    Get the balance of the account
    :param domain: (str) name of the domain
    :param name: (str) name of the transaction signer
    :param private_key: (str) Private key of the user
    :return: data: (array) asset id and assets quantity
    Return example:
    [asset_id: "fedcoin#federated"
    account_id: "generator@federated"
    balance: "1000"
    ]
    """
    account_id = name + '@' + domain
    iroha = Iroha(account_id)
    query = iroha.query('GetAccountAssets',
                        account_id=account_id)
    IrohaCrypto.sign_query(query, private_key)

    response = iroha_config.NETWORK.send_query(query)
    data = response.account_assets_response.account_assets
    for asset in data:
        print('Asset id = {}, balance = {}'.format(asset.asset_id, asset.balance))
    return data


@trace
def grants_access_to_set_details(your_domain, your_name, private_key, grant_domain, grant_account):
    """
    Grant node to set details on your profile
    :param your_domain: (str) your domain. Domain of the granter
    :param your_name:  (str) you name. Name of the granter
    :param private_key: (str) private key for signing. Private key of the granter
    :param grant_domain: (str) domain of the node how will have access permissions
    :param grant_account: (str) name of the node how will have access permissions
    :return:
    """
    my_id_account = your_name + '@' + your_domain
    grant_account_id = grant_account + '@' + grant_domain
    iroha = Iroha(my_id_account)
    tx = iroha.transaction([
        iroha.command('GrantPermission',
                      account_id=grant_account_id,
                      permission=can_set_my_account_detail)
    ],
        creator_account=my_id_account)
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx)


@trace
def set_detail(domain, name, private_key, detail_key, detail_value):
    """
    Set the details of a node. The details can be stored in JSON format with limit of 4096 characters per detail
    :param domain: (str) name of the domain
    :param name: (str) name of the transaction signer
    :param private_key: (str) Private key of the user
    :param detail_key: (str) Name of the detail we want to set
    :param detail_value: (str) Value of the detail
    :return: null:

    Usage example:
    set_detail('vehicle'),'Ford fiesta', 'key', 'age', '33')
    """
    account_id = name + '@' + domain
    iroha = Iroha(account_id)
    tx = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id,
                      key=detail_key,
                      value=detail_value)
    ])
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx)


@trace
def set_detail_to_node(domain, name, private_key, to_domain, to_name, detail_key, detail_value):
    """
    Set the details of a node. The details can be stored in JSON format with limit of 4096 characters per detail
    :param domain: (str) domain of the signer
    :param name: (str) name signer
    :param private_key: (str) Private key of the signer
    :param to_domain: (str) domain of the receptor
    :param to_name: (str) name of the receptor
    :param detail_key: (str) Name of the detail we want to set
    :param detail_value: (str) Value of the detail
    :return: null:

    Usage example:
    set_detail('vehicle'),'Ford fiesta', 'key', 'age', '33')
    """
    account = name + '@' + domain
    iroha = Iroha(account)
    account_id = to_name + '@' + to_domain
    tx = iroha.transaction([
        iroha.command('SetAccountDetail',
                      account_id=account_id,
                      key=detail_key,
                      value=detail_value)
    ])
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx)


@trace
def transfer_assets(domain, name, private_key, to_name, asset_name, quantity, description):
    """
    Transfer assets from one account to another
    :param domain: (str) name of the domain from where the node is sending the assets
    :param name: (str) name of the node who is sending the assets
    :param private_key: (str) pk of the the sender
    :param to_name: (str) name of the node receiving the assets
    :param asset_name: (str) name of the asset to be transferred
    :param quantity: (float) Number of assets we want to transfer
    :param description: (str) Small message to the receiver of assets
    :return:

    Example:
    transfer_assets('individuals','Dante', 'key', 'Toro', 'coin', '2', 'Shut up and take my money')
    """

    account_id = name + '@' + domain
    iroha = Iroha(account_id)
    destination_account = to_name + '@' + domain
    asset_id = asset_name + '#' + domain
    tx = iroha.transaction([
        iroha.command('TransferAsset',
                      src_account_id=account_id,
                      dest_account_id=destination_account,
                      asset_id=asset_id,
                      description=description,
                      amount=quantity)
    ])
    IrohaCrypto.sign_transaction(tx, private_key)
    send_transaction_and_print_status(tx)


@trace
def get_detail_from_generator(domain, name, private_key, generator_domain, generator_name, detail_id):
    """
    Consult a single detail writen by some generator
    :param domain: (str) name of the domain
    :param name: (str) name of the node
    :param private_key: (str) Private key of the user
    :param generator_domain: (str) domain of the user who create de detail
    :param generator_name: (str) name of the user who create de detail
    :param detail_id: (string) Name of the detail
    :return: data: (json) solicited details of the user

    Usage example:
    get_detail_from_generator('individual', 'David' 'key', 'vehicle', 'Sara' , 'Age')

    Return example:
    {
       "nodeA@domain":{
             "Age":"35"
        }
    }
    """
    account_id = name + '@' + domain
    generator_id = generator_name + '@' + generator_domain
    iroha = Iroha(account_id)
    query = iroha.query('GetAccountDetail',
                        account_id=account_id,
                        writer=generator_id,
                        key=detail_id)
    IrohaCrypto.sign_query(query, private_key)

    response = iroha_config.NETWORK.send_query(query)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return data.detail


@trace
def get_all_details_from_generator(domain, name, private_key, generator_domain, generator_name):
    """
    Consult all the details generated by some node
    :param domain: (str) name of the domain
    :param name: (str) name of the node
    :param private_key: (str) Private key of the user
    :param generator_domain: (str) domain of the user who create de detail
    :param generator_name: (str) name of the user who create de detail
    :return: data: (json) solicited details of the user

    Usage example:
    get_detail_from_generator('vehicle', 'Ford Fiesta', key, 'individual', 'david' )

    Return example:
    {
       "nodeA@domain":{
            "Age":"35",
            "Name":"Quetzacolatl"
        }
    }
    """
    account_id = name + '@' + domain
    generator_id = generator_name + '@' + generator_domain
    iroha = Iroha(account_id)
    query = iroha.query('GetAccountDetail',
                        account_id=account_id,
                        writer=generator_id)
    IrohaCrypto.sign_query(query, private_key)

    response = iroha_config.NETWORK.send_query(query)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return data.detail



@trace
def get_all_details(domain, name, private_key):
    """
    Consult all details of the node
    :param domain: (str) name of the domain
    :param name: (str) name of the node
    :param private_key: (str) Private key of the user
    :return: data: (json) solicited details of the user

    Usage example:
    get_detail_from_generator(Iroha('david@federated'),IrohaGrpc('127.0.0.1'), 'david@federated', 'key')

    Return example:
    {
        "nodeA@domain":{
            "Age":"35",
            "Name":"Quetzacoatl"
        },
        "nodeB@domain":{
            "Location":"35.3333535,-45.2141556464",
            "Status":"valid"
        },
        "nodeA@domainB":{
            "FederatingParam":"35.242553",
            "Loop":"3"
        }
    }
    """
    account_id = name + '@' + domain
    iroha = Iroha(account_id)
    query = iroha.query('GetAccountDetail',
                        account_id=account_id)
    IrohaCrypto.sign_query(query, private_key)

    response = iroha_config.NETWORK.send_query(query)
    data = response.account_detail_response
    print('Account id = {}, details = {}'.format(account_id, data.detail))
    return data.detail


@trace
def get_block(height):
    """
    Query a block in the ledger
    :param height:
    :return:
    """

    iroha_config.IROHA_ADMIN.blocks_query()
    query = iroha_config.IROHA_ADMIN.query('GetBlock',
                                     height=height)
    IrohaCrypto.sign_query(query, iroha_config.ADMIN_PRIVATE_KEY)

    block = iroha_config.NETWORK.send_query(query)
    print(block)
    return block

