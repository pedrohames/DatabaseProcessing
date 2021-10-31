import time
from data_handler import DataHandler
import DB
import os

start_time = time.time()

os.environ['POSTGRES_USER'] = 'myUser'
os.environ['POSTGRES_PASSWORD'] = 'myPassword'
os.environ['POSTGRES_DB'] = 'test_db'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_PORT'] = '5432'


db_setup_path = '/home/pedrohames/PycharmProjects/DockerPostgres/tables.sql'
DB.DB.db_setup(db_setup_path)
base_path = '/home/pedrohames/PycharmProjects/DockerPostgres/base_teste.txt'


content = DataHandler.txt_file_read(base_path)
DataHandler.customer_creator(content)

finish_time = time.time()

print(f'Total time: {finish_time-start_time} s')
