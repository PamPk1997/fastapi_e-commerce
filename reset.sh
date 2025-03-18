#!/bin/bash

echo "Stopping containers..."
docker-compose down -v

echo "Removing orphan containers..."
docker system prune -f

echo "Rebuilding..."
docker-compose up --build



