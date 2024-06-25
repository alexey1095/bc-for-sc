from enum import Enum


class ShipmentStatus(Enum):

    CREATED = 'CREATED'
    CONFIRMED = 'CONFIRMED'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'
