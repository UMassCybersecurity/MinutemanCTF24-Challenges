# Yell at me to write a solve script once the remote is up

num_rounds = 10

def read_in_starting_value():
    # read until starting
    # split on colon
    # cast content after colon to int and return
    pass

def read_turn():
    read_in_starting_value()
    # read everything into string
    # Separate string based on empty line \n\n
    # List comprehend result, splitting based on \n into operation and value
    operation_dict = {
        'ADD'     : lambda x,y: x + y,
        'SUBTRACT': lambda x,y: x - y,
        'MULTIPLY': lambda x,y: x * y,
        'MODULO'  : lambda x,y: x % y,
    }
    # Reduce over result, passing operation to dict, accumulator as first arg, value as second arg
    # return reduced result

for _ in range(num_rounds):
    read_turn()
    # send value

# recv remaining text (congrats and flag)
