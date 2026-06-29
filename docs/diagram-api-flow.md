sequenceDiagram
  participant Browser as Browser
  participant FE as Frontend
  participant API as FastAPI
  participant DB as Database

  Browser->>FE: Enter credentials
  FE->>API: POST /auth/login
  API->>DB: Find user by email
  DB-->>API: user record
  API-->>FE: access_token

  Browser->>FE: Navigate to protected page
  FE->>API: GET /auth/me (or protected endpoint)
  API->>API: Decode & validate JWT
  API-->>FE: user info / protected data
