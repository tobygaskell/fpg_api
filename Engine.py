import utils 
import Round
import Scores
import Results


def main():
    '''
    TODO: Test
    '''
    round_id = Round.get_current_round()

    changed, last_round_id = Round.round_changed(round_id) 

    collected = False
    calculated = False
    configured = False

    if changed: 
        collected = Results.init_results(last_round_id)
        calculated = Scores.calculate_scores(last_round_id)
        configured = Round.init_round(round_id)

    save_log(round_id, collected, calculated, configured) 

def save_log(round_id, collected, calculated, configured): 
    '''
    '''
    query = '''
            INSERT INTO LOGS
            VALUES
            (CURRENT_TIMESTAMP(2), {}, {}, {}, {})
            '''.format(round_id, collected, calculated, configured)
    
    utils.run_sql_query(query, True)