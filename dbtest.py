import psycopg2
from psycopg2 import sql

def connect_to_db():
    try:
        with psycopg2.connect(
           user = "postgres",
           password = "Admin123",
           host = "localhost",
           port = "5432",
           database = "ecomdb"
        ) as connection:
            with connection.cursor() as cursor:

                print("Your Database connection is succesfull")

    except (Exception, psycopg2.Error) as error:

        print("Error while connecting to PostgreSQL", error)

# Call the function to connect
if __name__ == "__main__":
    connect_to_db()
 


