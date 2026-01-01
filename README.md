# School Management

A Dockerized school management system with FastAPI, PostgreSQL, Redis, Grafana, Loki, Promtail, and SonarQube.

## Prerequisites

* Ubuntu 20.04+
* Git
* Docker & Docker Compose

## 1️⃣. Clone the Repository

git clone https://github.com/DineshKumar9412/school_management.git

### Change Dirctory
cd school_management

## 2️⃣. Install Docker and Docker Compose
sudo apt update

sudo apt upgrade -y

sudo apt install -y apt-transport-https ca-certificates curl software-properties-common lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io

sudo apt update

sudo apt install -y docker-compose-plugin

### Check installation:
docker --version

docker compose version


## 3️⃣. Create `.env` File

### Create a `.env` file in the project root:

DB_USER="root"

DB_PASSWORD="root@123"

DB_HOST="3.110.91.230"

DB_NAME="sampledb"

REDIS_HOST="3.110.91.230"

REDIS_PORT="6379"

REDIS_PASSWORD="Redis@123"

KEY="MDEyMzQ1Njc4OWFiY2RlZjAxMjM0NTY3ODlhYmNkZWY="

IV="YWJjZGVmOTg3NjU0MzIxMA=="


## 4️⃣. Configure SonarQube

### Set the `vm.max_map_count` for SonarQube:

### Temporary
sudo sysctl -w vm.max_map_count=524288

### Permanent
echo "vm.max_map_count=524288" | sudo tee -a /etc/sysctl.conf

sudo sysctl -p

## 5️⃣. Run Docker Compose

### Start all services:
sudo docker compose up -d

### Build the app container if needed:
sudo docker compose build

### Check logs for troubleshooting:
sudo docker compose logs -f

### Check running containers:
sudo docker ps

### Stop all services:
sudo docker compose down

## single app test
### Rebuild the Docker image:

sudo docker compose build app

### Restart the containers:

sudo docker compose up -d

### Check the container logs to make sure there are no import errors:

sudo docker logs school_app_container

sudo docker logs -f --tail 100 school_app_container

## Important: If you add or update any requirements.txt file, you should run:  

sudo docker compose build app

### check Log
sudo docker logs school_app_container

## 6️⃣. Access Applications

* **FastAPI Docs:** `http://<server-ip>:8000/docs`
* **Grafana:** `http://<server-ip>:3000`
* **SonarQube:** `http://<server-ip>:9000`
* **Prometheus:** `http://<server-ip>:9090`

> **Note:** To connect Grafana to Loki, add the Loki endpoint: `http://loki:3100`.

> **Note:** To connect Grafana to Prometheus, add the Prometheus endpoint: `http://prometheus:9090`.

## 7️⃣. Additional Notes

* Ensure volumes are persisted correctly for Grafana, SonarQube, and Loki.
* Adjust `.env` file as needed for your database and Redis credentials.

## 8️⃣ Without Docker how to check

### instal python 3.10
sudo apt update

sudo apt install software-properties-common -y

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.10 python3.10-venv python3.10-dev -y

python3.10 --version

### create a ENV
#### Create a virtual environment named 'school_env' using Python 3.10
python3.10 -m venv school_env

source school_env/bin/activate
#### Upgrade pip to the latest version
pip install --upgrade pip
#### Install all dependencies listed in requirements.txt
pip install -r requirements.txt
#### Run the FastAPI app using Uvicorn on all network interfaces (0.0.0.0) at port 8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000
#### List all processes listening on network ports (to check if your app is running)
sudo lsof -i -P -n | grep LISTEN

9️⃣
🔟


