import json

from records.record import Record, RecordType


class Genesis(Record):
    def __init__(self):
        super().__init__(record_type=RecordType.GENESIS)

    def json_serialize(self):
        return json.dumps(self.get_dict_encrypted())

    def get_dict(self):
        return {
            'record_type': self.record_type.name
        }

    @staticmethod
    def deserialize_genesis(json_string):
        return Genesis()
