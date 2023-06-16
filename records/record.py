from enum import Enum
from abc import ABC, abstractmethod


class Record(ABC):
    def __init__(self, record_type):
        self.record_type: RecordType = record_type

    @abstractmethod
    def json_serialize(self):
        pass

    @abstractmethod
    def get_dict(self):
        pass


class RecordType(Enum):
    NOTE = 1
    USER_DATA = 2
    SIMPLE_TEST = 3
    GENESIS = 4
