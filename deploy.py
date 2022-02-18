from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()

install_solc("0.6.6")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.6",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#connecting rinkeby
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/719c683e506f48e2841fce7a1d11d3a5"))
chainID = 4
my_address = "0x248C0ed5f24939efab3c2dC7eb8DaB1640b71D7A"
private_key = os.environ.get("PRIVATE_KEY")

# Creating contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

#get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

#building signing and sending transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chainID, "from": my_address, "nonce": nonce, "gasPrice": w3.eth.gas_price})
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

print("Contract deploying...")

#Working with contract
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)
print("Contract deployed")

#Call -> Simulate making the call and getting return value
#Transact -> Make the state change

print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(15).call())

store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chainID,
    "from": my_address,
    "nonce": nonce+1,
    "gasPrice": w3.eth.gas_price
})

print("Updating contract...")

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)

print("Contract updated")

print(simple_storage.functions.retrieve().call())
