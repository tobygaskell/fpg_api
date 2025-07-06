FROM ghcr.io/astral-sh/uv:python3.12-alpine

ADD . /app

WORKDIR /app

RUN ["uv", "sync", "--locked"]

COPY . .

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "wsgi:app"]
