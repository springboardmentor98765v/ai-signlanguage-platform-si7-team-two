# AI-Powered Sign Language Learning & Assessment Platform

## Backend API Contract (Milestone 1)

**Developer:** Backend Intern

**Version:** 1.0

---

# Authentication APIs

## 1. Register User

### Endpoint

POST /auth/register

### Request

```json
{
  "full_name": "Harshit Amit Paradeshi",
  "email": "harshit@example.com",
  "password": "Password@123",
  "role": "Learner"
}
```

### Response

```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

### Status Codes

- 201 Created
- 400 Bad Request
- 409 Conflict

---

## 2. Login User

### Endpoint

POST /auth/login

### Request

```json
{
  "email": "harshit@example.com",
  "password": "Password@123"
}
```

### Response

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "Bearer"
}
```

### Status Codes

- 200 OK
- 401 Unauthorized

---

# Course APIs

## 3. Get All Courses

### Endpoint

GET /courses

### Response

```json
[
  {
    "id": 1,
    "title": "Alphabet Course",
    "level": "Beginner"
  }
]
```

---

## 4. Get Course By ID

### Endpoint

GET /courses/{id}

### Response

```json
{
  "id": 1,
  "title": "Alphabet Course",
  "level": "Beginner",
  "description": "Learn A-Z Sign Language"
}
```

---

## 5. Create Course

### Endpoint

POST /courses

### Request

```json
{
  "title": "Alphabet Course",
  "level": "Beginner",
  "description": "Learn A-Z Sign Language"
}
```

### Response

```json
{
  "message": "Course created successfully"
}
```

---

## 6. Update Course

### Endpoint

PUT /courses/{id}

### Request

```json
{
  "title": "Alphabet Course Updated",
  "level": "Intermediate"
}
```

### Response

```json
{
  "message": "Course updated successfully"
}
```

---

## 7. Delete Course

### Endpoint

DELETE /courses/{id}

### Response

```json
{
  "message": "Course deleted successfully"
}
```

---

# Authentication

JWT Bearer Token

Example:

Authorization: Bearer <JWT_TOKEN>

---

# User Roles

- Learner
- Instructor
- Trainer
- Admin

---

# Standard HTTP Status Codes

| Code | Description |
|------|-------------|
|200|OK|
|201|Created|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|500|Internal Server Error|