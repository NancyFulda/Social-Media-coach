from sm_coach import *

#------------------------------
# TEST SEQUENCES
#
def test_pings():
    sentences = open('frequent_message.txt', 'r').readlines()
    sentences = [s.strip('\n') for s in sentences]

    print('\nTesting pings...')
    for s in sentences:
        classification = 7*' '
        if detect_ping(s):
            classification = 'PING   '
        print(classification + s)

def test_repeated_inquiries():
    sentences = open('frequent_message.txt', 'r').readlines()
    sentences = [s.strip('\n') for s in sentences]

    print('\nTesting repetitions...')
    for i,s in enumerate(sentences):
        #print(i, s)

        classification = 15*' '
        if i >0:
            if detect_repeat(s,sentences[i-1], threshhold = 0.05):
                classification = 'REPEAT         '
            elif detect_repeat(s,sentences[i-1], threshhold = 0.1):
                classification = 'soft_repeat    '

            print(15*' ' + sentences[i-1])
        print(classification + s + '\n')

def test_money_solicitations():
    sentences = open('random_sentences.txt', 'r').readlines()
    sentences += open('asking_for_money.txt', 'r').readlines()
    sentences = [s.strip('\n') for s in sentences]
    
    print('\nTesting money solicitations...')
    for i,s in enumerate(sentences):

        classification = 9*' '
        request_flag = False
        if detect_money_solicitation(s):
            request_flag = True
        if request_flag:
            print('request  ' + s)
        else:
            print(9*' ' + s)
        print()

def test_pi_solicitations():
    sentences = open('random_sentences.txt', 'r').readlines()
    sentences = [s.strip('\n') for s in sentences]
    
    print('\nTesting PI solicitations...')
    for i,s in enumerate(sentences):
        classification = 13*' '
        if detect_pi_solicitation(s):
            classification = 'PI REQUEST   '
        print(classification + s)
        print()

def test_meetup_solicitations():
    sentences = open('random_sentences.txt', 'r').readlines()
    sentences = [s.strip('\n') for s in sentences]
    
    print('\nTesting Meet-Up solicitations...')
    for i,s in enumerate(sentences):
        classification = 9*' '
        if detect_meetup_solicitation(s):
            classification = 'MEETUP   '
        print(classification + s)
        print()

def test_affirmatives():
    sentences = open('random_sentences.txt', 'r').readlines()
    sentences += open('offering_money.txt', 'r').readlines()
    sentences = [s.strip('\n') for s in sentences]
    
    print('\nTesting affirmatives...')
    for i,s in enumerate(sentences):
        classification = 14*' '
        if detect_affirmative(s):
            classification = 'AFFIRMATIVE   '
        print(classification + s)
        print()

#------------------------------
# TEST SOLICITATIONS FOR MONEY
#
# detects (a) statements that appear to be soliciting money and
# (b) affirmative responses to such statements

if __name__ == '__main__':
    
    test_pings()
    input("PING test completed. Hit enter to continue")

    test_repeated_inquiries()
    input("REPETITION test completed. Hit enter to continue")

    test_money_solicitations()
    input("MONEY SOLICITATION test completed Hit enter to continue")

    test_pi_solicitations()
    input("PERSONAL INFO test completed. Hit enter to continue")

    test_meetup_solicitations()
    input("MEETUP test completed. Hit enter to continue")

    test_affirmatives()
    print("AFFIRMATIVE test completed")
