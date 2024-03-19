## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Rafin000/api_building_with_flask.git
    ```
 
2. Navigate into the project directory:

    ```bash
    cd your-repository
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

      ```bash
      source venv/bin/activate
      ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set up environment variables
2. Run the Flask application:

    ```bash
    python3 manage.py run --port 5000
    ```

3. Open your web browser and navigate to `http://localhost:5000` to view the application.


## Migration

1. Migrate the Database

    ```bash
    alembic revision --autogenerate -m "Your migration message"
    alembic upgrade head
    ```
2. To rollback the migration

    ```bash
    alembic downgrade -1
    ```


