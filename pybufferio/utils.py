from enum import Enum

class Direction(Enum):
    FROM_START = 1
    FROM_END   = -1

def serialize_index(index):
    """Serialize index"""
    return hex(index).replace('0x', '')
