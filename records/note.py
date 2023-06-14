import json

from records.record import Record, RecordType


class Note(Record):
    def __init__(self, clinical_note):
        super().__init__(record_type=RecordType.NOTE)
        self.clinical_note = clinical_note

    def json_serialize(self):
        data = {
            'record_type': self.record_type.value,
            'clinical_note': self.clinical_note
        }
        return json.dumps(data)

    @staticmethod
    def json_deserialize_note(json_object):
        return Note(json_object['clinical_note'])

