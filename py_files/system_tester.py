import DB
import os

os.environ['POSTGRES_USER'] = 'myUser'
os.environ['POSTGRES_PASSWORD'] = 'myPassword'
os.environ['POSTGRES_DB'] = 'test_db'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_PORT'] = '5432'

