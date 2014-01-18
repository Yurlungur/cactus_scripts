#!/usr/bin/env sh

# A simple little function that adds simfactory sim script to your
# list of shell commands like "ls." This means you can run sim from
# anywhere on your computer, which is handy.

# Add cactus
CACTUS_DIRECTORY=/home/jonah/Storage/programming/Cactus
SIM_LOCATION=simfactory/bin/sim
sim () {
    OLD_PWD=$(pwd)
    cd $CACTUS_DIRECTORY
    $SIM_LOCATION $@
    cd $OLD_PWD
}