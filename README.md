#TODO: clean up branches, delete branch upon merging PR
## For Challenge Authors 

### Our Environment Setup 
We follow best GitOps practices. This repository is the single source of truth. 
We have a dev and production environment (two CTF environments). You will **NOT** be able to promote a challenge to production until it has passed E2E testing and been tested in the dev environment. 🤓

### PR Process
Please create a branch for each challenge named: *category*/*challenge-name*. This should correspond to the path to the challenge from the `challenges` folder
This branch will be merged into the dev branch once your PR is approved. You can then make a PR into prod. 

Flag Format: `UMASS{<FLAG>}`

There are two types of challenges: static vs. dynamic. 
Static challenges simply contain downloadable assets. 
Dynamic challenges need a running container for the player to interact with. 

1) Create a new directory in the appropriate category for your challenge. 
    - Use the following format (challenges/[category]/[challenge name])
        - Please make sure the challenge name does not contain any underscores, capital letters, or special characters. 
    - Each challenge should have the following things at the top level:
        - an optional static folder with downloadable assets
        - a Dockerfile/docker-compose.yaml and a config.env if dynamic (see this [config.env](./refs/config.env) for reference)
        - info.yaml (see this [info.yaml](./refs/info.yaml) for reference)
1) Create a PR to merge into the dev branch.
2) Test your challenges in the CTFd dev environment. Create any follow up PRs as necessary to make edits to your challenge. 
3) Create a PR to promote your challenge to the prod branch.


### End to End Testing (E2E)
Our E2E tests will validate the following:
- The Docker container builds 
- info.yaml contains all required fields

## Additional References
Docker File
- https://docs.docker.com/reference/dockerfile/
- https://medium.com/@anshita.bhasin/a-step-by-step-guide-to-create-dockerfile-9e3744d38d11
