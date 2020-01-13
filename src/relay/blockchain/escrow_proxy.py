import functools
import itertools
import logging
from typing import List

import relay.concurrency_utils as concurrency_utils

from .escrow_events import (
    DepositedEventType,
    EscrowEvent,
    WithdrawnEventType,
    event_builders,
    from_to_types,
    standard_event_types,
)
from .events import BlockchainEvent
from .proxy import Proxy, sorted_events

logger = logging.getLogger("escrow")


class EscrowProxy(Proxy):

    event_builders = event_builders
    event_types = list(event_builders.keys())

    standard_event_types = standard_event_types

    def __init__(self, web3, escrow_abi, address: str) -> None:
        super().__init__(web3, escrow_abi, address)

    def get_escrow_events(
        self,
        event_name: str,
        user_address: str = None,
        from_block: int = 0,
        timeout: float = None,
    ) -> List[BlockchainEvent]:
        logger.debug(
            "get_escrow_events: event_name=%s user_address=%s from_block=%s",
            event_name,
            user_address,
            from_block,
        )
        if user_address is None:
            queries = [
                functools.partial(self.get_events, event_name, from_block=from_block)
            ]
            events = concurrency_utils.joinall(queries, timeout=timeout)
        else:
            filter1 = {from_to_types[event_name][0]: user_address}

            queries = [
                functools.partial(self.get_events, event_name, filter1, from_block)
            ]
            results = concurrency_utils.joinall(queries, timeout=timeout)

            events = list(itertools.chain.from_iterable(results))

            for event in events:
                if isinstance(event, EscrowEvent):
                    event.user = user_address
                else:
                    raise ValueError("Expected a UnwEthEvent")
        return sorted_events(events)

    def get_all_escrow_events(
        self, user_address: str = None, from_block: int = 0, timeout: float = None
    ) -> List[BlockchainEvent]:
        queries = [
            functools.partial(
                self.get_escrow_events,
                type,
                user_address=user_address,
                from_block=from_block,
            )
            for type in self.standard_event_types
        ]
        results = concurrency_utils.joinall(queries, timeout=timeout)
        return sorted_events(list(itertools.chain.from_iterable(results)))

    def start_listen_on_deposited(self, on_deposited) -> None:
        def log(log_entry):
            on_deposited(self._build_event(log_entry))

        self.start_listen_on(DepositedEventType, log)

    def start_listen_on_withdrawn(self, on_withdrawn) -> None:
        def log(log_entry):
            on_withdrawn(self._build_event(log_entry))

        self.start_listen_on(WithdrawnEventType, log)
