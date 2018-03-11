# Python Docker development environment example

This project is based on [aiohttp polls example](https://github.com/aio-libs/aiohttp/tree/master/demos/polls) powered by [aiohttp](https://aiohttp.readthedocs.io/en/stable/), [jinja2](http://jinja.pocoo.org/docs/2.10/), [SQLAlchemy](https://www.sqlalchemy.org/) and [aiopg](http://aiopg.readthedocs.io/en/stable/).

Environment features:

* ✅ Development workflow powered by Docker and docker-compose
* ✅ [migrate](https://github.com/mattes/migrate) to manage database migrations
* ✅ [pytest](https://docs.pytest.org/en/latest/) to execute Python tests with [sql fixtures](demo_polls/conftest.py) (`questions_fixtures`, `choices_fixtures`)
* ✅ [task](https://github.com/go-task/task) - A task runner / simpler Make alternative written in Go
* ✅ [production deployment](prod_sample/) docker-compose example

## Prerequisites

* [Docker](https://docs.docker.com/engine/) and [docker-compose](https://docs.docker.com/compose/)
* [task](https://github.com/go-task/task)

Install this prerequisites on OSX with [homebrew](https://brew.sh/index_fr):

```
$ brew tap go-task/tap
$ brew update
$ brew install go-task
$ brew cask install docker
```


## Start development environment

List tasks available:

```
$ task -l
task: Available tasks for this project:
* build-docker: Build harobed/demo_polls Docker image
* clean: 	Stop and destroy all container and databases
* enter: 	Open shell in app container
* init: 	Start and initialize
* init-db: 	Initialize database with sample datas
* tests: 	Execute tests
```

Start and initialize environment:

```
$ task init
...
$ docker-compose  ps
               Name                              Command              State             Ports
------------------------------------------------------------------------------------------------------
dockerpythonexample_app_1             sleep infinity                  Up       0.0.0.0:32804->5000/tcp
dockerpythonexample_migrate_1         sleep 10000d                    Up
dockerpythonexample_postgres-test_1   docker-entrypoint.sh postgres   Up       5432/tcp
dockerpythonexample_postgres_1        docker-entrypoint.sh postgres   Up       5432/tcp
dockerpythonexample_wait_postgres_1   /wait                           Exit 0
```

Execute tests:

```
$ task tests
================================================ test session starts =================================================
platform linux -- Python 3.6.4, pytest-3.4.2, py-1.5.2, pluggy-0.6.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /code, inifile:
plugins: aiohttp-0.3.0
collected 4 items

demo_polls/test_views.py::test_index[pyloop] PASSED                                                            [ 25%]
demo_polls/test_views.py::test_get_poll[pyloop] PASSED                                                         [ 50%]
demo_polls/test_views.py::test_post_poll[pyloop] PASSED                                                        [ 75%]
demo_polls/test_views.py::test_poll_results[pyloop] PASSED                                                     [100%]

============================================== 4 passed in 1.75 seconds ==============================================
```

Enter in *demo_polls* container and start server:

```
$ task enter
# polls serve
DEBUG:polls:Debug mode enabled
INFO:polls:Serve 0.0.0.0:5000
======== Running on http://0.0.0.0:5000 ========
(Press CTRL+C to quit)
```

In another terminal:

```
$ echo "Browse to http://`docker-compose port app 5000`"
Browse to http://0.0.0.0:32804
```

## Test production deployment

Build production Docker image:

```
$ task build-docker
```

next read [prod_sample/README.md](prod_sample/README.md)
