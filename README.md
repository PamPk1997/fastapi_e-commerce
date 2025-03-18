
FastAPI Project

This is a FastAPI-based web application designed for efficient development and deployment. This guide provides setup instructions for running the project locally and with Docker.

--------------------------------------------------------------------------

Getting Started

1. Prerequisites
Ensure you have the following installed:
- Python 3.12+
- PostgreSQL
- Docker and Docker Compose 

--------------------------------------------------------------------------

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Copy the provided `.env.example` file and update it as needed:

cp .env.example .env

Set values for the following keys:
- `DATABASE_URL`: Database connection string (e.g., `postgresql://user:password@localhost/db_name`).

--------------------------------------------------------------------------

Running the Project Locally

1. Apply Migrations
Run the database migrations:

alembic upgrade head


2. Start the Server

uvicorn app.main:app --reload

The project will be available at http://127.0.0.1:8000/docs.

--------------------------------------------------------------------------

Running the Project with Docker

1. Update Configuration Files
To run the project using Docker, you need to make the following changes:

.env File
In the `.env` file, update the `DATABASE_URL` host from `localhost` to `db`:

DATABASE_URL=postgresql://user:password@db/db_name


alembic.ini File
In the `alembic.ini` file, update the database connection string:

sqlalchemy.url = postgresql://user:password@db/db_name


2. Build and Start Containers
Build the Docker images and start the containers using Docker Compose:

docker-compose up --build

4. Access the Application

The application will be available at http://localhost:8000/docs.

--------------------------------------------------------------------------

Key Commands
--> run docker container 
--> docker-compose up 

Stop Docker Containers

--> docker-compose down


Troubleshooting

1. Docker Issues
- If you encounter errors, ensure that the `.env` and `alembic.ini` files are correctly configured for Docker.

2. Database Issues
- Confirm that the database service is running and reachable. For Docker, the host must be `db`.

3. Apply Migrations
- If migrations fail, ensure the database is up-to-date and the `DATABASE_URL` is correct.

--------------------------------------------------------------------------


Reset script

If you stuck where you want to reset the whole docker config like containers and volumes 
simply run the reset.sh script 

# ./reset.sh soft   -> just rebuild
# ./reset.sh hard   -> wipe volumes too
