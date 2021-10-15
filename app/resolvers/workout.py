from app.db import Workout
from .middleware import ObjectTypeWithContext, Context


workout = ObjectTypeWithContext('Workout')


@workout.field('id')
def resolve_id(parent: Workout, _: Context):
    return parent.id


@workout.field('barcode')
def resolve_barcode(parent: Workout, _: Context):
    return parent.barcode


@workout.field('title')
def resolve_title(parent: Workout, _: Context):
    return parent.title


@workout.field('location')
def resolve_location(parent: Workout, _: Context):
    return parent.location


@workout.field('available')
def resolve_available(parent: Workout, _: Context):
    return parent.available


@workout.field('time')
def resolve_time(parent: Workout, _: Context):
    return parent.time


@workout.field('timestamp')
def resolve_timestamp(parent: Workout, _: Context):
    return parent.timestamp


@workout.field('group')
def resolve_group(parent: Workout, ctx: Context):
    return ctx.db.query(Workout).filter(Workout.barcode == parent.barcode).all()
