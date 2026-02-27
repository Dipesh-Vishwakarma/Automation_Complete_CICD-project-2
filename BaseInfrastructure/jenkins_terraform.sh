#!/bin/bash
set -e

# Update and install Java (Jenkins requires Java 17 or 21)
sudo apt update -y
sudo apt install -y fontconfig openjdk-21-jdk wget gnupg

# Add the Jenkins Debian repository and key
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Update package index again after adding Jenkins repo
sudo apt update -y

# Install Jenkins
sudo apt install -y jenkins

# Enable and start Jenkins service
sudo systemctl enable jenkins
sudo systemctl start jenkins

# Show status
sudo systemctl status jenkins --no-pager

#Installing Terraform in Jenkins VM
TERRAFORM_VERSION="1.6.6"

echo "Installing Terraform v${TERRAFORM_VERSION}"

# Install required packages
sudo apt-get update -y
sudo apt-get install -y curl unzip

# Download Terraform
cd /tmp
curl -fsSL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o terraform.zip

# Remove any existing terraform binary to avoid unzip prompt
sudo rm -f /usr/local/bin/terraform

# Unzip and install
unzip -o terraform.zip
sudo mv terraform /usr/local/bin/
sudo chmod +x /usr/local/bin/terraform

# Verify installation
terraform version

echo "Terraform installed successfully"
