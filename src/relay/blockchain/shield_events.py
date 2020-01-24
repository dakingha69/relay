from hexbytes import HexBytes

from .events import BlockchainEvent

# MerkleTree.sol events (shield contract inherits)
NewLeafEventType = "NewLeaf"
NewLeavesEventType = "NewLeaves"
# OutputEventType = "Output"

# CurrencyNetworkShield.sol events
TransferEventType = "Transfer"
SimpleBatchTransferEventType = "SimpleBatchTransfer"
BurnEventType = "Burn"
VerifierChangedEventType = "VerifierChanged"
VkChangedEventType = "VkChanged"
GatewayChangedEventType = "GatewayChanged"
GasUsedEventType = "GasUsed"

transaction_types = ["Mint", "Transfer", "Burn", "SimpleBatchTransfer"]


def str_to_bytes(str_or_bytes):
    """
    We have to convert str to bytes of bytes32 event arguments
    because the indexer currently can not save bytes in the database.
    See issue https://github.com/trustlines-protocol/py-eth-index/issues/16
    """
    if isinstance(str_or_bytes, HexBytes):
        return str_or_bytes
    else:
        return HexBytes(str_or_bytes)


class ShieldEvent(BlockchainEvent):
    def __init__(self, web3_event, current_blocknumber: int, timestamp: int):
        super().__init__(web3_event, current_blocknumber, timestamp)
        self.shield_address = web3_event.get("address")


class LeafEvent(ShieldEvent):
    @property
    def root(self):
        return str_to_bytes(self._web3_event.get("args").get("root"))


class NewLeafEvent(LeafEvent):
    @property
    def leaf_index(self):
        return self._web3_event.get("args").get("leafIndex")

    @property
    def leaf_value(self):
        return str_to_bytes(self._web3_event.get("args").get("leafValue"))


class NewLeavesEvent(LeafEvent):
    @property
    def min_leaf_index(self):
        return self._web3_event.get("args").get("minLeafIndex")

    @property
    def leaf_values(self):
        leaf_values = [
            str_to_bytes(leaf_value)
            for leaf_value in self._web3_event.get("args").get("leafValues")
        ]
        return leaf_values


class TransferEvent(ShieldEvent):
    @property
    def nullifier_1(self):
        return str_to_bytes(self._web3_event.get("args").get("nullifier1"))

    @property
    def nullifier_2(self):
        return str_to_bytes(self._web3_event.get("args").get("nullifier2"))


class SimpleBatchTransferEvent(ShieldEvent):
    @property
    def nullifier(self):
        return str_to_bytes(self._web3_event.get("args").get("nullifier"))


class BurnEvent(SimpleBatchTransferEvent):
    pass


class VerifierChangedEvent(ShieldEvent):
    @property
    def new_verifier(self):
        return self._web3_event.get("args").get("newVerifierContract")


class VkChangedEvent(ShieldEvent):
    @property
    def tx_type(self):
        return transaction_types[self._web3_event.get("args").get("txType")]


class GatewayChangedEvent(ShieldEvent):
    @property
    def new_gateway(self):
        return self._web3_event.get("args").get("newGatewayContract")


class GasUsedEvent(ShieldEvent):
    @property
    def by_shield_contract(self):
        return self._web3_event.get("args").get("byShieldContract")

    @property
    def by_verifier_contract(self):
        return self._web3_event.get("args").get("byVerifierContract")

    @property
    def by_currency_network_contract(self):
        return self._web3_event.get("args").get("byCurrencyNetworkContract")


event_builders = {
    NewLeafEventType: NewLeafEvent,
    NewLeavesEventType: NewLeavesEvent,
    # OutputEventType: OutputEvent,
    TransferEventType: TransferEvent,
    SimpleBatchTransferEventType: SimpleBatchTransferEvent,
    BurnEventType: BurnEvent,
    VerifierChangedEventType: VerifierChangedEvent,
    VkChangedEventType: VkChangedEvent,
    GatewayChangedEventType: GatewayChangedEvent,
    GasUsedEventType: GasUsedEvent,
}


standard_event_types = [
    NewLeafEventType,
    NewLeavesEventType,
    # OutputEventType,
    TransferEventType,
    SimpleBatchTransferEventType,
    BurnEventType,
    VerifierChangedEventType,
    VkChangedEventType,
    GatewayChangedEventType,
    GasUsedEventType,
]
