#!/bin/bash
# ---------------------------------------------------------------
#  Double-click this to let your class race each other.
#  Keep the window that opens OPEN for the whole lesson.
#  Closing it stops the race.
# ---------------------------------------------------------------
cd "$(dirname "$0")" || { echo "Could not find the game folder."; read -r; exit 1; }

printf '\033]0;Proportion Grand Prix - race server\007'   # name the window
[ -t 1 ] && clear                                          # only in a real window

if [ ! -f "race_server.py" ]; then
  echo
  echo "  Could not find race_server.py next to this file."
  echo "  Keep all the game files together in one folder."
  echo
  read -r -p "  Press Return to close. "
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo
  echo "  python3 is not installed on this Mac, so the class race cannot run."
  echo "  The game still works on its own - just open Proportion Grand Prix.html."
  echo
  read -r -p "  Press Return to close. "
  exit 1
fi

python3 "race_server.py"
status=$?

echo
if [ $status -ne 0 ]; then
  echo "  The server stopped unexpectedly (exit code $status)."
  echo "  The message above says why."
else
  echo "  Server stopped. The class race is now off."
fi
echo
read -r -p "  Press Return to close this window. "
