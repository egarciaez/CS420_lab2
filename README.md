# CS420_lab2

## Building and Running the Application

This application is a Dockerized command-line tool that analyzes application log files.
It is designed to run entirely inside a Docker container and requires only a single
`docker run` command to execute.

## Structure
```bash
log-analyzer/
├── app/
│ ├── init.py
│ ├── analyzer.py
│ └── cli.py
├── logs/
│ └── starterLog.log
├── Dockerfile
├── requirements.txt
README.md

- `app/` → Python package with the application code  
- `logs/` → Sample logs (replace or add your own logs here)  
- `Dockerfile` → Defines the container image  
- `requirements.txt` → Python dependencies (none external in this version)  
```

### Prerequisites
- Docker installed and running
- GitHub Codespaces or a local development environment
- A directory containing `.log` files

---
## Clone the Repository (if needed)

git clone https://github.com/<your-username>/log-analyzer.git
cd log-analyzer

## Build the Docker Image (Required)

From the root of the project 
(where the `Dockerfile` is located), build the image:

```bash
Build the Docker Image From the project root meaning where Dockerfile is located (in this case cd log-analyzer):
Run this after confirming you are in the right directory:

docker build -t log-analyzer .
```
This creates a local Docker image called log-analyzer
Copies the application code into the container
Installs any dependencies
Prepares the app to run inside the container

## Confirm the image exists
```bash
Run this next: 
docker images
```
#### You should see something like this: 
<img width="589" height="36" alt="image" src="https://github.com/user-attachments/assets/561a3aad-071b-4171-adfc-4d61ca6ff575" />



## Run the Application (Docker): 
```bash
Run this next: 
macOS / Linux (Bash / Zsh): 
docker run --rm -v $(pwd)/logs:/logs log-analyzer --log-dir /logs

Windows (PowerShell): 
docker run --rm -v ${PWD}/logs:/logs log-analyzer --log-dir /logs
```


Explanation:

--rm → removes the container after it exits

-v $(pwd)/logs:/logs → mounts the host logs/ folder into the container

--log-dir /logs → tells the app where to find .log files inside the container

### Expected Output:
<img width="395" height="177" alt="image" src="https://github.com/user-attachments/assets/fadc97f5-4656-46f7-b534-7998bc26824b" />


