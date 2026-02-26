#!/bin/bash
set -e

# Update and install Java (Jenkins requires Java 11 or 17)
sudo apt update -y
sudo apt install -y fontconfig openjdk-17-jdk wget gnupg

# Check Java Version
java --version

# Create Directory to store Slave Deployments
mkdir /home/ubuntu/app

#Check Directory Permissions
ls -ld /home/ubuntu/app

# Give Required permissions
sudo chown -R ubuntu:ubuntu /home/ubuntu/app
chmod 755 /home/ubuntu/app
chown ubuntu:ubuntu /home/ubuntu/app
