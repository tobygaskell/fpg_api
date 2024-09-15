

def main(result, h2h, derby, dmm, doubled): 
    '''
    '''
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
               'Lose':-1, 
               'Draw':0}

    score, basic_score = assign_score(0, mapping, result)

    return score, basic_score

def get_h2h(score, h2h, result): 
    '''
    '''
    h2h_score = None

    if h2h: 
        mapping = {'Win':1, 
                   'Lose':-1, 
                   'Draw':0}
        
        score, h2h_score = assign_score(score, mapping, result)

    return score, h2h_score

def get_derby(score, derby, result):
    '''
    '''
    derby_score = None
    if derby: 
        mapping = {'Win':1, 
                   'Lose':-1, 
                   'Draw':-1}
        
        score, derby_score = assign_score(score, mapping, result)

    return score, derby_score

def get_dmm(score, dmm, result):
    '''
    '''
    dmm_score = None
    if dmm: 
        mapping = {'Win':0, 
                   'Lose':0, 
                   'Draw':2}
        
        score, dmm_score = assign_score(score, mapping, result)

    return score, dmm_score

def get_doubled(score, doubled): 
    '''
    '''
    if doubled: 
        score = score * 2

    return score