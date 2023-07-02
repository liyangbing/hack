#!/bin/bash

start() {
  nohup python server/server.py > nohup-backgroud.out &
  nohup streamlit run admin/qa.py --server.port 50001 > nohup-front.out &
}

stop() {
  kill $(ps aux | grep 'python server/server.py' | grep -v grep | awk '{print $2}')
  kill $(ps aux | grep 'streamlit run admin/qa.py' | grep -v grep | awk '{print $2}')
}

restart() {
  stop
  sleep 2
  start
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    restart
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
esac

tail -f nohup-backgroud.out nohup-front.out

exit 0
