from ariadne import make_executable_schema, load_schema_from_path, asgi
from .middleware import ContextMiddleware
from .query import query
from .pagination import edge, connection, page_info
from .workout import workout
from .workout_group import group
from .scalars import iso8601, cursor


sdl = load_schema_from_path('./app/resolvers/schema.graphql')

resolvers = make_executable_schema(
    sdl,
    query,
    workout,
    group,
    iso8601,
    cursor,
    edge,
    connection,
    page_info
)

graphql_endpoint = asgi.GraphQL(resolvers, debug=True, extensions=[ContextMiddleware])
