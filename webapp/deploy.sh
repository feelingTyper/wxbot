#!/bin/bash

ln -s ../../downloads static/stores
nohup python3 webserver.py>/dev/null 2>&1 &
