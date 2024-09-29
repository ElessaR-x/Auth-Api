# FastAPI Authentication and Admin API

![FastAPI Version](https://img.shields.io/badge/FastAPI-0.1.0-brightgreen)

## Overview
This is a FastAPI project that provides an authentication and admin API with the following functionalities:

- **Authentication**: User registration, login, and token validation.
- **Admin Features**: Managing user permissions, banning users, and HWID resets.
- **Reseller Management**: Reseller license creation.
- **Owner Features**: Changing user roles.

## Getting Started

### Prerequisites
To run this project locally, you need:

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/) installed
- [Uvicorn](https://www.uvicorn.org/) as an ASGI server

### Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    uvicorn main:app --reload
    ```

4. Open your browser and navigate to:

    ```
    http://127.0.0.1:8000/docs
    ```

   You will find the Swagger documentation for the API.

## API Endpoints

### Authentication

| Method | Endpoint        | Description         |
|--------|-----------------|---------------------|
| POST   | `/auth/register`| Register a new user.|
| POST   | `/auth/login`   | User login.         |
| POST   | `/auth/token-check`| Validate a token.|

### Admin

| Method | Endpoint          | Description           |
|--------|-------------------|-----------------------|
| POST   | `/admin/ban`      | Ban a user.           |
| POST   | `/admin/unban`    | Unban a user.         |
| POST   | `/admin/hwid_reset`| Reset HWID for a user.|
| POST   | `/admin/add_time` | Add time to a user.   |
| POST   | `/admin/remove_time` | Remove time from a user. |
| POST   | `/admin/freeze_time` | Freeze a user's time. |

### Reseller

| Method | Endpoint             | Description             |
|--------|----------------------|-------------------------|
| POST   | `/reseller/create_license` | Create a reseller license. |

### Owner

| Method | Endpoint             | Description             |
|--------|----------------------|-------------------------|
| POST   | `/owner/change_role` | Change the role of a user. |

### Customer

| Method | Endpoint                  | Description        |
|--------|---------------------------|--------------------|
| POST   | `/customer/renew_license` | Renew the license. |

## Authorization
To access certain admin and reseller endpoints, you need to be authorized. Click the `Authorize` button in the API documentation and enter the required credentials.

## Schemas
This project contains several request and response schemas:

- **RegisterForm**: Schema for registering a new user.
- **License**: Schema for handling license information.
- **TokenCheckRequest**: Schema for validating access tokens.
- **ValidationError**: Schema for validation errors in requests.

## Swagger UI
The API documentation is available via Swagger UI. You can access it at:

https://professional-faith-colorware-a5c65759.koyeb.app/docs
