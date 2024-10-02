# fpg_api
This is a backend API for the FPG app

## Useful commands on how to run this
```ps aux | grep fpg``` -- This will show you if the api is running in the background on the server  

```nohup venv/bin/python fpg_api.py &``` -- This will run the api in the background of the server  

```cat nohup.out``` -- This will allow you to see the output of the api

## Post Endpoints 
- get_score             -- Not Needed -- POST
- get_result            -- Not Needed -- POST
- get_choices           -- Not Needed -- POST
- init_round            -- Not Needed -- POST
- get_logo              -- Not Needed -- POST
- inti_results          -- Not Needed -- POST
- calculate_scores      -- Not Needed -- POST 

- engine                              -- GET
- get_current_round                   -- GET
- get_standings                       -- GET
- get_rolling_standings               -- GET

- init_player                         -- POST
- get_previous_choices                -- POST
- get_available_choices               -- POST
- get_round_info                      -- POST
- get_fixtures                        -- POST
- get_points                          -- POST

- make_choice                         -- POST
- update_choice                       -- POST

---
# GET

#### engine (GET)
```
returns = {'Everyday Ran':True}
```

#### get_current_round (GET)
```
returns = {'Round ID':3}
```

#### get_standings (GET)
```
returns = {'':'', 
           '':''}
```

### get_rolling_standings (GET)
```
returns = {'':'', 
           '':''}
```

#### init_player (POST)
```
data = {'Email':'Test@Test.com'}
```
```
returns = {'player_id':3}
```

### get_previous_choices (POST)
```
data = {'Player':3}
```
```
returns = {'':'', 
           '':''}
```

#### get_available_choices (POST)
```
data = {'Player':3}
```
```
returns = {'':'', 
           '':''}
```

#### get_round_info (POST)
```
data = {'Round':10}
```
```
returns = {'Round'  : 10, 
           'Double' : True/False, 
           'DMM'    : True/False, 
           'Cut Off': '2024-10-09 10:50'}
```

#### get_fixtures (POST)
```
data = {'Round':10}
```
```
returns = {'':'', 
           '':''}
```

#### get_points (POST)
```
data = {'Round':10}
```
```
returns = {'':'', 
           '':''}
```

--- 
# POST 

#### make_choice (POST)
```
data = {'Choice'  : 'Manchester United', 
        'Player'  : 3,
        'Round'   : 10}
```
```
returns = {'Submitted':True/False}
```

#### update_choice (POST)
```
data = {'Choice'  : 'Manchester United', 
        'Player'  : 3, 
        'Round'   : 10}
```
```
returns = {'Updated':True/False}
```