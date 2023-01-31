# neon database connect

## Setup
- Create python virtual environment
- Install python dependencies: `pip install -r requirements.txt`
- Create _.env_ file in this directory with neon database information. Should look like the following:
  ```
  POSTGRES_USER=username
  POSTGRES_PASSWORD=password
  POSTGRES_DATABASE=db_name
  POSTGRES_CONNECTION=connection-string
  POSTGRES_ENDPOINT=endpoint-string
  ```