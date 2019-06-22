#!/bin/bash
export PYTHONUNBUFFERED=1
cd /data/svr/MyFastDFS
/data/svr/python3/bin/python3  manage.py runserver 0.0.0.0:80 > ./server.log 2>&1 &
echo "end"
