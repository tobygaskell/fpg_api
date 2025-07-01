# FPG API

This is a backend API for the FPG app. It is the link between the front end and the database.

## Useful commands

### Gracefully restart the K8s deployment

```
kubectl rollout restart deployment fpg-api -n testing
kubectl rollout restart deployment fpg-api -n prod
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

| Endpoint                 | Season Added | Tested |
| ------------------------ | ------------ | ------ |
| current_round            | N/A          | N/A    |
| deactivate_notifications | N/A          | N/A    |
| get_available_choices    | True         | False  |
| get_choices              | True         | False  |
| get_fixtures             | True         | False  |
| get_player_info          | True         | False  |
| get_points               | True         | False  |
| get_previous_choices     | True         | False  |
| get_previous_points      | True         | False  |
| get_rolling_standings    | True         | False  |
| get_round_info           | True         | False  |
| get_round_results        | True         | False  |
| get_season_overview      | True         | False  |
| get_standings            | True         | False  |
| get_weekly_info          | True         | False  |
| get_username             | N/A          | N/A    |
| init_player              | N/A          | N/A    |
| init_notifications       | N/A          | N/A    |
| init_player_app          | N/A          | N/A    |
| make_choice              | True         | False  |
| update_choice            | True         | False  |
| update_username          | N/A          | N/A    |
