# Blog App

A simple blog app built using FastAPI, Beanie ODM and MongoDB.

## Local development setup

1. Clone the repo: `git clone https://github.com/amit-ksh/blog-fastapi-mongodb.git`

1. Install packages:
    ```bash
        cd blog-fastapi-mongodb
        pip install -r requirements.txt
    ```

1. Copy `.env.sample`, rename to `.env.dev` and fill up the variables value
    ```bash
        DATABASE_URL="DB_URL"
        secret_key="SECRET"
    ```

1. Run DB migrations: `scripts/run-migrations.sh`

1. Start the server: `scripts/start-app.sh`. Server running at `http://localhost:8080/`

*Swagger API docs at http://localhost:8080/docs#/*

