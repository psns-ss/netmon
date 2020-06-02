# netmon

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.

Run dev environment:

```shell script
docker-compose -f docker-compose.dev.yml -d
```

Show logs:

```shell script
docker-compose -f docker-compose.dev.yml logs
```

Show service logs:

```shell script
docker-compose -f docker-compose.dev.yml logs backend
```

all settings are available on .env file

docs are available on localhost/docs

admin panel is available on localhost
