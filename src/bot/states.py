from enum import IntEnum

class States(IntEnum):
    INCOMING_MESSAGE = 1
    WAITING_CHOICE = 2
    WAITING_IMAGE_CHOICE = 3
    WAITING_NEWS_TYPE = 4
    END = 5
