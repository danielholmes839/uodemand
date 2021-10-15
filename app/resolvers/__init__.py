from ariadne import make_executable_schema, load_schema_from_path, asgi
from .middleware import ContextMiddleware
from .query import query
from .workout import workout
from .scalars import iso8601, cursor


sdl = load_schema_from_path('./app/resolvers/schema.graphql')

resolvers = make_executable_schema(
    sdl,
    query,
    workout,
    iso8601,
    cursor,
)

graphql_endpoint = asgi.GraphQL(resolvers, debug=True, extensions=[ContextMiddleware])
