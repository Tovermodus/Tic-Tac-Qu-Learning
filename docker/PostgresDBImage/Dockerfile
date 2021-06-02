FROM postgres:13
COPY docker/TestDBImage/create_tables.sql /docker-entrypoint-initdb.d
COPY docker/TestDBImage/fill_tables.sql /docker-entrypoint-initdb.d
ENV POSTGRES_DB docker
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD secret
ENV PGDATA /var/lib/postgresql/data