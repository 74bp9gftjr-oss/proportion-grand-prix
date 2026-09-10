#!/bin/bash
# Double-click this to stop the race server if you left one running.
clear
n=$(pgrep -f "race_server.py" | wc -l | tr -d ' ')
if [ "$n" = "0" ]; then
  echo
  echo "  No race server was running."
else
  pkill -f "race_server.py"
  sleep 1
  echo
  echo "  Stopped $n race server(s)."
fi
echo
read -r -p "  Press Return to close. "
