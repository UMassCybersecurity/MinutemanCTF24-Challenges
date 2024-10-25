#!/bin/bash
# n runs of generate and validate to ensure it worky

./generate_challenge_data.sh
SOLUTION="$(./solution.sh)"

for i in {0..100}; do
     printf "test $i\n"
    ./generate_challenge_data.sh
    answer=$(./solution.sh)
    if [[ "$answer" != "$SOLUTION" ]]; then
        printf "failure :(\n"
        exit
    fi
done
