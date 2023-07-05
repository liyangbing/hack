#!/bin/bash

current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Current time: $current_time"

start() {
  echo "Starting server..." | tee -a nohup-backgroud.out nohup-front.out
  start_time=$(date +%s)
  nohup python server/server.py > nohup-backgroud.out 2>&1 &
  nohup streamlit run admin/qa.py --server.port 50001 > nohup-front.out 2>&1 &
  disown %1
  disown %2
  end_time=$(date +%s)
  elapsed_time=$((end_time - start_time))
  echo "Server started, time taken: $elapsed_time seconds" | tee -a nohup-backgroud.out nohup-front.out
}

stop() {
  echo "Stopping server..." | tee -a nohup-backgroud.out nohup-front.out
  start_time=$(date +%s)
  kill $(ps aux | grep 'python server/server.py' | grep -v grep | awk '{print $2}')
  kill $(ps aux | grep 'streamlit run admin/qa.py' | grep -v grep | awk '{print $2}')
  end_time=$(date +%s)
  elapsed_time=$((end_time - start_time))
  echo "Server stopped, time taken: $elapsed_time seconds" | tee -a nohup-backgroud.out nohup-front.out
}

restart() {
  echo "Restarting server..." | tee -a nohup-backgroud.out nohup-front.out
  start_time=$(date +%s)
  stop
  sleep 2
  start
  end_time=$(date +%s)
  elapsed_time=$((end_time - start_time))
  echo "Server restarted, time taken: $elapsed_time seconds" | tee -a nohup-backgroud.out nohup-front.out
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


current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Current time: $current_time"

exit 0
