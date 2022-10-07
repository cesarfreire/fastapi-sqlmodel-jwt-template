
# FastAPI + SQLModel + JWT Auth template


Basic template to run FastAPI application, with SQLModel and JWT authentication.
## Installation

You need [Poetry](https://python-poetry.org/docs/ "Install Poetry") installed.

```bash
  git clone <this-repo-url>
  
  cd fastapi-sqlmodel-jwt-template/

  poetry install
```

And wait until poetry install finish.
    
## Run

To run this project:

```bash
  poetry shell
```

Run the API:
```bash
  uvicorn fastapi_jwt_template.main:app --port 7777
```

Check: http://localhost:7777/docs



#### You can change the port number.
## Badges


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
