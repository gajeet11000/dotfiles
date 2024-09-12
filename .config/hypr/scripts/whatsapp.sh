#!/bin/bash

# Define the window title to look for
WINDOW_TITLE="web.whatsapp.com"

# Define the command to run if the window is not found
COMMAND="google-chrome-stable --app=https://web.whatsapp.com"

# Use hyprctl to get the list of windows in JSON format and check for the title
if ! hyprctl clients -j | jq -e --arg title "$WINDOW_TITLE" '.[] | select(.title == $title)' > /dev/null; then
    # Run the command if the window is not found
    $COMMAND
fi

