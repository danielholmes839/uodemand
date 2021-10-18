import os
import sys
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        if '--docker' in sys.argv:
            print('Reading docker.env')
            load_dotenv('docker.env')
        else:
            print('Reading .env')
            load_dotenv()

        self.host = os.getenv('HOST', '0.0.0.0')
        self.port = int(os.getenv('PORT', 8000))

        self.db_name = os.getenv('POSTGRES_DB', 'uottawa-workouts')
        self.db_user = os.getenv('POSTGRES_USER', 'postgres')
        self.db_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
        self.db_host = os.getenv('POSTGRES_HOST', 'localhost')
        self.db_port = os.getenv('POSTGRES_PORT', '5432')

        self.aws_backups_enabled = bool(os.getenv('AWS_ENABLED', False))
        self.aws_bucket_name = os.getenv('AWS_BUCKET', 'uottawa-demand')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY', '')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_KEY', '')

    def db_uri(self) -> str:
        return f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'


settings = Settings()
