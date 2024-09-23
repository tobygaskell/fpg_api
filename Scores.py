import Round
import Results 
import Games 
import Choices
import utils


def get_score(result, h2h, derby, dmm, doubled): 
    '''
    '''
    print(result)
    score, basic_score = get_basic(result)

    score, h2h_score = get_h2h(score, h2h, result)
    
    score, derby_score = get_derby(score, derby, result)

    score, dmm_score = get_dmm(score, dmm, result)

    subtotal = score

    score = get_doubled(score, doubled)

    return score, basic_score, h2h_score, derby_score, dmm_score, subtotal


def assign_score(score, mapping, result): 
    '''
    '''
    return score + mapping[result], mapping[result]

def get_basic(result): 
    '''
    '''
    mapping = {'Win':1, 
               'Loss':-1, 
               'Draw':0}

    score, basic_score = assign_score(0, mapping, result)

    return score, basic_score

def get_h2h(score, h2h, result): 
    '''
    '''
    h2h_score = None

    if h2h: 
        mapping = {'Win':1, 
                   'Loss':-1, 
                   'Draw':0}
        
        score, h2h_score = assign_score(score, mapping, result)

    return score, h2h_score

def get_derby(score, derby, result):
    '''
    '''
    derby_score = None
    if derby: 
        mapping = {'Win':1, 
                   'Loss':-1, 
                   'Draw':-1}
        
        score, derby_score = assign_score(score, mapping, result)

    return score, derby_score

def get_dmm(score, dmm, result):
    '''
    '''
    dmm_score = None
    if dmm: 
        mapping = {'Win':0, 
                   'Loss':0, 
                   'Draw':2}
        
        score, dmm_score = assign_score(score, mapping, result)

    return score, dmm_score

def get_doubled(score, doubled): 
    '''
    '''
    if doubled: 
        score = score * 2

    return score

def save_score(player, round_id, score, basic_score, h2h_score, derby_score, dmm_score, subtotal):
    '''
    TODO: Test
    '''
    query = '''
            INSERT INTO SCORES
            (PLAYER_ID, ROUND, BASIC_POINTS, H2H_POINTS, 
             DERBY_POINTS, DMM_POINTS, SUBTOTAL, TOTAL)
            VALUES 
            ({}, {}, {}, {}, {}, {}, {}, {})
            '''.format(player, 
                       round_id, 
                       basic_score if basic_score else 'null', 
                       h2h_score if h2h_score else 'null', 
                       derby_score if derby_score else 'null', 
                       dmm_score if dmm_score else 'null', 
                       subtotal if subtotal else 'null', 
                       score if score else 'null')
    
    utils.run_sql_query(query, True)
    return True


def calculate_scores(round_id): 
    '''
    TODO: Test
    '''
    doubled, dmm, _ = Round.get_round_info(round_id)
    choices = Choices.get_choices(round_id)

    for player, choice in choices.items():
        fixture_id, derby, h2h = Games.get_game_info(choice, round_id)
        
        result = Results.get_result(choice, fixture_id)
        print(choice, result)
        # print('h2h: {}, derby: {}'.format(h2h, derby))
        score, basic_score, h2h_score, derby_score, dmm_score, subtotal = get_score(result, 
                                                                                    h2h, 
                                                                                    derby, 
                                                                                    dmm, 
                                                                                    doubled)
        # print('choice: {}, h2h: {}, derby: {}'.format(choice, h2h_score, derby_score))
        save_score(player, round_id, score, basic_score, 
                   h2h_score, derby_score, dmm_score, 
                   subtotal)
        
    calculated = True

    return calculated

def get_points(round_id): 
    '''
    '''
    query = '''
            SELECT  
                    SUBSTRING_INDEX(email, '@', 1) AS USER,
                    TEAM_CHOICE,
                    coalesce(basic_points, 0)   as basic_points, 
                    coalesce(h2h_points, 0)     as h2h_points,
                    coalesce(derby_points, 0)   as derby_points,
                    coalesce(dmm_points, 0)     as dmm_points,
                    coalesce(subtotal, 0)       as subtotal,
                    coalesce(total, 0)          as total

            FROM SCORES as s
            LEFT JOIN PLAYERS as p
            on s.player_id = p.player_id
            LEFT JOIN CHOICES AS C
            ON p.PLAYER_ID = C.PLAYER_ID AND s.ROUND = C.ROUND
            WHERE s.round = {}
            ORDER BY TOTAL DESC
            '''.format(round_id)
    
    points = utils.run_sql_query(query)

    return points.to_json(orient='records')