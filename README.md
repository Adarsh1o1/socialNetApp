# Social Networking Application

This is a simple social networking application built with Django and Django REST Framework (DRF). The application supports user authentication, friend requests, and basic CRUD operations on user profiles. It uses SQLite for the database and Docker for containerization.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)

## Technologies Used

- **Python**: Programming language
- **Django**: Web framework
- **Django REST Framework (DRF)**: Framework for building APIs
- **JWT AUTHENTICATION**: Javascript web token for authentication
- **SQLite**: Database for storing application data
- **Docker**: Containerization tool
- **Docker Compose**: Tool for defining and running multi-container Docker applications

## Features

- User authentication (signup, login, logout)
- Send, accept, and reject friend requests
- List friends and pending friend requests
- Search users by name or email
- Limit friend request submissions to three per minute

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: [Download and install Docker](https://www.docker.com/products/docker-desktop)
- **Docker Compose**: Comes with Docker Desktop

## Installation

### Step 1: Clone the Repository

git clone https://github.com/yourusername/social-networking-app.git
cd social-networking-app

### Step 2: Build Docker Image and run containers

docker-compose build
docker-compose up

This command will start the application on http://127.0.0.1:8000.

### Step 3 Access Api end points
### [Postman collection is added in main branch of this repo.](https://github.com/Adarsh1o1/socialNetApp/blob/main/Social%20networking%20site.postman_collection.json)
- **Signup**:
POST method
http://127.0.0.1:8000/api/myapp/signup/
Request body
```bash
{
  "email":"lucasadarsh@gmail.com",
  "username":"lucas",
  "password":"Adarsh@123",
  "password2":"Adarsh@123"
}
```
-  **Login**:
POST method
http://127.0.0.1:8000/api/myapp/login/
Request body:
```bash
{
  "email":"lucasadarsh@gmail.com",
  "password":"Adarsh@123"
}
```
Get the access token from response and must to use this token to access other api endpoint except login and signup
**Make sure to pass bearer token in headers**

Search firends by username or email:
GET method
http://127.0.0.1:8000/api/myapp/users/?search=kashish

- **Send firend requests**:
POST method
```bash
http://127.0.0.1:8000/api/myapp/friend-requests/
Request body:
{
  "to_user": 2
}
```
you will get a firend request id, status etc in response for future use

- **Accept Request**:
POST method
http://127.0.0.1:8000/api/myapp/friend-requests/id/accept/
NOTE: Put id in above url which you get form send firend request api like replace with id with 2 or 3(whatever id u recieved in response form send firend request api)
Request body:
```bash
{
    "action": "accept"

}
```

- **Reject Request**:
POST method
http://127.0.0.1:8000/api/myapp/friend-requests/id/reject/
NOTE: Put id in above url which you get form send firend request api like replace with id with 2 or 3(whatever id u recieved in response form send firend request api)
Request body:
```bash
{
    "action": "reject"
}
```

- **To see list of pending requests**:
GET method
http://127.0.0.1:8000/api/myapp/friend-requests/list_pending_requests

- **To see list of friends**s:
GET method
http://127.0.0.1:8000/api/myapp/friend-requests/list_friends

### NOTE: Make sure to provide Bearer token in headers to access Api endpoints except login and signup


