# FPG API

This is a backend API for the FPG app. It is the link between the front end and the database.

## Useful commands

### Gracefully restart the K8s deployment

```
kubectl rollout restart deployment fpg-api -n testing
kubectl rollout restart deployment fpg-api -n prod
```

### To Run Pytests Locally

`
uv run pytest

```

### Build & Run docker image locally

```

docker build -t fpg .
docker run -p 8000:8000 --env-file .env fpg

```

### To run locally so it will refresh with changes

```

docker compose up --build

```

```
