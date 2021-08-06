# Import dependencies
import os
import subprocess
import json
from dotenv import load_dotenv
import pprint
from bit import PrivateKeyTestnet

pp = pprint.PrettyPrinter(indent=2)

from eth_account import Account

# Load and set environment variables
load_dotenv("/Users/FinTech/PycharmProjects/Bootcamp/HW/19-Wallet/mnemonic_keys.env")
mnemonic = os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Create a function called `derive_wallets`
def derive_wallets(coinType):
    command = 'php hd-wallet-derive/hd-wallet-derive.php ' \
              '-g ' \
              '--mnemonic=mnemonic ' \
              '--cols=address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub ' \
              '--format=json ' \
              '--coin=' + coinType + ' ' \
                                     '--numderive=3'
    print('Command to execute: ' + command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {ETH: derive_wallets(ETH), BTCTEST: derive_wallets(BTCTEST)}
pp.pprint(coins)
print("Private key of the 2nd ethereum index is: " + coins[ETH][1]['privkey'])

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, private_key):
    if coin == 'eth':
        account_eth = Account.from_key(private_key)
        return account_eth
    if coin == 'btc-test':
        account_btctest = PrivateKeyTestnet(private_key)
        return account_btctest

account = priv_key_to_account('btc-test', "cVAgDoahzo5Ucdv8ioxxubvmE6LfU3ZQgJ21UvY4eC1xi6WkvnXe")
print(account.address)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    if coin == 'eth':
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    if coin == 'btc_test':
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, coin)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    if coin == 'eth':
        tx = create_tx(coin, account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    if coin == 'btc_test':
        tx = create_tx(coin, account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        return NetworkAPI.broadcast_tx_testnet(signed_tx)




