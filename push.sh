#!/bin/bash
git add .
read -p "Enter commit message: " msg
git commit -m "$msg"
echo "Pushing to remote repository..."
git push
echo "Push successful!"