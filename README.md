[![Build Status](http://drone.liinda.ru/api/badges/octomen/thupoll/status.svg)](http://drone.liinda.ru/octomen/thupoll)

ThuPoll


## Installation

Install docker


## Run server locally

1. Run server

```bash
docker-compose up
```

2. Check [url](http://localhost:5000) 



## Testing 

```bash
# run test docker container
docker-compose up -d test

# run tests
docker-compose exec test pytest
```

    
## Migration-usecase
0) Start and connect to test server
    ```bash
    docker-compose up -d test
    docker-compose exec test bash
    ```
    
   Next commands execute in this shell - in this `test`-container
    
1) Refesh your local DB according structure in project

    ```bash
    flask db upgrade
    ```

2) Change DB-structure in `thupoll/models.py`

3) Autogenerate migration
    ```bash
    flask db migrate
    ```

4) Migrate local DB:

    ```bash
    flask db upgrade
    ```
