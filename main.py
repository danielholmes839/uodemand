import uvicorn
from app import app, settings

if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)
