from sqlalchemy import asc, desc
from datetime import datetime
from app.db import Workout
from .middleware import ObjectTypeWithContext, Context


query = ObjectTypeWithContext('Query')


@query.field('workouts')
def resolve_workouts(_, ctx: Context, first: int, after: datetime = None):
    if after is None:
        after = datetime.utcnow()

    workouts = ctx.db.query(Workout)\
        .filter(Workout.time > after)\
        .order_by(desc(Workout.timestamp), asc(Workout.time))\
        .limit(min(10, first))

    paginated = {
        'pageInfo': {},
        'edges': [{
            'node': workout,
            'cursor': workout.time
        } for workout in workouts]
    }

    return paginated