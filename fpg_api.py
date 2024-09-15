from flask import Flask, request
import get_score as gs


app = Flask(__name__)

@app.route('/get_score', methods=['POST'])
def get_score():
    '''
    '''
    request_data = request.get_json()

    player = request_data['Player']
    result = request_data['Result']
    h2h = request_data['H2H']
    derby = request_data['Derby']
    dmm = request_data['DMM']
    doubled = request_data['Doubled']

    score, basic_score, h2h_score, derby_score, dmm_score, subtotal = gs.main(result, 
                                                                              h2h, 
                                                                              derby, 
                                                                              dmm, 
                                                                              doubled)

    return {'Result' : score, 
            'Basic': basic_score, 
            'H2H': h2h_score, 
            'Derby': derby_score, 
            'DMM':dmm_score, 
            'Sub Total': subtotal}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
