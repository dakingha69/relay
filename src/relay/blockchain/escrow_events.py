from .events import TLNetworkEvent

DepositedEventType = "Deposited"
WithdrawnEventType = "Withdrawn"


class EscrowEvent(TLNetworkEvent):
    def __init__(self, web3_event, current_blocknumber, timestamp, user=None):
        super().__init__(
            web3_event, current_blocknumber, timestamp, from_to_types, user
        )
        self.escrow_address = web3_event.get("address")


class WeiAmountEvent(EscrowEvent):
    @property
    def wei_amount(self):
        return self._web3_event.get("args").get("weiAmount")


class DepositedEvent(WeiAmountEvent):
    @property
    def payee(self):
        return self._web3_event.get("args").get("payee")


class WithdrawnEvent(DepositedEvent):
    pass


event_builders = {
    DepositedEventType: DepositedEvent,
    WithdrawnEventType: WithdrawnEvent,
}


from_to_types = {
    DepositedEventType: ["payee", "payee"],
    WithdrawnEventType: ["payee", "payee"],
}

standard_event_types = [DepositedEventType, WithdrawnEventType]
