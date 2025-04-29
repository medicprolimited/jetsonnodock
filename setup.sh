#!/bin/bash

# Create new directory structure
mkdir -p /home/mx/jetsonnodock/backend
mkdir -p /home/mx/jetsonnodock/frontend

# Move backend files
cp -r backend/* /home/mx/jetsonnodock/backend/
cp README.md /home/mx/jetsonnodock/

# Move frontend files
cp -r frontend/* /home/mx/jetsonnodock/frontend/

# Set permissions
chown -R mx:mx /home/mx/jetsonnodock

echo "Directory structure has been updated to use jetsonnodock" 