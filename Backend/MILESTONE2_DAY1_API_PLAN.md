# Milestone 2 – Backend API Plan

**Intern:** Harshit  
**Branch:** backend-harshit  

---

# Objective

Review all Milestone 1 backend APIs, verify that they are functioning correctly, identify the new APIs required for Milestone 2, and prepare an implementation plan.

---

# Milestone 1 APIs Reviewed

## User Service

- User Registration
- User Login

**Status:** ✅ Working

---

## Course Service

- Get Courses
- Get Lessons
- Get Lesson Details

**Status:** ✅ Working

---

## Business Logic Service

- AI Prediction
- Practice
- Assessment
- Feedback
- Analytics

**Status:** ✅ Working

---

# Existing API Test Results

| API | Status |
|------|--------|
| User Registration | ✅ Passed |
| User Login | ✅ Passed |
| Get Courses | ✅ Passed |
| Get Lessons | ✅ Passed |
| Get Lesson Details | ✅ Passed |
| AI Prediction | ✅ Passed |
| Practice | ✅ Passed |
| Assessment | ✅ Passed |
| Feedback | ✅ Passed |
| Analytics | ✅ Passed |

---

# New APIs Required for Milestone 2

## User Service

### Update Profile

**Method:** PUT

**Endpoint:**
```
/users/profile
```

**Purpose**

- Update user profile information
- Update email
- Update avatar
- Update learning preferences

---

### Change Password

**Method:** PUT

**Endpoint:**
```
/users/change-password
```

**Purpose**

- Allow authenticated users to change their password

---

### Forgot Password

**Method:** POST

**Endpoint:**
```
/users/forgot-password
```

**Purpose**

- Generate password reset request

---

### Reset Password

**Method:** POST

**Endpoint:**
```
/users/reset-password
```

**Purpose**

- Reset password securely using reset token

---

## Instructor APIs

### Get Assigned Students

**Method:** GET

**Endpoint:**
```
/instructor/students
```

**Purpose**

- View assigned students
- Monitor learner progress

---

### View Student Progress

**Method:** GET

**Endpoint:**
```
/instructor/student/{student_id}/progress
```

**Purpose**

- View learner progress reports

---

### View Student Assessments

**Method:** GET

**Endpoint:**
```
/instructor/student/{student_id}/assessments
```

**Purpose**

- View learner assessment history

---

## Admin APIs

### Manage Users

**Methods**

- GET
- POST
- PUT
- DELETE

**Endpoints**

```
/admin/users
/admin/users/{id}
```

**Purpose**

- View all users
- Create new users
- Update user information
- Delete users
- Manage user roles

---

### Dashboard

**Method:** GET

**Endpoint**
```
/admin/dashboard
```

**Purpose**

- View overall platform statistics
- Monitor system activity

---

## Course Service Expansion

### Create Course

**Method:** POST

```
/courses
```

---

### Update Course

**Method:** PUT

```
/courses/{id}
```

---

### Delete Course

**Method:** DELETE

```
/courses/{id}
```

---

### Create Module

**Method:** POST

```
/modules
```

---

### Update Module

**Method:** PUT

```
/modules/{id}
```

---

### Delete Module

**Method:** DELETE

```
/modules/{id}
```

---

### Create Lesson

**Method:** POST

```
/lessons
```

---

### Update Lesson

**Method:** PUT

```
/lessons/{id}
```

---

### Delete Lesson

**Method:** DELETE

```
/lessons/{id}
```

---

# Implementation Plan

## Day 2

- Implement Update Profile API
- Implement Change Password API

---

## Day 3

- Implement Forgot Password API
- Implement Reset Password API

---

## Day 4

- Implement Instructor APIs

---

## Day 5

- Implement Admin APIs

---

## Day 6

- Expand Course, Module, and Lesson CRUD APIs

---

## Day 7

- Perform integration testing
- Fix bugs
- Prepare for Milestone 2 demonstration

---

# Summary

- All Milestone 1 APIs were reviewed.
- Existing APIs were re-tested and verified to be working correctly.
- New APIs required for Milestone 2 have been identified.
- A day-wise implementation plan has been prepared for development.

No modifications to the existing Milestone 1 APIs are required at this stage.

---

# Day 1 Checklist

- [x] Reviewed all Milestone 1 APIs
- [x] Re-tested existing APIs
- [x] Identified new APIs required for Milestone 2
- [x] Prepared implementation plan
- [ ] Shared API plan with teammates
- [ ] Discussed during daily stand-up