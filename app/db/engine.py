import os
from sqlalchemy import create_engine

name = os.getenv('POSTGRES_NAME', 'uottawa-workouts')
user = os.getenv('POSTGRES_USER', 'postgres')
password = os.getenv('POSTGRES_PASSWORD', 'postgres')
host = os.getenv('POSTGRES_HOST', 'localhost')
port = os.getenv('POSTGRES_PORT', '5432')

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}')
