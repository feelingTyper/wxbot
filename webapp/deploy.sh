#!/bin/bash

netstat -lnp|grep 5000 | awk '{print $7}'|awk -F'/' '{print $1}'|xargs -I{} kill -9 {}

[[ ! -h static/stores ]] && ln -s ../../downloads static/stores

nohup python3 webserver.py>/dev/null 2>&1 &
