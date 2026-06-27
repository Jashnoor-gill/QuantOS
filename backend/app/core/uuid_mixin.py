import uuid

class UUIDMixin:
    id: uuid.UUID = uuid.uuid4()