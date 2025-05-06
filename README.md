# fpg_api
This is a backend API for the FPG app

## Useful commands on how to run this
```ps aux | grep fpg``` -- This will show you if the api is running in the background on the server  

```nohup venv/bin/python fpg_develop_api.py &``` -- This will run the api in the background of the server  

```cat nohup.out``` -- This will allow you to see the output of the api

## Endpoints 
- get_round_info
- get_choices
- init_player
- engine
- get_fixtures
- get_available_choices
- current_round
- get_standings
- get_points
- get_rolling_standings
- get_previous_choices
- make_choice
- update_choice