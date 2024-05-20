## A fastapi based web application for IOT

- To run the project
    - Close the repository
    - Create a python virtual environment and activate it.
    - Make a file named ``.env``
    - Copy all from ``example.env`` to ``.env``
    - Change the db configuration as required.
    - Run migrations command
  ```bash
    alembic revision --autogenerate -m "initial migrations"
    alembic upgrade head
  ```
    - Then run the server 
  ```bash
    uvicorn src.main:app --reload
    ```