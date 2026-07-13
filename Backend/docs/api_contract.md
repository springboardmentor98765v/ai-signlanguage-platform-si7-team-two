# AI-Powered Sign Language Learning & Assessment Platform

## Backend API Contract (Milestone 1)

**Developer:** Backend Intern

**Version:** 1.0

> **Note:** This document reflects the APIs currently implemented in Milestone 1.
> Some endpoints planned in the Software Requirements Specification (SRS) will be added in later milestones.

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
  "password": "Password@123"
}
```

### Response

```json
{
  "id": "6f3c2db2-f991-45b4-a55b-3a4a8e2f9d98",
  "full_name": "Harshit Amit Paradeshi",
  "email": "harshit@example.com",
  "role_id": "54d6bda5-79d5-4dd7-93d2-315d4fc0f66a"
}
```

### Status Codes

- 200 OK
- 400 Bad Request

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
  "message": "Login successful",
  "user": {
    "id": "6f3c2db2-f991-45b4-a55b-3a4a8e2f9d98",
    "full_name": "Harshit Amit Paradeshi",
    "email": "harshit@example.com",
    "role_id": "54d6bda5-79d5-4dd7-93d2-315d4fc0f66a"
  }
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

Authentication is currently under development.

JWT authentication will be implemented in a future milestone.

Current login endpoint validates user credentials and returns user details.

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

| Code | Description           |
| ---- | --------------------- |
| 200  | OK                    |
| 201  | Created               |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 409  | Conflict              |
| 500  | Internal Server Error |
