import utils
import Players
import Choices
import Games
import Results
import Scores
import Round


def send_new_round_update(round_id):
    '''
    '''
    emails = Players.get_all_emails()

    for email in emails:
        try:
            body = new_round_body(round_id, email)

            subject = 'FPG Round {} Update'.format(round_id)

            utils.send_email(email, subject, body)
        except BaseException:
            pass

    return True


def new_round_body(round_id, email):
    '''
    '''
    doubled, dmm, _ = Round.get_round_info(round_id)

    player_id = Players.get_player_id(email)

    choice = Choices.get_choices(round_id)[player_id]

    fixture_id, derby, h2h = Games.get_game_info(choice, round_id)

    result = Results.get_result(choice, fixture_id)

    if result == 'Win':
        email_result = 'winning'
    elif result == 'Draw':
        email_result = 'drawing'
    else:
        email_result = 'losing'

    total_score = Scores.get_score(result, h2h, derby, dmm, doubled)[0]

    body = '''
Howdy {},

Round {} of the premier league has concluded - meaning the FPG scores are in...

You picked <b>{}</b> who ended up <b>{}</b> their game
leaving you with a total score of <b>{}</b>.

Head over to the <a href="https://fpg-pick.streamlit.app">FPG Home Page</a>
to see the details

While you are there why not submit your choice for this week

Thankyou,

FPG
'''.format(email.split('@')[0], round_id, choice, email_result, total_score)
    return body
