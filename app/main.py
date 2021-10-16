import pytz
from datetime import datetime

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi_utils import tasks
from sqlalchemy import desc, asc, func
from sqlalchemy.orm import Session

from app.db import Workout, db_context, db_provider
from app.resolvers import graphql_endpoint
from app.scraping import scrape

app = FastAPI()

origins = [
    # 'http://localhost:3000', # TODO: uncomment when working on UI
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_route('/api/graphql', graphql_endpoint)


# @app.on_event('startup')
@tasks.repeat_every(seconds=60*20)
async def scrape_task():
    """ Scrape the uOttawa website every 20 minutes """
    workouts = scrape()

    with db_context() as db:
        for workout in workouts:
            db.add(Workout.from_dict(workout))

        db.commit()


@app.get('/workouts/recent')
async def workouts_recent(db: Session = Depends(db_provider)):
    """ Retrieve the latest 20 data points """
    dt = datetime.utcnow()
    db.query(Workout.id, func.max(Workout.timestamp))\
        .filter(Workout.time > dt)\
        .group_by(Workout.barcode)\
        .subquery()

    workouts = db.query(Workout.barcode, func.count(Workout.barcode), Workout.id).group_by(Workout.barcode).all()

    print(workouts)
    return []


@app.get('/workouts/after')
async def workouts_after(after: str = None, limit: int = 10, db: Session = Depends(db_provider)):
    print(after)
    if after is None:
        dt = datetime.utcnow().replace(tzinfo=pytz.utc)
    else:
        dt = datetime.fromisoformat(after)

    limit = min(limit, 10)
    workouts = db.query(Workout).filter(Workout.time > dt).order_by(Workout.time).limit(limit)
    return [workout.to_dict() for workout in workouts]


@app.get('/workouts/{barcode}')
async def workouts_by_barcode(barcode: int, db: Session = Depends(db_provider)):
    """ Retrieve all data points for the given bar code """
    workouts = db.query(Workout).filter(Workout.barcode == barcode).order_by(Workout.timestamp).all()
    return [workout.to_dict() for workout in workouts]


@app.get('/download')
async def download(db: Session = Depends(db_provider)):
    """ Retrieve all data points for the given bar code """
    return [workout.to_dict() for workout in db.query(Workout).all()]
