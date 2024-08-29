#!/bin/bash

# Run the API in a new xterm window
xterm -e "cd ./src/api && python3 main.py; exec bash" &

# Run the GUI server in another new xterm window
xterm -e "cd ./src/gui && python3 server.py; exec bash" &

# Wait a few seconds to ensure the servers are up
sleep 10

# Open the application in the default web browser
xdg-open http://127.0.0.1:5050/
