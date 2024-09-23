from numpy.random import randint
import sys

flag = 'UMassCTF{y0u_c@n_c0unt_0n_m3_l1ke_123}'

num_rounds = 10
operations_per_round = 100

# Tuples are (displayed string, internal operator, min value, max value)
operators = [
    ('ADD',      lambda x,y: x + y, 0,  100),
    ('SUBTRACT', lambda x,y: x - y, 0,  100),
    ('MULTIPLY', lambda x,y: x * y, 1,  10 ),
    ('MODULO',   lambda x,y: x % y, 10, 1000),
]

description = '''In this challenge, we are going to practice our arithmetic skills.

We are going to play a 10 round game. At the beginning of each round, I pick a random number to start with and announce it. Then, I randomly pick one of four operations: +, -, *, and %, and a random number to apply the operation with. I randomly sample 100 operations and numbers in this manner, cumulatively updating the total as I go.

For an example game, let's say I start by picking the number 8. Then, on turn 1, I pick the addition operation + and number 90, so the total after turn 1 is 96. On turn 2, I pick the multiplication operation * and number 7, so the total after turn 2 is 672. This series of events would be displayed through nc as follows:
---
Starting value is 6
Operation 1
ADD
90

Operation 2 
MULTIPLY
7

...
---
After turn 100, nc will ask you what the current value is. You should respond with the current total, written as an integer (there are no floats or division in this challenge), and no other characters or whitespace. If your answer is correct, you will continue to the second round, where I pick a new starting value and we play again. If your answer is incorrect, nc will close the connection, and you can reconnect to try again.

After you make it through the tenth round, nc will print out a congratulations message and the flag.

Remark: note that % is the modulo operation (like in python), where 0 ≤ (x % n) < n for all x (that is, the output of the modulo operation is never negative), not the remainder operation (like in C), where (x % n) is negative if x is negative.

Are you ready to start? [Yes/No]
'''

print(description)

if input() != 'Yes':
    print('User is not ready. Reconnect to nc to when you are ready.')
    sys.exit(0)

for n in range(num_rounds):
    total = randint(0, 11)
    print(f'Starting value is {total}')
    for i in range(operations_per_round - 1):
        # Randomly sample an operation
        op_string, operator, min_value, max_value = operators[randint(0, 4)]
        # Sample the number to use with that operation
        number = randint(min_value, max_value)
        # Print operation and number to user
        print(f'Operation {i + 1}\n{op_string}\n{number}\n')

        # Compute new total
        new_total = operator(total, number)
        # print(total, number, new_total) # Comment this line out to see the internal state
        total = new_total

    user_value = int(input('What is the current value?\n'))
    if total != user_value:
        print('Your guess is not correct. Please reconnect to nc to try again')
        sys.exit(0)

    print('Correct.')

print('Congrats, here is your flag.')
print(flag)