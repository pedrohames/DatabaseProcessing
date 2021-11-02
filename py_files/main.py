import time
from data_handler import DataHandler
import DB
import os
from system_tester import SystemTester


total_time_st = time.time()

db_setup_st = time.time()
# Reads sql file to setup database
print('Starting database setup')
db_setup_path = os.environ['DATABASE_SETUP_SQL_FILE']

# Wait database to get ready and then set it up.
DB.DB.db_setup(db_setup_path)
db_setup_ft = time.time()
print('Database setup DONE!')
print(f'\t Database setup time: {db_setup_ft - db_setup_st} s.')

print('Starting data processing')
# Get database_path from env var
base_path = os.environ['TXT_BASE_PATH']

# Start processing time measurement
start_time = time.time()

# Read data from txt file database
content = DataHandler.txt_file_read(base_path)

# Data processing
DataHandler.customer_creator(content)
print('Data processing DONE!')

# Finishes processing time measurement
finish_time = time.time()
print(f'\tData processing time: {finish_time-start_time} s')


# Counts database insertions and prints results
test_st = time.time()
print('Starting test')
SystemTester.count_test()
test_ft = time.time()
print(f'\tTesting time: {test_ft-test_st} s')

# Total time
total_time_ft = time.time()
print(f'Total time: {total_time_ft - total_time_st}')
