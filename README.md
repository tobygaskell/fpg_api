# FPG API

This is a backend API for the FPG app. It is the link between the front end and the database.

## API Docs

Documentation and endpoint testing can be found [here.](http://127.0.0.1:5000/apidocs/#)

## Release Pattern

![alt text](image-1.png)

## Endpoints

#### GET

- current_round
- get_available_choices
- get_choices
- get_fixtures
- get_player_info
- get_points
- get_previous_choices
- get_previous_points
- get_rolling_standings
- get_round_info
- get_round_results
- get_season_overview
- get_standings
- get_weekly_info
- init_player

#### POST

- make_choice
- update_choice

## Useful commands

`ps aux | grep fpg` -- This will show you if the api is running in the background on the server

`nohup venv/bin/python fpg_api.py &` -- This will run the api in the background of the server

`cat nohup.out` -- This will allow you to see the output of the api

### To Gracefully restart the deployment after the docker image is updated

```
kubectl rollout restart deployment fpg-api -n testing
kubectl rollout restart deployment fpg-api -n prod
```

### spin up local docker env

```
docker build -t fpg .
docker run -p 8000:8000 --env-file .env fpg
```
