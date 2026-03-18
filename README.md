# studybuddy
A program created to help students study efficiently. Track study sessions with the timer feature, and summarize total time spent in study sessions. Generate motivational quotes and enjoy ascii art along with it! Keep track of items on your task list with the built in task manager. 

- uv for dependency management
- Pytest for tests
- ruff for formatting and linting
- ty for type checking


## Building

- Install uv https://docs.astral.sh/uv/getting-started/installation/
- Clone from GitHub
- Build - Install, test, lint `make build`. This step pulls the python version defined in pyproject.toml
- Tests can be run with `make test`

## Dependencies
- relies on microservices built on REST APIs
    - timer microservice
    - motivational quotes microservice
    - ascii art microservice
    - unit conversion microservice
    - reports microservice
    - music fetcher microservice
- uses Rich for text formatting


- 


