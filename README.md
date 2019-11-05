## Overview
This repository includes (extremely preliminary) code to detect four variants of inappropriate social media behavior including:

(1) 'Pinging' or repetitious statements <br>
(2) Solicitations for money <br>
(3) Requests for personal informatin (PI) <br>
(4) Requests to meet in person <br>

Functionality for detecting affirmative responses to inappropriate solicitations is also included.

These functions are intended to support a front-end system that detects inappropriate behaviors and provides a 'stop and think' moment to social media users before their typed responses are sent to the recipient. For example, if an online friend asked for money and the social media user typed 'Ok, how much do you need?" the envisioned front-end system would raise a dialog box cautioning the user about their response and suggesting several alternatives such as "I'm sorry you're in a tough situation right now" or "I'm sorry, but my social media coach says I'm not supposed to give money to people I meet online". The system might also provide an option to send the exchange to a human advisor with a request for guidance on how to proceed.

The vision is that ultimate control remains with the social media user, but the system offers insight into the dynamics and dangers of the online world and provides an opportunity to rethink messages that may be inadvisable.

## Setup
to run this code, you'll need to download the pre-trained GLoVE word vectors from https://nlp.stanford.edu/projects/glove/ <br>
Place them in your local directory.
```
wget http://nlp.stanford.edu/data/glove.840B.300d.zip
```

## Usage
```
import sm_coach as coach

sentence1 = "I am wondering whether this sentence is asking for money"
sentence2 = "And I am wondering whether this sentence is similar to sentence1"

money_solicitation = coach.detect_money_solicitation(sentence1)
ping = coach.detect_ping(sentence1)
repeat = coach.detect_repeat(sentence1, sentence2)
pi = coach.detect_pi_solicitation(sentence1)
meetup = coach.detect_meetup_solicitation(sentence1)
affirmative = coach.detect_affirmative(sentence1)

print(money_solicitation, ping, repeat, pi, meetup, affirmative)
```

You can also run a sequence of tests on various pre-coded sentences by executing:
```
python3 detection_tests.py
```

## Disclaimer
Right now the repo only contains quickly-hacked-together code for the purposes of exploratory testing. If initial experiments seem promising, I'll put a student on the task of improving accuracy, precision, and recall on the classification algorithms. Pretty sure we can get close to 90% in all categories.
