from app.db import Workout
from .middleware import ObjectTypeWithContext, Context


workout = ObjectTypeWithContext('Workout')


@workout.field('id')
def resolve_id(parent: Workout, _):
    return parent.id


@workout.field('barcode')
def resolve_barcode(parent: Workout, _):
    return parent.barcode


@workout.field('title')
def resolve_title(parent: Workout, _):
    return parent.title


@workout.field('location')
def resolve_location(parent: Workout, _):
    return parent.location


@workout.field('available')
def resolve_available(parent: Workout, _):
    return parent.available


@workout.field('time')
def resolve_time(parent: Workout, _):
    return parent.time


@workout.field('timestamp')
def resolve_timestamp(parent: Workout, _):
    return parent.timestamp


@workout.field('group')
def resolve_group(parent: Workout, ctx: Context):
    return ctx.db.query(Workout).filter(Workout.barcode == parent.barcode).all()


@workout.field('count')
def resolve_count(parent: Workout, ctx: Context):
    # TODO dataloader this maybe
    return ctx.db.query(Workout).filter(Workout.barcode == parent.barcode).count()
