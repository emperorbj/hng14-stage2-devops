#!/bin/bash
echo "creating docker files"
read -p "Enter the directory: " dir
cd $dir
touch Dockerfile
touch .dockerignore
echo "Docker files created successfully in $dir"