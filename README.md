## A fastapi based web application for IOT

- To run the project
    - Close the repository
    - Create a python virtual environment and activate it.
    - Make a file named ``.env``
    - Copy all from ``example.env`` to ``.env``
    - Change the db configuration as required.
    - Then run the command to create db tables ```python3 create_db.py```
    - Then run the server 
   ```bash
  uvicorn src.main:app --reload
  ```