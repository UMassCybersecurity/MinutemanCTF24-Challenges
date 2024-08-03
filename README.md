## Tentative CTF date: October 12-14, 2024

## For Challenge Authors 

### Our Environment Setup 
We follow best GitOps practices. This repository is the single source of truth. 
We have a dev and production enviornment (two ctfd environments). You will **NOT** be able to promote a challenge to production until it has passed E2E testing and been tested in the dev enviornment. 🤓

### PR Process
Please create a branch for each challenge named: *category*/*challenge-name*.
This branch will be merged into the dev branch once your PR is approved. 
See the example challenges in the `/challenges/examples`

There are two types of challenges: static vs. dynamic. 
Static challenges simply contain downloadable assets. 
Dynamic challenges need a running container for the player to interact with. 
You can specify the type of challenge in the info.yaml. 

1) Create a new directory in the appropriate category for your challenge. 
    - Use the following format (challenges/[category]/[challenge name])
    - Each challenge should contain the following:
        - a static folder with downloadable assets
        - Dockerfile/docker-compose.yml (if dynamic)
        - info.yaml (*see example challenges for required fields*)
        - README.md
        - solve script (if dynamic) (*see example challenges for format*)
2) Create a PR to merge into the dev branch. 
3) Contact DevOps club (ogpatel@umass.edu or abodepudi@umass.edu) for a PR review. **Only PRs that pass the E2E tests will be approved.** 
4) Test your challenges in the ctfd dev environment. Create any follow up PRs as necessary to make edits to your challenge. 
5) Create a PR to promote your challenge to the prod branch. 
6) Contact ogpatel@umass.edu or abodepudi@umass.edu for a PR review.


### End to End Testing (E2E)
Our E2E tests will validate the following:
- The Docker container builds 
- Successfully deploys to a testing GCP Cloud Run container
- info.yaml contains all required fields 
- Solve script returns proper flag

### Other 
If you anticipate your challenge needing special resources, please let us know well ahead of time. 


## Additional References
Docker File
- https://docs.docker.com/reference/dockerfile/
- https://medium.com/@anshita.bhasin/a-step-by-step-guide-to-create-dockerfile-9e3744d38d11

CTFd info.yaml
- https://github.com/CTFd/ctfcli/tree/master
