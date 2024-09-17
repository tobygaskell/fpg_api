# fpg_api
This is a backend API for the FPG app


## Post Endpoints 

#### get_score
This endpoint will be used to get the score for a given result  
For example: if a player picked a team that won you would post win and the round params for the given round and this endpoint would return the score breakdown gained from that match. 
```
data = {
    'Player'  : <player name>, 
    'Result'  : 'Win'/'Lose'/'Draw',
    'H2H'     : True/False, 
    'Derby'   : True/False, 
    'DMM'     : True/False, 
    'Doubled' : True/False
    }
```
```
returns = {
    'Basic': 1, 
    'DMM': 0, 
    'Derby': None, 
    'H2H': 1, 
    'Result': 4, 
    'Sub Total': 2
    }

```


#### get_result

```
data = {'':'', 
        '':'', 
        }
```
```
returns = {'':'', 
           '':'', 
           }
```

#### get_round_info

```
data = {'':'', 
        '':'', 
        }
```
```
returns = {'':'', 
           '':'', 
           }
```

#### make_choice

```
data = {'':'', 
        '':'', 
        }
```
```
returns = {'':'', 
           '':'', 
           }
```


## Get Endpoints

#### get_choice
```
returns = {'':'', 
           '':'', 
           }
```

#### get_teams

```
returns = {'':'', 
           '':'', 
           }
```