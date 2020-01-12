from .events import BlockchainEvent

ExchangeRateChangedEventType = "ExchangeRateChanged"


class GatewayEvent(BlockchainEvent):
    def __init__(self, web3_event, current_blocknumber: int, timestamp: int):
        super().__init__(web3_event, current_blocknumber, timestamp)
        self.gateway_address = web3_event.get("address")


class ExchangeRateChangedEvent(GatewayEvent):
    @property
    def changed_exchange_rate(self):
        return self._web3_event.get("args").get("_changedExchangeRate")


event_builders = {ExchangeRateChangedEventType: ExchangeRateChangedEvent}


standard_event_types = [ExchangeRateChangedEventType]
