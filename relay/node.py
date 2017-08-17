
class Node:

    def __init__(self, web3):
        self._web3 = web3

    def relay_tx(self, rawtxn):
        return self._web3.eth.sendRawTransaction(rawtxn)

    def transaction_receipt(self, txn_hash):
        return self._web3.eth.getTransactionReceipt(txn_hash)

    def get_tx_infos(self, user_address):
        return {'balance': self._web3.eth.getBalance(user_address),
                'nonce': self._web3.eth.getTransactionCount(user_address),
                'gasPrice': self._web3.eth.gasPrice}

    @property
    def blocknumber(self):
        return self._web3.eth.blockNumber

    def balance(self, address):
        return self._web3.eth.getBalance(address)