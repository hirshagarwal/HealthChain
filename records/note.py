import json

from records.record import Record, RecordType


class Note(Record):
    def __init__(self, clinical_note):
        super().__init__(record_type=RecordType.NOTE)
        self.clinical_note = clinical_note

    def json_serialize(self):
        return json.dumps(self.get_dict())

    def get_dict(self):
        return {
            'record_type': self.record_type.name,
            'clinical_note': self.clinical_note
        }

    @staticmethod
    def json_deserialize_note(json_string):
        json_object = json.loads(json_string)
        return Note(json_object['clinical_note'])

