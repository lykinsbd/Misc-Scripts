#!/bin/bash

# Script to hoff an unattended computer.

# Find a picture of the hoff

curl -o ~/Pictures/hoffin-it http://blahblahblah


# Run openscript to install it as the desktop background

osascript <<EOF
tell application "System Events"
    set desktopCount to count of desktops
    repeat with desktopNumber from 1 to desktopCount
        tell desktop desktopNumber
            set picture to "~/Pictures/hoffin-it"
        end tell
    end repeat
end tell
EOF


