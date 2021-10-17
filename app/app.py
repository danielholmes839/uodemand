from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils import tasks
from app.db import Workout, db_context
from app.settings import settings
from app.s3 import backup
from app.resolvers import graphql_endpoint
from app.scraping import scrape

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# GraphQL endpoint
app.add_route('/api/graphql', graphql_endpoint)


@app.on_event('startup')
@tasks.repeat_every(seconds=60*20)
async def scrape_task():
    """ Scrape the uOttawa website every 20 minutes """
    workouts, timestamp = scrape()
    print('Scraping uOttawa...')
    print(f'Scraped {len(workouts)} records')

    if len(workouts) == 0:
        return

    if settings.aws_backups_enabled:
        backup(workouts, timestamp)

    with db_context() as db:
        for workout in workouts:
            db.add(Workout.from_dict(workout))

        db.commit()

    print('Successfully uploaded records')
