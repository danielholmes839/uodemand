from fastapi import FastAPI
from fastapi_utils import tasks
from scraping import scrape


app = FastAPI()
app.recent = []


@app.on_event('startup')
@tasks.repeat_every(seconds=60*15)
async def scrape_task():
    """ Scrape the uOttawa website every 15 minutes """
    data = scrape()
    app.recent = data


@app.get("data/recent")
async def recent_handler():
    return app.recent
