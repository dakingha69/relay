from .events import BlockchainEvent


class GatewayEvent(BlockchainEvent):
    def __init__(self, web3_event, current_blocknumber: int, timestamp: int):
        super().__init__(web3_event, current_blocknumber, timestamp)
        self.gateway_address = web3_event.get("address")

event_builders = {}


standard_event_types = []
