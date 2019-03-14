[![Build Status](http://thupoll.liinda.ru:8090/api/badges/octomen/thupoll/status.svg)](http://thupoll.liinda.ru:8090/octomen/thupoll)

ThuPoll


## Installation

Install docker


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
