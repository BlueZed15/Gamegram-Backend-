# Gamegram API Frontend Guide

## Auth

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

### Sign Up

```http
POST /v1/auth/signup
Content-Type: application/json
```

Request:

```json
{
  "email": "player@example.com",
  "username": "player1",
  "password": "password123"
}
```

Success:

```json
{
  "message": "Sign Up Successful"
}
```

Possible errors:

```text
409 Username already exists
409 Email already exists
422 Validation error
```

### Login

```http
POST /v1/auth/login
Content-Type: application/x-www-form-urlencoded
```

Form fields:

```text
username=player1
password=password123
```

Success:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

Use the token on protected requests:

```http
Authorization: Bearer jwt-token
```

### Current User

```http
GET /v1/auth/getuser
Authorization: Bearer <access_token>
```

Success:

```json
{
  "id": "user-uuid",
  "email": "player@example.com",
  "username": "player1",
  "avatar_url": null,
  "bio": null,
  "created_at": "2026-05-28T10:00:00"
}
```

## Sandboxes

### List Sandboxes

```http
GET /sandboxes/
```

Success:

```json
[
  {
    "id": "sandbox-uuid",
    "name": "test",
    "sandbox_url": "https://...",
    "runnable_url": null
  }
]
```

### Select Sandbox

Returns a runnable game URL for the selected sandbox.

```http
GET /sandboxes/select/{sandbox_id}
Authorization: Bearer <access_token>
```

Success:

```json
{
  "id": "sandbox-uuid",
  "name": "test",
  "sandbox_url": "https://...",
  "runnable_url": "http://127.0.0.1:8000/sandboxes/sandbox-uuid/files/index.html?mode=edit&sandbox_id=sandbox-uuid&creator_id=user-uuid"
}
```

The frontend/webview should open `runnable_url`.


## Games

### Game Feed

```http
GET /games/?counter=1
```

Success:

```json
{
  "counter": 1,
  "total": 10,
  "games": [
    {
      "game_id": "game-uuid",
      "title": "Untitled",
      "creator_id": "user-uuid",
      "creator_name": "player1",
      "like_count": 0,
      "dislike_count": 0,
      "play_count": 0,
      "runnable_url": "http://127.0.0.1:8000/sandboxes_data/test/index.html?mode=noedit&game_id=game-uuid",
      "icon_url": null,
      "created_at": "2026-05-28T10:00:00"
    }
  ]
}
```

### Single Game

```http
GET /games/{game_id}
```

Success:

```json
{
  "game_id": "game-uuid",
  "title": "Untitled",
  "creator_id": "user-uuid",
  "creator_name": "player1",
  "like_count": 0,
  "dislike_count": 0,
  "play_count": 0,
  "runnable_url": "http://127.0.0.1:8000/sandboxes_data/test/index.html?mode=noedit&game_id=game-uuid",
  "icon_url": null,
  "created_at": "2026-05-28T10:00:00"
}
```

## Frontend Notes

- Store the `access_token` after login.
- Send `Authorization: Bearer <access_token>` for protected endpoints.
- Open sandbox `runnable_url` in the webview.
- The WebGL game should include the bearer token when calling protected backend endpoints.
- Do not put long-lived access tokens in public URLs in production.
