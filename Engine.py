import utils
import Round
import Scores
import Results
import Updates


def main():
    '''
    TODO: Test
    '''
    round_id = Round.get_current_round('api')

    changed, last_round_id = Round.round_changed(round_id)

    collected = False
    calculated = False
    configured = False
    emailed = False

    if changed:
        collected = Results.init_results(last_round_id)
        calculated = Scores.calculate_scores(last_round_id)
        configured = Round.init_round(round_id)
        emailed = Updates.send_new_round_update(last_round_id)

    save_log(round_id, collected, calculated, configured, emailed)


def save_log(round_id, collected, calculated, configured, emailed):
    '''
    '''
    query = '''
            INSERT INTO LOGS
            (time_added, round, results_pulled, scores_updated,
             next_round_init, update_sent)
            VALUES
            (CURRENT_TIMESTAMP(2), {}, {}, {}, {}, {})
            '''.format(round_id, collected, calculated, configured, emailed)

    utils.run_sql_query(query, True)
