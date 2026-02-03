# Django + PostgreSQL backend

## Prerequisites

- **Docker Engine**
- **Docker Compose v2** plugin

## Setup

1. create a `.env` file

```sh
POSTGRES_USER = # user
POSTGRES_PASSWORD = # password
POSTGRES_DB = # database name

SECRET_KEY = # secret key
DATABASE_URL = # url
```

or look at the shared drive for mine

_might need to use sudo_

docker compose build

docker compose up

docker exec -it django python manage.py migrate

_check http://localhost:8000/ to confirm it worked_

_optionally run **docker exec -it django python manage.py createsuperuser** to create admin acc_

## Useful Commands

- **docker compose down** (stop everything)
- **docker compose up** (start)

- **docker exec -it postgres psql -U postgres** (access area to run postgres commands)
- **\c <database_name>** _just do \c for default db_ (enter a database)
- **\d** (view stuff in the db you entered)
- **\d+ <table_name>**
- **\q** (quit)

- **docker exec -it django bash** (enter container for the backend)
- run commands for django here and other related stuff

## Tips
- NEVER run pip install .... instead add it to requirements.txt
  - sudo docker compose up --build
- Don't run django commands outside of the docker container (explanation on how to enter in commands section)

## Models

### Accounts
```mermaid
erDiagram
    USER {
        UUID id PK
        string email
        string username
        string first_name
        string last_name
        string visibility
        smallint xp
        smallint level
        smallint grad_year
        string discord
        string instagram
        string github
        string linkedin
        text bio
        json blocked
        datetime updated_at
        datetime date_joined
    }

    SCHOOL {
        int id PK
        string name
    }

    MAJOR {
        int id PK
        string name
    }

    SKILL {
        int id PK
        string name
    }

    INTEREST {
        int id PK
        string name
    }

    %% --- Many-To-Many Relations ---
    USER ||--o{ USER_SKILLS : "has"
    SKILL ||--o{ USER_SKILLS : "used by"

    USER ||--o{ USER_INTERESTS : "has"
    INTEREST ||--o{ USER_INTERESTS : "chosen by"

    USER_SKILLS {
        UUID user_id FK
        int skill_id FK
    }

    USER_INTERESTS {
        UUID user_id FK
        int interest_id FK
    }

    %% --- Many-To-One ( User -> School/Major ) ---
    SCHOOL ||--o{ USER : "has many"
    MAJOR  ||--o{ USER : "has many"
```
