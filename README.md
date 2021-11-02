# DatabaseProcessing

> A Python+Postgres system docker based able to read a specific text file database.

## Database

<img src="https://github.com/pedrohames/DatabaseProcessing/blob/main/DB_ER_Diagram.jpg" alt="ER diagram">

## Requirements
* Docker environment installed, you can install it using docker_install.sh file as below.
```
sudo ./docker_install.sh
```

## How to use
```
git clone https://github.com/pedrohames/DatabaseProcessing.git
cd DatabaseProcessing
sudo docker-compose up
```
## Tips
* ./pgdata/ must be there even if it is empty, this database is used to persist the data after stop postgres service.
* If you want, some environment vars like database name, host, and port can be changed at docker-compose.yml.


## Next steps
* Stores and Relationships bulk INSERT.
* Add a thread to process the relationships between Customers and Stores.
* Create tests that compare data from database and text database file.

