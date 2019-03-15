#!/bin/sh

# #########
# preparing
# #########

adduser ubuntu
usermod -aG sudo ubuntu

mkdir /home/ubuntu/.ssh
cp /root/.ssh/authorized_keys /home/ubuntu/.ssh/authorized_keys

ufw app list
ufw allow OpenSSH
yes y | ufw enable
ufw status
apt update -y && apt install -y mc

# ##############
# install docker
# ##############

sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo apt install -y docker-compose

usermod -aG docker ubuntu

docker info
