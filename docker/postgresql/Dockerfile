FROM postgres:13.1

# create the app user
RUN addgroup --system postgres && adduser --system --group postgres   #  going to create a group and a user.

# following up, we will install system and postgres dependencies.
RUN apt-get update && \
    apt-get install -y --no-install-recommends dos2unix

# copy the dependencies file to the working directory
ADD ./scripts/init.postgres.sh /docker-entrypoint-initdb.d/init-db.sh

# convert scripts to unix format
RUN dos2unix /docker-entrypoint-initdb.d/init-db.sh

# chown all the files to the app user
RUN chown -R postgres:postgres /docker-entrypoint-initdb.d

# change to the app user
USER postgres
