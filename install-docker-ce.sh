#!/bin/bash
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
# Ubuntu
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# Kali
#curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
#echo 'deb [arch=amd64] https://download.docker.com/linux/debian buster stable' | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
