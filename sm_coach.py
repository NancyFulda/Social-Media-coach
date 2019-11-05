import numpy as np
import scipy.spatial as spatial
import random

#------------------------------
# GLOBALS AND HELPER FUNCTIONS
#

LIMIT = 50000

#------------------------------
# INITIALIZE MODEL
#

print('Initializing word vectors...')
glove_tokens = []
glove_vectors = []
with open('glove.840B.300d.txt','r') as f:
    data = f.read()
    lines = data.split('\n')
    print('%d lines found, using the first %d' % (len(lines), LIMIT))
    for line in lines[:LIMIT]:
        tokens = line.split(' ')
        glove_tokens.append(tokens[0])
        glove_vectors.append(np.array([float(t) for t in tokens[1:]]))
print('done\n')

#------------------------------
# HELPER FUNCTIONS
#

def tokenize(source_line):
    source_line = source_line.strip('\n').strip()
    source_line = source_line.lower()
    source_line = source_line.replace('.', ' .')\
                             .replace(',', '')\
                             .replace('?', ' ?')\
                             .replace('!', ' .')\
                             .replace('"', ' "')\
                             .replace('\'', ' \'')\
                             .replace('-', '')\
                             .replace(':', '')\
                             .replace(';', '')
    source_line = source_line.replace('  ',' ').replace('  ', ' ').replace('  ', ' ')
    return source_line.split()

def calc_distance(v1, v2, metric='cosine'):
    if metric == 'cosine':
        return spatial.distance.cosine(v1,v2)
    elif metric == 'cityblock':
        return spatial.distance.cityblock(v1,v2)
    elif metric == 'correlation':
        return spatial.distance.correlation(v1,v2)
    elif metric == 'euclidean':
        return spatial.distance.euclidean(v1,v2)
    else:
        raise ValueError('Unkown distance metric: ' + metric)

def embed(text):
    vector = np.mean(np.array([glove_vectors[glove_tokens.index(w)] for w in tokenize(text) if w in glove_tokens]), axis=0)
    return vector

#------------------------------
# KEY DETECTION FUNCTIONS
#

def detect_ping(s, metric='cosine'):
    #test_phrases = ['?','hi?','hello?','hello','are you there?','are you still there?']
    test_phrases = ['?',
                    'hi?',
                    'hello?',
                    'hello',
                    'are you there?',
                    'are you online?']
    min_dist = 1000
    for t in test_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v, metric)
        min_dist = min(dist, min_dist)
    if min_dist < 0.1:
        return True
    return False

def detect_repeat(s1, s2, threshhold = 0.05, metric='cosine'):
    dist = calc_distance(embed(s1), embed(s2))
    if dist < threshhold:
        return True
    return False

def detect_money_solicitation(s):
    sim_phrases = ['will you give me some money', 
                    'i need money', 
                    'please give me a little bit of cash', 
                    'i need to borrow some cash', 
                    'do you have a credit card?']
    ant_phrases = ['I don\'t want to give you any money',
                    'no you cannot have my bank account number',
                    'I do not loan money to strangers',
                    'I don\'t think that\'s a good idea']
    min_dist = 1000
    max_dist = 0
    for t in sim_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        min_dist = min(dist, min_dist)
    for t in ant_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        max_dist = max(dist, min_dist)
    if min_dist < 0.1 and max_dist > 0.1:
        return True
    return False

def detect_pi_solicitation(s):
    sim_phrases = ['what\'s your name?', 
                    'where do you live', 
                    'i need your social security number', 
                    'tell me what your name is', 
                    'how old are you?',
                    'what is your address?']
    ant_phrases = ['I don\'t want to tell you my name',
                    'no i will not give you my social security number',
                    'i am 17 years old',
                    'i do not share my address with people online']
    min_dist = 1000
    max_dist = 0
    for t in sim_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        min_dist = min(dist, min_dist)
    for t in ant_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        max_dist = max(dist, min_dist)
    if min_dist < 0.1 and max_dist > 0.1:
        return True
    return False

def detect_meetup_solicitation(s):
    sim_phrases = ['do you want to meet me somewhere?', 
                    'lets meet irl', 
                    'i would like to meet you', 
                    'would you like to meet?',
                    'let\'s get together this weekend.',
                    'shall we get together?',
                    'we should meet']
    ant_phrases = ['I never meet with strangers from the internet',
                  'no I don\'t want to meet together']
    min_dist = 1000
    max_dist = 0
    for t in sim_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        min_dist = min(dist, min_dist)
    for t in ant_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        max_dist = max(dist, min_dist)
    if min_dist < 0.09 and max_dist > 0.1:
        return True
    return False

def detect_money_offer(s):
    sim_phrases = ['I guess I could loan you a few dollars', 
                    'would you like some money?', 
                    'you can have some of mine',
                    'do you need some money?'] 
    ant_phrases = ['I wish I could help',
                    'i can\'t help you with that',
                    'i\m sorry, but i can\'t do that',
                    'no',
                    'sorry',
                    'not a chance',
                    'i don\'t think that\'s a good idea',
                    'i would like to, but']
    min_dist = 1000
    max_dist = 0
    for t in sim_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        min_dist = min(dist, min_dist)
    for t in ant_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        max_dist = max(dist, min_dist)
    if min_dist < 0.1 and max_dist > 0.05:
        return True
    return False

def detect_affirmative(s):
    sim_phrases = ['OK', 
                    'sure!',
                    'sure', 
                    'all right', 
                    'alright', 
                    'i can do that',
                    'yes']
    ant_phrases = ['I wish I could help',
                    'i can\'t help you with that',
                    'i\m sorry, but i can\'t do that',
                    'sorry',
                    'not a chance',
                    'i don\'t think that\'s a good idea',
                    'i would like to, but',
                    'no',
                    'no i don\'t']
    min_dist = 1000
    max_dist = 0
    for t in sim_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        min_dist = min(dist, min_dist)
    for t in ant_phrases:
        s_v = embed(s)
        t_v = embed(t)
        dist = calc_distance(s_v, t_v)
        max_dist = max(dist, min_dist)
    if min_dist < 0.1 and max_dist > 0.1:
        return True
    return False

