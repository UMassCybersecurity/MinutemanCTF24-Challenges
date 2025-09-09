#!/bin/bash
# create the challenge data for a given flag
# yes, this is hella slow. no, i do not care.

OUTF="challenge_data.txt"
CHARS_PER_LINE=10000
FLAG="filler_padding_cushioning_lining_umass{coreutils_more_like_coolutils}_wadding_stuffing"
FLAG_LENGTH=$(printf "$FLAG" | wc -c)

# translation of hint:
# on every line, there are many dupicate chars
# but there is one unduplicated char on every line
# solve this in a one-liner
HINT="----
Per line of like chars
Sits a lonesome, single byte
Can you find Waldo?
----

"
printf "%s" "$HINT" > "$OUTF"

allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[{]}\|:;,<.>/?'

# add flag to the generated data
for i in $(seq $FLAG_LENGTH); do
    char=$(printf "%s" "$FLAG" | cut -c $i) # target char

    new_allowed_chars=$(printf "%s" "$allowed_chars" | sed "s/$char//") # allowed chars with target removed

    # generate strings
    data="$(cat /dev/urandom |        # random data
        tr -dc $new_allowed_chars |   # of allowed chars
        fold -w $CHARS_PER_LINE |     # with this many chars
        head -n 1                     # for one line
    )"
    printf "%s" "$char$data$data" | fold -w1 | shuf | tr -d '\n' >> "$OUTF" # randomise order of chars
    printf "\n" >> "$OUTF"
done
