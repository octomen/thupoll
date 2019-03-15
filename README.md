[![Build Status](http://thupoll.liinda.ru:8090/api/badges/octomen/thupoll/status.svg)](http://thupoll.liinda.ru:8090/octomen/thupoll)

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

or

```bash
docker-compose run --rm --entrypoint "pytest -v" test 
```
