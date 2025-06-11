# FPG API

This is a backend API for the FPG app. It is the link between the front end and the database.

## Useful commands

### Gracefully restart the K8s deployment

```
kubectl rollout restart deployment fpg-api -n testing
kubectl rollout restart deployment fpg-api -n prod
```

### Spin up local docker env

```
docker build -t fpg .
docker run -p 8000:8000 --env-file .env fpg
```

### Spin up a development server

```
app.run(debug=True, host='0.0.0.0', port=5001)
```
