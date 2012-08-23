#!/bin/bash

if [[ $1 == "" || $2 == "" ]]; then
    echo "Please enter VISITHOME location and Python Binary location"
    exit 0
fi
export PYTHONBIN=$2

if [[ ! -e $PYTHONBIN/python ]]; then
   echo "Python bin $PYTHONBIN does not contain python executable"
   exit 0
fi 

export VISITHOME=$1
export VISITPLUGINDIR=$VISITHOME/plugins
export PATH=$VISITHOME/bin:$PYTHONBIN:$PATH
export PYTHONPATH=$VISITHOME/lib/site-packages

$PYTHONBIN/python server_example.py
