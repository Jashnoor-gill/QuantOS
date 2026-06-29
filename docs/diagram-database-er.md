erDiagram
  USERS ||--o{ USERS : creates
  USERS {
    int id PK
    string email UNIQUE
    string username UNIQUE
    string hashed_password
    bool is_active
    datetime created_at
  }

  %% Note: Expand this ER diagram as additional domain models are finalized.
