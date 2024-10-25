#!/bin/bash
# solve the challenge data

INF="challenge_data.txt"

for line in $(cat "$INF" | tail -n +6); do
    printf "%s" "$line" | fold -w1 | sort | uniq -u | tr -d '\n'
    printf "\n"
done
