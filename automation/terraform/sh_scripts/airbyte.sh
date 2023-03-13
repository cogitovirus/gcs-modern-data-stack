#! /bin/bash
curl -sSO https://dl.google.com/cloudagents/add-logging-agent-repo.sh
sudo bash add-logging-agent-repo.sh --also-install
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add --
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian buster stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -a -G docker $USER
sudo apt-get -y install docker-compose-plugin
docker compose version
mkdir airbyte && cd airbyte
curl -sOO https://raw.githubusercontent.com/airbytehq/airbyte/master/.env
curl -sOO https://raw.githubusercontent.com/airbytehq/airbyte/master/docker-compose.yaml
curl -sOO https://raw.githubusercontent.com/airbytehq/airbyte/master/flags.yml
docker compose up -d