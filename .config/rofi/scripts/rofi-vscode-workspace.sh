#!/bin/bash

# Directory where your workspace files are located
workspace_dir="$HOME/Documents/VSCode Workspace/"

# Get a list of workspace filenames without extension
workspaces=$(find "$workspace_dir" -type f -name "*.code-workspace" -exec basename {} \; | sed 's/\.code-workspace$//')

# Use Rofi to display the workspace selection menu
selected_workspace=$(echo "$workspaces" | rofi  -sort -sorting-method fzf -dmenu -i -p "Select a workspace:")

# If a workspace is selected, open VS Code with that workspace
if [ -n "$selected_workspace" ]; then
   code "--new-window" "--folder-uri" "file://$workspace_dir/$selected_workspace.code-workspace"
fi