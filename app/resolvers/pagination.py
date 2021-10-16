from ariadne import ObjectType
from sqlalchemy import asc, desc
from typing import List
from app.db import Workout
from .middleware import Context
from .scalars import Cursor

MAX_PAGE_SIZE = 20


class WorkoutPage:
    def __init__(self, workouts: List[Workout], limit: int):
        self.workouts = workouts
        self.limit = limit

    def edges(self):
        return self.workouts[:self.limit]

    def has_next_page(self):
        return self.limit + 1 == len(self.workouts)


def paginate_workouts_forward(ctx: Context, first: int, after: Cursor = None) -> WorkoutPage:
    first = min(MAX_PAGE_SIZE, first)

    if after is None:
        after = Cursor.now()

    # Query an extra workout that won't be shown to the user. It will be used for hasNextPage
    workouts = ctx.db.query(Workout)\
        .filter(Workout.time > after.time, Workout.timestamp <= after.timestamp)\
        .order_by(desc(Workout.timestamp), asc(Workout.time)).limit(first + 1).all()

    return WorkoutPage(workouts, first)


def paginate_workouts_backward(ctx: Context, last: int, before: Cursor = None):
    last = min(MAX_PAGE_SIZE, last)

    if before is None:
        before = Cursor.now()

    # Query an extra workout that won't be shown to the user. It will be used for hasNextPage
    workouts = ctx.db.query(Workout) \
        .filter(Workout.time < before.time, Workout.timestamp <= before.timestamp) \
        .order_by(desc(Workout.timestamp), desc(Workout.time)).limit(last + 1).all()

    return WorkoutPage(workouts, last)


page_info = ObjectType('PageInfo')
connection = ObjectType('WorkoutConnection')
edge = ObjectType('WorkoutEdge')


@page_info.field('hasPreviousPage')
def resolve_has_previous_page(parent: WorkoutPage, _):
    # TODO but most likely not necessary there will be plenty of data
    return True


@page_info.field('hasNextPage')
def resolve_has_next_page(parent: WorkoutPage, _):
    return parent.has_next_page()


@page_info.field('startCursor')
def resolve_has_next_page(parent: WorkoutPage, _):
    if len(parent.workouts) > 0:
        return Cursor.from_workout(parent.workouts[0])

    return Cursor.now()


@page_info.field('endCursor')
def resolve_has_next_page(parent: WorkoutPage, _):
    if len(parent.workouts) > 0:
        return Cursor.from_workout(parent.workouts[-1])

    return Cursor.now()


@connection.field('pageInfo')
def resolve_page_info(parent: WorkoutPage, _):
    return parent


@connection.field('edges')
def resolve_edges(parent: WorkoutPage, _):
    return parent.edges()


@edge.field('cursor')
def resolve_cursor(parent: Workout, _) -> Cursor:
    return Cursor.from_workout(parent)


@edge.field('node')
def resolve_node(parent: Workout, _) -> Workout:
    return parent
