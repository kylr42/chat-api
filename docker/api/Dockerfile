FROM python:3.9.5

# set the working directory in the container
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

# create the app user
RUN addgroup --system app && adduser --system --group app   #  going to create a group and a user.

# following up, we will install system and python dependencies.
RUN apt-get update \
  && apt-get -y install netcat gcc libpq-dev \
  && apt-get clean

# copy the dependencies file to the working directory
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# upgrade pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install poetry
COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false \
    && poetry install --only main

# copy project
COPY . /usr/src/app/

# chown all the files to the app user
RUN chown -R app:app /usr/src/app/

# change to the app user
USER app
