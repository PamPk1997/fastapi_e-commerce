#!/bin/bash

echo "Stopping containers..."
docker-compose down -v

echo "Removing orphan containers..."
docker system prune -f

docker volume rm -rf ecom_postgres_data



