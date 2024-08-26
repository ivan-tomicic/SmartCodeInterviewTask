# Football Management API

This Django-based API provides endpoints for managing football teams, players, and coaches. It allows creating, retrieving, updating, and deleting teams, players, and coaches, as well as managing their relationships.

## Setup and Running the Application

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Steps to Run the Application

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Install PostgreSQL if you haven't already (https://www.postgresql.org/download/)
   - Open a PostgreSQL shell or use a GUI tool like pgAdmin
   - Connect to PostgreSQL as a superuser (usually 'postgres'):
     ```
     psql -U postgres
     ```
   - Create a new database:
     ```sql
     CREATE DATABASE football_management;
     ```
   - Create a new user:
     ```sql
     CREATE USER your_username WITH PASSWORD 'your_password';
     ```
   - Grant necessary permissions to the user:
     ```sql
     GRANT ALL PRIVILEGES ON DATABASE football_management TO your_username;
     ALTER USER your_username CREATEDB;
     ```
   - Connect to the new database:
     ```sql
     \c football_management
     ```
   - Grant schema usage and create privileges to the new user:
     ```sql
     GRANT USAGE, CREATE ON SCHEMA public TO your_username;
     ```
   - Exit the PostgreSQL shell:
     ```
     \q
     ```

5. Create a `.env` file in the project root and add your database configuration:
   ```
   DB_NAME=football_management
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

### Accessing the Swagger Documentation

Once the server is running, you can access the Swagger UI at:

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

I have also included the export of the Postman collection as a JSON file in the root directory (Football Management API.postman_collection.json).

This will provide an interactive interface to explore and test the API endpoints.
