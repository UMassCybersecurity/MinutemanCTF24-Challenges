# SHUNT-53
Author: RS311
Description: My buddy Jaquiese started making phones, but forgot the password to his prototype. Guess it's up to you.

## Intended Solution(s)
Note: it is possible to programmatically implement both solutions, but it may be easier to solve visually.

### Option 1: Smart Bruteforce
The password is guaranteed to be 5 characters long, and only contain uppercase alphabetical characters. 
- If one was to bruteforce the password, the total number of guesses before you are guaranteed a solution is $$26 * 26 * 26 * 26 * 26 = 26^5 = 11881376$$.
- The number of guesses we allow is 26 * 5 = 130, so bruteforcing is impossible.

Using the power traces given to us when entering a password, we can monitor the current when entering passwords. The key is to look at the trace character by character.
- At t = 10 + 5*x + 2.5 (where x is the index of the character in the string), the current draw is in three possible states: 
  - One that represents that the character we guessed is alphanumerically **before** the correct character (hovering at around 5 mA).
  - One that represents that the character we guessed is alphanumerically **after** the correct character (hovering at around 15 mA).
  - One that represents that the character we guessed is alphanumerically **equal** to the correct character (hovering at around 10 mA).
- If any of the characters are incorrect, then the current draw approaches 0 mA (signaling that the password was wrong).

Knowing that, we can bruteforce from `A` -> `Z` on each character, until we meet the condition for it being equal (that is, the current is around 10 mA). With this approach, it reduces our search space to 26 * 5 = 130 guesses to guarantee that we are correct.

### Option 2: Binary Search
As stated previously:
- At t = 10 + 5*x + 2.5 (where x is the index of the character in the string), the current draw is in three possible states: 
  - One that represents that the character we guessed is alphanumerically **before** the correct character (hovering at around 5 mA).
  - One that represents that the character we guessed is alphanumerically **after** the correct character (hovering at around 15 mA).
  - One that represents that the character we guessed is alphanumerically **equal** to the correct character (hovering at around 10 mA).
  
This logic can be used to perform a binary search on the trace data, which will reliably get you under 130 guesses. 

For each character, the total number of guesses to guarantee a match is log_2(n), where n = 26. 5 * log_2(26) = 5 * 4.70043971814 ~= 23.5021985907 = 24 guesses to guarantee the correct password.