import os
import sys
import subprocess
import shlex

import pytest
from aiohttp import web
from sqlalchemy import create_engine

from . import server

here = os.path.abspath(os.path.dirname(__file__))


def execute_migrate(command):
    subprocess.run(
        shlex.split('migrate -path=migrate/ -database postgres://%s:%s@%s:5432/%s?sslmode=disable %s' % (
            os.environ['POLLS_DB_USER'],
            os.environ['POLLS_DB_PASSWORD'],
            os.environ['POLLS_DB_HOST'],
            os.environ['POLLS_DB_NAME'],
            command
        )),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def execute_sqlfile(engine, sql_file):
    with open(os.path.join(here, 'sql-fixtures', sql_file), "r") as f:
        engine.execute(f.read())

@pytest.fixture()
def test_db():
    os.environ['POLLS_DB_NAME'] = 'polls-test'
    os.environ['POLLS_DB_USER'] = 'polls-test'
    os.environ['POLLS_DB_PASSWORD'] = 'password'
    os.environ['POLLS_DB_HOST'] = 'postgres-test'

    execute_migrate('drop')
    execute_migrate('up')
    return create_engine(
        'postgresql://%s:%s@%s:5432/%s' % (
            os.environ['POLLS_DB_USER'],
            os.environ['POLLS_DB_PASSWORD'],
            os.environ['POLLS_DB_HOST'],
            os.environ['POLLS_DB_NAME']
        )
    )

@pytest.fixture()
def app(loop):
    return server.get_app(loop)


@pytest.fixture
def http_client(test_db, app, loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(app))

@pytest.fixture
def questions_fixtures(test_db):
    execute_sqlfile(test_db, 'questions.sql')


@pytest.fixture
def choices_fixtures(test_db, questions_fixtures):
    execute_sqlfile(test_db, 'choices.sql')
