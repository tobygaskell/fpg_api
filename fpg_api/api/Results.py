import utils


def get_standings(season):
    '''
    '''
    query = '''
            WITH base as (
                SELECT distinct c.player_id, r.round, r.fixture_id,
                    team_choice, home_team, away_team, home_goals,
                    away_goals,  home_goals - away_goals as GD
                from (SELECT DISTINCT *
                    FROM RESULTS
                    WHERE game_status = 'Match Finished'
                    AND season = {}) r
                left join (SELECT * FROM FIXTURES WHERE SEASON = {}) f
                on r.FIXTURE_ID  = f.FIXTURE_ID
                left join (SELECT * FROM CHOICES WHERE SEASON = {}) c
                on TEAM_CHOICE = home_team
                and r.round = c.round
                left join PLAYERS p
                on c.PLAYER_ID  = p.PLAYER_ID

                union

                select distinct c.player_id, r.round, r.fixture_id,
                    team_choice, home_team, away_team, home_goals,
                    away_goals, away_goals - home_goals as GD
                from (SELECT DISTINCT *
                    FROM RESULTS
                    WHERE game_status = 'Match Finished'
                    AND season = {}) r
                left join (SELECT * FROM FIXTURES WHERE SEASON = {}) f
                on r.FIXTURE_ID  = f.FIXTURE_ID
                left join (SELECT * FROM CHOICES WHERE SEASON = {}) c
                on TEAM_CHOICE = away_team
                and r.round = c.round
                left join PLAYERS p
                on c.PLAYER_ID  = p.PLAYER_ID
            )

            , subtotal as (
                select *, sum(GD) over (partition by player_id
                                        order by round asc) as rolling_gd
                from base
                where player_id is not null
                order by player_id, round desc
            )

            , standings as (
                SELECT  P.PLAYER_ID,
                        coalesce(nullif(username, ''),
                                SUBSTRING_INDEX(email, '@', 1)) AS USER,
                        CAST(COALESCE(SUM(total), 0) as int) AS SCORE
                FROM (SELECT * FROM SCORES WHERE season = {}) AS F
                RIGHT JOIN PLAYERS AS P
                ON F.PLAYER_ID = P.PLAYER_ID
                GROUP BY P.player_id
                ORDER BY sum(total) desc
            )

            , max_round as (
                SELECT MAX(ROUND) AS max_round
                FROM SCORES
                WHERE season = {}
            )

            , last_weeks_standings as (
                SELECT
                    P.PLAYER_ID,
                    SUBSTRING_INDEX(email, '@', 1) AS USER,
                    CAST(COALESCE(SUM(TOTAL), 0) AS int) AS SCORE
                FROM (SELECT * FROM SCORES WHERE season = {}) AS F
                RIGHT JOIN PLAYERS AS P
                ON F.PLAYER_ID = P.PLAYER_ID
                WHERE round NOT IN (SELECT * FROM max_round)
                GROUP BY P.player_id
                ORDER BY sum(total) desc
            )

            , last_weeks_subtotal as (
                select *, sum(GD) over (partition by player_id
                                        order by round asc) as rolling_gd
                from base
                where player_id is not null
                and round NOT IN (SELECT * FROM max_round)
                order by player_id, round desc
            )

            , totals as (
                select a.player_id, rolling_gd
                from ((
                select player_id,
                    round,
                    cast(rolling_gd as int) as rolling_gd
                from subtotal ) a
                inner join
                (select player_id, max(round) as round
                from subtotal
                group by player_id) b
                on a.player_id = b.player_id
                and a.round = b.round
            ) )

            , last_weeks_totals as (
                select a.player_id, rolling_gd
                from ((
                select player_id,
                    round,
                    cast(rolling_gd as int) as rolling_gd
                from last_weeks_subtotal ) a
                inner join
                (select player_id, max(round) as round
                from last_weeks_subtotal
                group by player_id) b
                on a.player_id = b.player_id
                and a.round = b.round
            ) )

            , final as (
                select RANK() over (ORDER BY score DESC,
                                            rolling_gd desc) as Position,
                    stand.player_id,
                    user as User,
                    COALESCE(rolling_gd, 0) as 'Goal Diff',
                    score as Score
                from standings as stand
                left join totals as t
                on stand.player_id = t.player_id
                )

            , last_week_final as (
                select RANK() over (ORDER BY score DESC,
                                            rolling_gd desc) as Position,
                    stand.player_id,
                    user as User,
                    rolling_gd as 'Goal Diff',
                    score as Score
                from last_weeks_standings as stand
                left join last_weeks_totals as t
                on stand.player_id = t.player_id
            )

            select f.*, case when f.position < lwf.position then 'Up'
                            when f.position = lwf.position then 'Same'
                            when f.position > lwf.position then 'Down'
                            else 'Same'
                            end as movement_indicator
            from final as f
            left join last_week_final as lwf
            on f.player_id = lwf.player_id
            ORDER BY  f.position, f.player_id;
            '''.format(season, season, season,
                       season, season, season,
                       season, season, season)
    data = utils.run_sql_query(query)

    return data.to_json(orient='records')


