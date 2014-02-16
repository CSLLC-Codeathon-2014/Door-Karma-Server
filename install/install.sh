#!/bin/bash
TARGET=/usr/local/
CONFIG=/etc/doorkarma/

echo "Welcome to the installer for the door karma server!"
read -p "We will now begin the installation, press C-c now to cancel or [ENTER] to procede"

echo "I need root privileges to install..."
sudo apt-get update
sudo apt-get install -y mysql-server phpmyadmin python python-mysqldb python-flask

echo "Now I will copy the files into the target folder($TARGET))"
sudo mkdir -p $TARGET
sudo cp src/*.py $TARGET

echo "Now I will copy the config data into place ($CONFIG)"
sudo mkdir -p $CONFIG
sudo cp src/*.json $CONFIG

echo "Now I will link the init script in."
sudo ln -s /etc/init.d/doorKarma $TARGET/doorKarma.py

echo "Now I will start the service."
/etc/init.d/doorKarma start

echo "DONE!"
exit(0)
