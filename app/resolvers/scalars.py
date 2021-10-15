from ariadne import ScalarType
from base64 import b64encode, b64decode
from datetime import datetime

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


@cursor.serializer
def serialize_cursor(dt: datetime) -> str:
    dt = dt.isoformat()
    return b64encode(bytes(dt, 'utf-8')).decode()


@cursor.value_parser
def parse_cursor_value(encoded_dt: str) -> datetime:
    if encoded_dt:
        dt = b64decode(encoded_dt).decode()
        return datetime.fromisoformat(dt)


@cursor.literal_parser
def parse_cursor_literal(ast):
    encoded_dt = str(ast.value)
    return parse_cursor_value(encoded_dt)