def get_rolling_standings(season=2024):
    '''
    '''
    query = '''
            WITH base AS (
                SELECT distinct c.player_id, r.round, r.fixture_id,
                    team_choice, home_team, away_team, home_goals,
                    away_goals,  home_goals - away_goals as GD
                from (SELECT * FROM RESULTS WHERE SEASON = {}) r
                left join (SELECT * FROM FIXTURES WHERE SEASON = {}) f
                on r.FIXTURE_ID  = f.FIXTURE_ID
                left join (SELECT * FROM CHOICES WHERE SEASON = {}) c
                on TEAM_CHOICE = home_team
                and r.round = c.round
                left join PLAYERS p
                on c.PLAYER_ID  = p.PLAYER_ID

                union

                select distinct c.player_id, r.round, r.fixture_id,
                    team_choice, home_team, away_team, home_goals,
                    away_goals, away_goals - home_goals as GD
                from (SELECT * FROM RESULTS WHERE SEASON = {}) r
                left join (SELECT * FROM FIXTURES WHERE SEASON = {}) f
                on r.FIXTURE_ID  = f.FIXTURE_ID
                left join (SELECT * FROM CHOICES WHERE SEASON = {}) c
                on TEAM_CHOICE = away_team
                and r.round = c.round
                left join PLAYERS p
                on c.PLAYER_ID  = p.PLAYER_ID
            )

            , subtotal as (
                select *, sum(GD) over (partition by player_id
                                        order by round asc) as rolling_gd
                from base
                where player_id is not null
                order by player_id, round desc
            )

            , standings as (
                SELECT *, rank() over (partition by round
                                    order by rolling_total desc ) as position
                FROM (SELECT distinct s.round,
                            p.player_id,
                            SUBSTRING_INDEX(email, '@', 1) AS USER,
                            COALESCE(SUM(TOTAL) OVER (PARTITION by player_id
                                                    order by s.round asc), 0)
                                                    as rolling_total
                FROM (SELECT * FROM SCORES WHERE SEASON = {}) AS s
                INNER JOIN PLAYERS AS p
                ON s.PLAYER_ID = p.PLAYER_ID
                INNER JOIN ROUNDS AS r
                on s.ROUND = r.ROUND) as a
            )

            SELECT RANK() OVER (partition by t.round
                                ORDER BY rolling_total DESC,
                                         rolling_gd DESC) AS Position,
                stand.player_id,
                user AS User,
                rolling_gd AS 'Goal Diff',
                rolling_total AS Score,
                t.round
            FROM standings AS stand
            INNER JOIN subtotal AS t
            ON stand.player_id = t.player_id
            AND stand.round = t.round;
            '''.format(season, season, season,
                       season, season, season,
                       season)

    data = utils.run_sql_query(query)

    return data.to_json(orient='records')


def get_round_results(round_id, season=2024):
    '''
    '''
    query = '''
            SELECT DISTINCT *
            FROM RESULTS
            WHERE ROUND = {}
            AND SEASON = {}
            AND GAME_STATUS = 'Match Finished'
            '''.format(round_id, season)

    return utils.run_sql_query(query).to_json(orient='records')
