# CS420_lab2

## Building and Running the Application

This application is a Dockerized command-line tool that analyzes application log files.
It is designed to run entirely inside a Docker container and requires only a single
`docker run` command to execute.

### Prerequisites
- Docker installed and running
- GitHub Codespaces or a local development environment
- A directory containing `.log` files

---

### Build the Docker Image

From the root of the project (where the `Dockerfile` is located), build the image:

```bash
docker build -t log-analyzer .

### Run the Application

Run the application using one Docker command, providing the log directory as an argument:
docker run --rm \
  -v $(pwd)/logs:/logs \
  log-analyzer \
  --log-dir /logs
