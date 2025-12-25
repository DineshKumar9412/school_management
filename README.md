# school_management

# git clone
git clone https://github.com/DineshKumar9412/school_management.git

# install docker
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

docker compose version
docker --version

# chnage direcory
cd school_management

# .env file creation
DB_USER="root"
DB_PASSWORD="root@123"
DB_HOST="3.110.91.230"
DB_NAME="sampledb"
REDIS_HOST="3.110.91.230"
REDIS_PORT="6379"
REDIS_PASSWORD="Redis@123"

# sonerquser chnages
# Run this once on the host:
sudo sysctl -w vm.max_map_count=524288

# Make it permanent:
echo "vm.max_map_count=524288" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# docker run
sudo docker compose up -d
docker compose up loki
docker compose build


# docker check 
sudo docker ps

# docker down 
sudo docker compose down

# docker log 


# check FASTAPI 
serverip : 8000/docs

# check Grafan 
serverip : 3000

ad loki endpoint to ad source 
http://loki:3100







