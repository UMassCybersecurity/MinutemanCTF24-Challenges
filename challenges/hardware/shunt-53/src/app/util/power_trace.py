import math
import random

def f(x):
    return math.e**x

def g(x):
    return math.e**(-x+7)

def h(x):
    return 1

def j(x):
    return 48 * (x - 9.5) + 1

def k(x):
    return 25

# Introduce some noise so the traces are more realistic.
def noise(val, k):
    return val + random.uniform(-k, k)

def generate(x, guess = None, correct = None):
    val = 0
    if x < 3.5:
        val = f(x)
    elif 3.5 <= x < 7:
        val = g(x)
    elif 7 <= x < 9.5:
        val = h(x)
    elif 9.5 <= x < 10:
        val = j(x)
    else:
        base_val = k(x)

        slice_index = int((x - 10) // 5)
        if slice_index >= len(correct):
            return 0
        
        guess_c = ord(guess[slice_index])
        correct_c = ord(correct[slice_index])
        delta = guess_c - correct_c
        # Wrong - LT
        if delta < 0:
            val = base_val - 20
        # Wrong - GT
        elif delta > 0:
            val = base_val - 10
        else:
            val = base_val - 15
    
    return noise(val, 0.5)
    