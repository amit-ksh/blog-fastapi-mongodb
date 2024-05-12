#!/bin/bash

source .env.dev

echo "Running migrations"
beanie migrate -uri $DATABASE_URL -p database/migrations -d 1

echo "Migrations completed"
read -n 1 -s -r -p "Press any key to exit"