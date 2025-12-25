# School Management

A Dockerized school management system with FastAPI, PostgreSQL, Redis, Grafana, Loki, Promtail, and SonarQube.

## Prerequisites

* Ubuntu 20.04+
* Git
* Docker & Docker Compose

## 1. Clone the Repository

git clone https://github.com/DineshKumar9412/school_management.git

### Change Dirctory
cd school_management

## 2. Install Docker and Docker Compose

sudo apt update && sudo apt upgrade -y

sudo apt install -y apt-transport-https ca-certificates curl software-properties-common lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

### Check installation:
docker --version

docker compose version


## 3. Create `.env` File

### Create a `.env` file in the project root:

DB_USER="root"

DB_PASSWORD="root@123"

DB_HOST="3.110.91.230"

DB_NAME="sampledb"

REDIS_HOST="3.110.91.230"

REDIS_PORT="6379"

REDIS_PASSWORD="Redis@123"


## 4. Configure SonarQube

### Set the `vm.max_map_count` for SonarQube:

### Temporary
sudo sysctl -w vm.max_map_count=524288

### Permanent
echo "vm.max_map_count=524288" | sudo tee -a /etc/sysctl.conf

sudo sysctl -p

## 5. Run Docker Compose

### Start all services:
sudo docker compose up -d

### Build the app container if needed:
docker compose build

### Check logs for troubleshooting:
docker compose logs -f

### Check running containers:
sudo docker ps

### Stop all services:
sudo docker compose down

## 6. Access Applications

* **FastAPI Docs:** `http://<server-ip>:8000/docs`
* **Grafana:** `http://<server-ip>:3000`
* **SonarQube:** `http://<server-ip>:9000`

> **Note:** To connect Grafana to Loki, add the Loki endpoint: `http://loki:3100`.

## 7. Additional Notes

* Ensure volumes are persisted correctly for Grafana, SonarQube, and Loki.
* Adjust `.env` file as needed for your database and Redis credentials.

