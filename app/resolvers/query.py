from sqlalchemy import asc
from app.db import Workout
from .middleware import ObjectTypeWithContext, Context
from .scalars import Cursor
from .pagination import WorkoutPage, paginate_workouts_forward, paginate_workouts_backward


query = ObjectTypeWithContext('Query')


@query.field('workouts')
def resolve_workouts(
    _,
    ctx: Context,
    first: int = None,
    last: int = None,
    after: Cursor = None,
    before: Cursor = None,
) -> WorkoutPage:
    """ Relay pagination for workout data points """
    if first is not None:
        if first <= 0:
            raise Exception('"first" must be greater than 0')

        # Paginate forward
        return paginate_workouts_forward(ctx, first, after)

    if last is not None:
        if last <= 0:
            raise Exception('"last" must be greater than 0')

        # Paginate backward
        return paginate_workouts_backward(ctx, last, before)


@query.field('workout', rename={'id': 'workout_id'})
def resolve_workout(_, ctx: Context, workout_id: int):
    return ctx.db.query(Workout).filter(Workout.id == workout_id).first()


@query.field('workoutGroup')
def resolve_group(_, ctx: Context, barcode: int):
    workouts = ctx.db.query(Workout) \
        .filter(Workout.barcode == barcode) \
        .order_by(asc(Workout.timestamp)).all()

    print(workouts)
    if len(workouts) > 0:
        return workouts
