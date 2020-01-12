import functools
import itertools
import logging
from typing import List

import relay.concurrency_utils as concurrency_utils

from .events import BlockchainEvent
from .gateway_events import (
    ExchangeRateChangedEventType,
    event_builders,
    standard_event_types,
)
from .proxy import Proxy, sorted_events

logger = logging.getLogger("gateway")


class GatewayProxy(Proxy):

    event_builders = event_builders
    event_types = list(event_builders.keys())
    standard_event_types = standard_event_types

    def __init__(self, web3, gateway_abi, address: str) -> None:
        super().__init__(web3, gateway_abi, address)
        self.exchange_rate: int = self._proxy.functions.exchangeRate().call()
        self.escrow_address: str = self._proxy.functions.escrowAddress().call()
        self.gated_currency_network_address: str = self._proxy.functions.gatedCurrencyNetworkAddress().call()

    def deposits_of(self, user_address: str):
        return self._proxy.functions.depositsOf(user_address).call()

    def get_gateway_events(
        self, event_name: str, from_block: int = 0, timeout: float = None
    ) -> List[BlockchainEvent]:
        logger.debug(
            "get_gateway_events: event_name=%s from_block=%s", event_name, from_block
        )
        queries = [
            functools.partial(self.get_events, event_name, from_block=from_block)
        ]
        events = concurrency_utils.joinall(queries, timeout=timeout)
        return sorted_events(events)

    def get_all_gateway_events(
        self, from_block: int = 0, timeout: float = None
    ) -> List[BlockchainEvent]:
        queries = [
            functools.partial(self.get_gateway_events, type, from_block=from_block)
            for type in self.standard_event_types
        ]
        results = concurrency_utils.joinall(queries, timeout=timeout)
        return sorted_events(list(itertools.chain.from_iterable(results)))

    def start_listen_on_exchange_rate_changed(self, on_exchange_rate_changed) -> None:
        def log(log_entry):
            on_exchange_rate_changed(self._build_event(log_entry))

        self.start_listen_on(ExchangeRateChangedEventType, log)
