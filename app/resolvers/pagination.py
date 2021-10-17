from ariadne import ObjectType
from sqlalchemy import desc
from typing import List
from app.db import Workout
from app.db.engine import engine
from .middleware import Context
from .scalars import Cursor
from datetime import datetime

MAX_PAGE_SIZE = 20


class WorkoutPage:
    def __init__(self, workouts: List[Workout], limit: int):
        self.count = len(workouts)
        self.edges = workouts[:limit]
        self.limit = limit

    def start_cursor(self):
        return Cursor.from_workout(self.edges[0])

    def end_cursor(self):
        return Cursor.from_workout(self.edges[-1])

    def has_next_page(self):
        return self.limit + 1 == self.count


def paginate_workouts_forward(ctx: Context, first: int, after: Cursor = None):
    first = min(MAX_PAGE_SIZE, first)

    if after is None:
        after = Cursor.now()

    params = {'dt': after.time, 'limit': first + 1}
    statement = """
        SELECT * FROM (
            SELECT DISTINCT ON (barcode) *
            FROM workout
            WHERE time > :dt 
            ORDER BY barcode, timestamp DESC
        ) t ORDER BY "time" ASC LIMIT :limit
    """

    rows = ctx.db.execute(statement, params)
    workouts = [Workout.from_tuple(row) for row in rows]

    if len(workouts) == 0:
        return None

    return WorkoutPage(workouts, first)


def paginate_workouts_backward(ctx: Context, last: int, before: Cursor = None):
    last = min(MAX_PAGE_SIZE, last)

    if before is None:
        before = Cursor.now()

    # Query an extra workout that won't be shown to the user. It will be used for hasNextPage
    workouts = ctx.db.query(Workout) \
        .filter(Workout.time < before.time, Workout.timestamp <= before.timestamp) \
        .order_by(desc(Workout.timestamp), desc(Workout.time)).limit(last + 1).all()

    if len(workouts) == 0:
        return None

    return WorkoutPage(workouts, last)


page_info = ObjectType('PageInfo')


@page_info.field('hasPreviousPage')
def resolve_has_previous_page(_, __):
    # TODO but most likely not necessary there will be plenty of data
    return True


@page_info.field('hasNextPage')
def resolve_has_next_page(parent: WorkoutPage, _):
    print(parent.has_next_page())
    return parent.has_next_page()


@page_info.field('startCursor')
def resolve_start_cursor(parent: WorkoutPage, _):
    if len(parent.edges) > 0:
        return parent.start_cursor()

    return Cursor.now()


@page_info.field('endCursor')
def resolve_has_next_page(parent: WorkoutPage, _):
    if len(parent.edges) > 0:
        return parent.end_cursor()

    return Cursor.now()


connection = ObjectType('WorkoutConnection')


@connection.field('pageInfo')
def resolve_page_info(parent: WorkoutPage, _):
    return parent


@connection.field('edges')
def resolve_edges(parent: WorkoutPage, _):
    return parent.edges


edge = ObjectType('WorkoutEdge')


@edge.field('cursor')
def resolve_cursor(parent: Workout, _) -> Cursor:
    return Cursor.from_workout(parent)


@edge.field('node')
def resolve_node(parent: Workout, _) -> Workout:
    return parent
