# Contributing to the Orderlie Project.

We're glad to have you contribute to the Orderlie Project. This repository contains the backend codebase for orderlie
that uses [FastAPI](https://fastapi.tiangolo.com/) + [postgres](https://www.postgresql.org/)

## Development setup

This project is easiest to setup with `docker`. Create a new `.env` file in the project's root that matches the
`.env.sample`. (Note if you're using `docker`, `POSTGRES_HOST=database` and `POSTGRES_HOST=5432` in the `.env` file).

After cloning this repository, branch off to your local branch

```bash
git checkout -b my-branch
```

Spin up a docker container

```bash
docker compose up --build -d
```

Viola! you can visit [http://localhost:8082](http://localhost:8082)
Happy contributing!

### Setting up without docker

Without `docker`, you'll need to have `pipenv` installed. If you don't have `pipenv`,
you can install it with `pip install pipenv`. You'll also need to have `postgres`
installed. Provide the credentials to connect to the `postgres` database in a
`.env` file which you'll have to create in the project's root to match the
`.env.sample` file.

After cloning this repository, branch off to your local branch

```bash
git checkout -b my-branch
```

Install the project's dependencies

```bash
pipenv install
```

Switch to the project's virtual environment

```bash
pipenv shell
```

Start up the development server.

```bash
uvicorn main:app --host 0.0.0.0 --port 8082 --reload
```

Viola! you can visit [http://localhost:8082](http://localhost:8082)
Happy contributing!
