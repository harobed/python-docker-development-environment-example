Test production **demo_polls** Docker image:

```
$ docker-compose up -d postgres
$ docker-compose run --rm wait_postgres
$ docker-compose run --rm migrate
$ cat ../sample_data.sql | docker exec -i --user postgres `docker-compose ps -q postgres` psql polls
$ docker-compose up -d app
$ echo "Browse to http://`docker-compose port app 5000`"
```
