FROM python:3.6.4-stretch

RUN pip install -U pip

RUN mkdir -p /code/
WORKDIR /code/

COPY ./demo_polls/ /code/demo_polls/
COPY ./setup.py /code/
COPY ./requirements.txt /code/

RUN pip install -e .

ENV POLLS_DEBUG=0
ENV POLLS_HOST=0.0.0.0
ENV POLLS_PORT=5000

ENV POLLS_DB_HOST=postgres
ENV POLLS_DB_USER=polls
ENV POLLS_DB_PASSWORD=password
ENV POLLS_DB_NAME=polls

ENTRYPOINT ["/usr/local/bin/polls"]
CMD ["serve"]
