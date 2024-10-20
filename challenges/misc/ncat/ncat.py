import sys
import random


flag = 'MINUTEMAN{3T_h@s_ph0n3d_h0m3}'

questions = [
    (
        'On what floor of the Du Bois library are the Teenage Mutant Ninja Turtle Statues? [1-30]',
        '21'
    ),
    (
        'Before the creation of the 110-160-210 intro sequence, what was the name of the first required course in the CS curriculum? [A/B/C/D]\n\nA. CS 101\nB. CS 110\nC. CS 121\nD. CS 131',
        'C'
    ),
    (
        'Which of the following colleges is *not* in the 5 College Consortium? [A/B/C/D]\n\nA. Hampshire College\nB. Smith College\nC. Springfield College\nD. Mount Holyoke College',
        'C'
    ),
    (
        'UMass has an infamous college football rivalry with which other New England university? [A/B/C/D]\n\nA. UMass Cambridge\nB. Boston College\nC. Amherst College\nD. University of Connecticut',
        'D'
    ),
    (
        "You may have noticed that certain areas on campus have themed names: Southwest dorms are named after US Presidents and authors, dining halls are named after Massachusetts counties, and so on. Which of the following trees is not represented by a Honors College residence hall? [A/B/C/D]\n\nA. Willow\nB. Maple\nC. Linden\nD. Oak",
        'A'
    )
]

description = '''
Welcome to nc! nc, or Netcat, is a terminal utility for connecting to and listening to ports on the internet. 

You're probably used to a web browser, where you type a link in the address bar, your browser connects to that web page, listens for content (html, css, etc.), displays it on your screen. nc is similar, but instead of taking a website link or domain name as its address, nc takes in the ip address and port, connects to that address, and listens for traffic. 

nc is a networking swiss army knife. Through nc, you can send and receive files, chat back and forth with another user, or scan a server for open ports on a server (don't do this to someone else's server without their permission!). nc is also the standard method for connecting to servers for CTF challenges.

In a typical nc challenge, the organizers (us) run a program on their server and expose it to the internet via a port. Then, the organizers provide competitors with the ip address + port of the challenge (for competitors to connect to and test their exploits). nc challenges are most common in the crypto, web, and misc. categories.

In this three part challenge series, you will learn how to 
1. Connect to nc via your terminal
2. Receive and send content to and from nc manually via your terminal
3. Receive and send content to and from nc automatically via a script, such as a python program

In this challenge, we're going to play some UMass trivia. I'm going to ask you a series of multiple-choice questions. The answer options will be provided in square brackets, for example [Yes/No] or [True/False] for a binary answer, [A/B/C/D] for multiple choice, or [1-10] for numerical answers 1, 2, ..., 10.

When you send back your answer, make sure there is no leading or trailing whitespace, and that your answer is the correct case (for example, Yes is a valid response, but yes is not). While we *could* format your answers for you, some challenge authors elect not to do this, and the format (more specifically the encoding) of your answers will be important once we start to script our responses.

Are you ready to start? [Yes/No]
'''

print(description)

if input() != 'Yes':
    print('Exiting challenge, user was not ready. Once you are ready, reconnect to us via nc.')
    sys.exit(0)

random.shuffle(questions)

for i, (question, answer) in enumerate(questions):
    print(f'Question {i+1}:')
    print(question)
    print()

    if input() != answer:
        print('That answer is incorrect. To play again, reconnect via nc.')

    print('Correct!\n')

print("Congrats, here's your flag.")
print(flag)