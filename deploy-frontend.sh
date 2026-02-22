#!/bin/bash
# Build and push frontend Docker image to Docker Hub
# Remember to run docker desktop first

set -e  # Stop on any error

echo "Building Docker image..."
docker build -t resume-frontend ./my-resume-app/

echo "Tagging image..."
docker tag resume-frontend tristesse02/resume-frontend:latest

echo "Pushing to Docker Hub..."
docker push tristesse02/resume-frontend:latest

echo "Done! Go to Render and trigger a Manual Deploy."
