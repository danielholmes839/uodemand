from typing import List
from app.db import Workout
from .middleware import ObjectTypeWithContext, Context


group = ObjectTypeWithContext('WorkoutGroup')


@group.field('first')
def resolve_id(parent: List[Workout], _):
    return parent[0]


@group.field('last')
def resolve_last(parent: List[Workout], _):
    return parent[-1]


@group.field('workouts')
def resolve_workouts(parent: List[Workout], _):
    return parent
