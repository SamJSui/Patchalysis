#!/bin/bash

# Configuration variables
GIT_REPO="https://github.com/SamJSui/Patchalysis.git"
USER="ec2-user"
APP_DIR=/home/$USER/Patchalysis
VENV_DIR=$APP_DIR/venv
SERVICE_NAME="patchalysis.service"

# Pull the latest changes from the repository
cd $APP_DIR
git pull $GIT_REPO

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install/Update dependencies
pip install -r requirements.txt

# Restart the application using systemd
sudo systemctl daemon-reload
sudo systemctl restart $SERVICE_NAME

# Check the status of the application
sudo systemctl status $SERVICE_NAME

# Restart nginx
sudo systemctl restart nginx
sudo systemctl reload nginx
sudo systemctl status nginx

echo "Deployment script executed successfully."
