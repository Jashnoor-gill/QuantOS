flowchart LR
  U[User] -->|Open login/register| FE[React Frontend]
  FE -->|POST /auth/login or /auth/register| BE[FastAPI Backend]
  BE -->|Validate JWT & return token| FE

  FE -->|Attach Authorization: Bearer <token>| BE
  BE -->|Protected APIs| ENGINES[Engines/Modules]
  BE --> DB[(SQL Database)]

  ENGINES --> BE
  BE --> FE
