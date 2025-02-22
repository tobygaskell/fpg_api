import random
import utils


def init_round(round_id):
    '''
    '''
    if round_id > 0 and round_id <= 38:

        dmm = random.randrange(100) < 10

        doubled = random.randrange(100) < 10

        query = '''
                SELECT MIN(kickoff) AS CUTOFF,
                       DATE(MAX(kickoff)) AS END_DATE
                FROM FIXTURES
                WHERE round = {}
                AND season = 2024
                '''.format(round_id)

        df = utils.run_sql_query(query)

        cutoff = df['CUTOFF'][0]
        end_date = df['END_DATE'][0]

        query = '''
                INSERT INTO ROUNDS
                (ROUND, DP_ROUND, DMM_ROUND, CUT_OFF, END_DATE)
                VALUES
                ({}, {}, {}, '{}', '{}')
                '''.format(round_id, dmm, doubled, cutoff, end_date)

        utils.run_sql_query(query, True)

        query = '''
                UPDATE CURRENT_ROUND
                SET ROUND_ID = ROUND_ID + 1
                '''

        utils.run_sql_query(query, True)

        init = True

    else:
        init = False

    return init


def get_round_info(round_id):
    '''
    '''
    query = '''
            SELECT DP_ROUND, DMM_ROUND, CUT_OFF
            FROM ROUNDS
            WHERE ROUND = {}
            LIMIT 1
            '''.format(round_id)
    data = utils.run_sql_query(query)
    doubled = bool(data['DP_ROUND'][0])
    dmm = bool(data['DMM_ROUND'][0])
    cut_off = data['CUT_OFF'][0]

    return doubled, dmm, cut_off


def get_current_round(method='sql'):
    '''
    '''
    if method == 'api':
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/rounds"

        response = utils.get_api(url,
                                 {"league": "39",
                                  "season": "2024",
                                  "current": "true"})

        round_id = response['response'][0][-2:].strip()

    elif method == 'sql':
        query = '''
                SELECT MAX(ROUND_ID) as current_round
                FROM CURRENT_ROUND
                '''

        round_id = utils.run_sql_query(query)['current_round'][0]

    return int(round_id)


def round_changed(round_id):
    '''
    '''
    changed = False

    query = '''
            SELECT MAX(ROUND_ID) as ROUND
            FROM CURRENT_ROUND
            '''
    last_round_id = int(utils.run_sql_query(query)['ROUND'][0])

    if last_round_id == int(round_id) - 1:
        changed = True

    return changed, last_round_id
