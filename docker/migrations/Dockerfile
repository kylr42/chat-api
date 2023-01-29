FROM python:3.9.5

# set the working directory in the container
RUN mkdir -p /usr/src/postgres_migrations/
WORKDIR /usr/src/postgres_migrations/

# create the app user
RUN addgroup --system app && adduser --system --group app   #  going to create a group and a user.

# following up, we will install system and python dependencies.
RUN apt-get update \
  && apt-get install -y --no-install-recommends dos2unix \
  && apt-get clean

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# upgrade pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install poetry
COPY poetry.lock pyproject.toml /usr/src/postgres_migrations/
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

# copy project
COPY . /usr/src/postgres_migrations/

# wait for postgres to be ready
RUN chmod +x scripts/wait-for-server.sh

# convert scripts to unix format
RUN dos2unix scripts/*

# chown all the files to the app user
RUN chown -R app:app /usr/src/postgres_migrations/
