#!/bin/bash

python3 manage.py runserver 0.0.0.0:8000 &
redis-server /etc/redis/redis.conf &
python3 manage.py rqworker default &
tail -f /dev/null