FROM tiangolo/uvicorn-gunicorn:python3.11

LABEL maintainer="Gbenga Adeyi <adeyigbenga005@gmail.com>"

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --system

COPY . /app