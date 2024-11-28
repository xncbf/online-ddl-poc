FROM flyway/flyway:latest

COPY migrations/sql /flyway/sql
COPY flyway.conf /flyway/conf
