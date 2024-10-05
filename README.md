# fpg_api
This is a backend API for the FPG app

## Useful commands on how to run this
```ps aux | grep fpg``` -- This will show you if the api is running in the background on the server  

```nohup venv/bin/python fpg_api.py &``` -- This will run the api in the background of the server  

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


# GET

## get_round_info
Parameters 

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | True     |
| round_id  | 10      | False    |

```
returns = {'Round'  : 10, 
           'Double' : True/False, 
           'DMM'    : True/False, 
           'Cut Off': '2024-10-09 10:50'}
```

## get_choices
Parameters 

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | True     |
| round_id  | 10      | False    |

```
returns = {<player_id>:<choice>}

eg = {2: 'Manchester United', 
      3: 'Manchester City', 
      ...}

```

## init_player
Parameters 

| Name      | Example          | Optional |
| --------- | ---------------- | -------- |
| email     | test@example.com | False     |
```
returns = {'player_id': 3}
```

## engine
Parameters: 

| Name | Example | Optional |
| ---- | ------- | -------- |
| None | None    | None     |

```
returns = {'Everyday Ran':True}
```

## get_fixtures
Parameters 

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | True     |
| round_id  | 10      | False    |

```
returns = [{'FIXTURE_ID': 1208082,
            'HOME_TEAM': 'Aston Villa',
            'AWAY_TEAM': 'Manchester United',
            'KICKOFF': 1728219600000,
            'LOCATION': 'Villa Park',
            'ROUND': 7,
            'SEASON': 2024,
            'DERBY': 0,
            'HOME_LOGO': 'https://media.api-sports.io/football/teams/66.png',
            'AWAY_LOGO': 'https://media.api-sports.io/football/teams/33.png'},
           ...]
```

__returns:__

| fixture_id | home_team | away_team | kickoff | location | round | season|derby|home_logo|away_logo|
| ----- | --------- | --------- | ------- | -------- | ----- | ----- | --- | ------- | ------- |
| 13232 | Man C  | Man U  | 2024-09-10 12:30 | Old Trafford | 1 | 2024  | True    | string  | string  |
| 23242 | Man U  | Man C  | 2024-09-10 12:30 | Old Trafford | 1 | 2024  | True    | string  | string  |
| 32343 | Spurs  | Villa  | 2024-09-10 12:30 | Old Trafford | 1 | 2024  | True    | string  | string  |

## get_available_choices
Parameters 

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | False     |

```
returns = [{'TEAM_NAME': 'Manchester United'},
           {'TEAM_NAME': 'Newcastle'},
           ...]
```
__returns:__

| TEAM_NAME         |
| ----------------- |
| Manchester United |
| Manchester City   |
| Newcastle United  |


## current_round
Parameters 

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | True     |
```
returns = {'Round ID':3}
```

## get_standings
Parameters 

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | True     |
```
returns = [{'Position': 1,
            'player_id': 11,
            'User': 'XXXXX',
            'Goal Diff': 7,
            'Score': 4},
           ...]
```
__returns:__

| Position | player_id | User | Goal Diff | Score |
| ---------| --------- | ---- | --------- | ----- |
| 1        | 10        | XXXX | 10        | 7     |
| 2        | 11        | XXXX | 3         | 4     |
| 3        | 41        | XXXX | -1        | 2     |

## get_points
Parameters 

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | True     |
| round_id  | 10      | False    |

```
returns = [{'player_id': 25,
            'User': 'XXXXX',
            'Choice': 'Bournemouth',
            'Result': 'Won',
            'Basic': 1,
            'Head 2 Head': 0,
            'Derby': 1,
            'Draw Means More': 0,
            'Subtotal': 2,
            'Total': 2},
           ...]
```
__returns:__

| player_id | User | Choice | Result | Basic | Head 2 Head | Derby | Draw Means More | Subtotal | Total |
| --------- | ---- | ------ | ------ | ----- | ----------- | ----- | --------------- | -------- | ----- |
| 1         | XXX  | Man U  | Won    | 1     | 1           | 1     | 0               | 3        | 6     |
| 2         | XXX  | Man C  | Lost   | -1    | -1          | -1    | 0               | -3       | -6    |
| 3         | XXX  | Villa  | Draw   | 0     | 0           | 0     | 2               | 2        | 4     |


## get_rolling_standings
Parameters 

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | True     |

```
returns = [{'Position': 1,
            'player_id': 10,
            'User': 'XXXXXXXX',
            'Goal Diff': 1.0,
            'Score': 2.0,
            'round': 1},
           ...]
```

__returns:__

| Position | player_id | User | Goal Diff | Score | round |
| ---------| --------- | ---- | --------- | ----- | ----- |
| 1        | 10        | XXXX | 10        | 7     | 10    |
| 2        | 11        | XXXX | 3         | 4     | 9     |
| 3        | 41        | XXXX | -1        | 2     | 10    |



## get_previous_choices
__Parameters__

| Name      | Example | Optional |
| --------- | ------- | -------- |
| player_id | 6       | False    |


```
returns = [{'Choice': 'Manchester United', 
            '1st Pick': 1, 
            '2nd Pick': 0},
           ...]
```

__returns:__

| Choice            | 1st Pick | 2nd Pick  |
| ---------------   | -------- | --------- |
| Manchester City   | True     | False     |
| Manchester United | True     | True      |
| Newcastle United  | True     | False     |


# POST 

## make_choice
```
data = {'Choice'  : 'Manchester United', 
        'Player'  : 3,
        'Round'   : 10}
```
```
returns = {'Submitted':True/False}
```

## update_choice
```
data = {'Choice'  : 'Manchester United', 
        'Player'  : 3, 
        'Round'   : 10}
```
```
returns = {'Updated':True/False}
```