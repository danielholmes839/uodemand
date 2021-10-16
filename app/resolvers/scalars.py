from ariadne import ScalarType
from base64 import b64encode, b64decode
from datetime import datetime
from app.db import Workout

iso8601 = ScalarType('ISO8601')


@iso8601.serializer
def serialize_datetime(dt: datetime) -> str:
    return dt.isoformat()


@iso8601.value_parser
def parse_datetime_value(value: str) -> datetime:
    if value:
        return datetime.fromisoformat(value)


@iso8601.literal_parser
def parse_datetime_literal(ast):
    value = str(ast.value)
    return parse_datetime_value(value)


cursor = ScalarType('CURSOR')


class Cursor:
    def __init__(self, time: datetime, timestamp: datetime):
        self.time = time
        self.timestamp = timestamp

    def serialize(self) -> str:
        time_iso = self.time.isoformat()
        timestamp_iso = self.timestamp.isoformat()
        dt = f'{time_iso},{timestamp_iso}'

        return b64encode(bytes(dt, 'utf-8')).decode()

    @staticmethod
    def deserialize(serialized: str):
        dt = b64decode(serialized).decode().split(',')
        time = datetime.fromisoformat(dt[0])
        timestamp = datetime.fromisoformat(dt[1])

        return Cursor(time, timestamp)

    @staticmethod
    def now():
        dt = datetime.utcnow()
        return Cursor(dt, dt)

    @staticmethod
    def from_workout(workout: Workout):
        return Cursor(workout.time, workout.timestamp)


@cursor.serializer
def serialize_cursor(c: Cursor) -> str:
    return c.serialize()


@cursor.value_parser
def parse_cursor_value(serialized: str) -> Cursor:
    if serialized:
        return Cursor.deserialize(serialized)


@cursor.literal_parser
def parse_cursor_literal(ast):
    encoded_dt = str(ast.value)
    return parse_cursor_value(encoded_dt)
