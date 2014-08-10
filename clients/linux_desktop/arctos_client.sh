#!/bin/bash

if [ $# != 2 ]
then
  echo "Usage : $0 header serverinfo"
  echo "        $0 'New notification' 'http://localhost:8080/channel'"
  exit 1
fi

header=$1
listen=$2

while sleep 1
do
  message="$(wget -qO- $2)"
  notify-send "$1" "$message"
done
