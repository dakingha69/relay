import logging
from typing import List

from .events import BlockchainEvent
from .proxy import Proxy
from .shield_events import event_builders, standard_event_types, transaction_types

logger = logging.getLogger("gateway")


class ShieldProxy(Proxy):

    event_builders = event_builders
    event_types = list(event_builders.keys())
    standard_event_types = standard_event_types

    def __init__(self, web3, shield_abi, address: str) -> None:
        super().__init__(web3, shield_abi, address)

        # Shield
        self.network_address: str = self._proxy.functions.getCurrencyNetwork().call()
        self.gateway_address: str = self._proxy.functions.getGateway().call()
        self.verifier_address: str = self._proxy.functions.getVerifier().call()
        self.latest_root: str = self._proxy.functions.latestRoot().call()

        # Merkle tree
        self.tree_height: int = self._proxy.functions.treeHeight().call()
        self.tree_width: int = self._proxy.functions.treeWidth().call()
        self.leaf_count: int = self._proxy.functions.leafCount().call()

    def nullifiers(self, nullifier: str):
        return self._proxy.functions.nullifiers(nullifier).call()

    def roots(self, root: str):
        return self._proxy.functions.roots(root).call()

    def vk_list(self):
        vk_list = [
            self._proxy.functions.getVerificationKey(i).call()
            for i in range(0, len(transaction_types))
        ]
        return vk_list

    def vk_of(self, transaction_type: str):
        index = transaction_types.index(transaction_type)
        return self._proxy.functions.getVerificationKey(index).call()

    def get_shield_events(
        self, event_name: str, from_block: int = 0, timeout: float = None
    ) -> List[BlockchainEvent]:
        return []

    def get_all_shield_events(
        self, from_block: int = 0, timeout: float = None
    ) -> List[BlockchainEvent]:
        return []
