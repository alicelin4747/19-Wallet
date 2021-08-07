# 19-Wallet
## Transation Screenshot
### BTC-Test

`send_tx('btc-test', account_btctest, 'mxwSU31v1NtbUi6Pc5bN9BgmmAGw13JdvX', 0.000005)`

![alt text](sender.jpg)

![alt text](recipient.jpg)

## What does the wallet do
1. `drive_wallets` function - use hd-wallet-derive to generate wallets for BTC-Testnet and ETH
2. store the wallet information such as address and keys for each coin type in a dictionary
3. `priv_key_to_account` function - convert private keys to account address using `Account.from_key` for ETH and `PrivateKeyTestnet` for BTC-testnet
4. `create_tx` function - create unsigned transaction
5. `send_tx` function - signs and sends the transaction

Library needed for the wallet include bit, eth_accont, web3, subprocess, json, and NetworkAPI.  