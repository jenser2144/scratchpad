FROM python:3.10-slim-buster

RUN mkdir -p /src

RUN apt-get update
RUN apt-get install -y --no-install-recommends libpq-dev python3-dev
RUN apt-get install -y --no-install-recommends gcc
RUN apt-get install -y --no-install-recommends git

RUN pip install --upgrade pip
COPY ./deploy/requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /src

# create the app user
RUN addgroup app
RUN useradd -g app app

COPY ./deploy/entrypoint.sh /src/entrypoint.sh

# chown all the files to the app user
RUN chown -R app:app /src
RUN chmod 770 /src/entrypoint.sh

COPY ./deploy/profiles.yml home/app/.dbt/profiles.yml

ARG HOST
ARG USER
ARG PASS
ENV HOST $HOST
ENV USE $USER
ENV PASS $PASS

RUN cd /src/test_dbt_project/ && dbt deps --profiles-dir /home/app/.dbt/
RUN chown -R app:app home/app/
RUN chown -R app:app /src

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]
