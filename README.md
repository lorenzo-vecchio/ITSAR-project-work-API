# API Documentation for Flask Application

This document provides documentation for using the Flask API in the given application.

## Endpoints

The following endpoints are available:

1. `/register` - Register a new user
2. `/login` - Log in a user
3. `/animals` - Manage animal data
4. `/luoghi` - Retrieve location information
5. `/logout` - Log out the user

---

## 1. /register

### Method

- `POST`

### Description

This endpoint allows users to register by providing their username, password, and email.

### Request Body

| Field     | Type   | Required | Description           |
| --------- | ------ | -------- | --------------------- |
| username  | string | Yes      | The username          |
| password  | string | Yes      | The password          |
| mail      | string | Yes      | The email address     |

### Responses

| Status Code | Description                       |
| ----------- | --------------------------------- |
| 200         | Successful registration           |
| 400         | Bad request (missing parameters)  |

---

## 2. /login

### Methods

- `GET`
- `POST`

### Description

This endpoint handles user login functionality.

### Request Body

| Field     | Type   | Required | Description           |
| --------- | ------ | -------- | --------------------- |
| username  | string | Yes      | The username          |
| password  | string | Yes      | The password          |

### Responses

| Status Code | Description                       |
| ----------- | --------------------------------- |
| 200         | Successful login                  |
| 400         | Bad request (missing parameters)  |
| 401         | Invalid username or password       |

---

## 3. /animals

### Methods

- `GET`
- `POST`

### Description

This endpoint allows users to manage animal data.

### Authentication

Authentication is required for this endpoint. The user must be logged in.

### GET Request

This method retrieves animal data for the logged-in user.

### Responses

| Status Code | Description                     |
| ----------- | ------------------------------- |
| 200         | Successful retrieval of animals |
| 401         | Not logged in                   |

### POST Request

This method allows the user to add new animal data.

#### Request Body

| Field             | Type   | Required | Description                            |
| ----------------- | ------ | -------- | -------------------------------------- |
| nome_animale      | string | Yes      | The name of the animal                  |
| sesso             | string | Yes      | The gender of the animal                |
| data_di_nascita   | string | Yes      | The date of birth of the animal         |
| razza             | string | Yes      | The breed of the animal (case-insensitive) |

#### Responses

| Status Code | Description                           |
| ----------- | ------------------------------------- |
| 200         | Successful addition of animal data     |
| 400         | Bad request (missing parameters)      |
| 401         | Not logged in                         |

---

## 4. /luoghi

### Methods

- `GET`

### Description

This endpoint retrieves location information.

### Authentication

Authentication is required for this endpoint. The user must be logged in.

### GET Request

This method retrieves location data.

### Responses

| Status Code | Description                       |
| ----------- | --------------------------------- |
| 200         | Successful retrieval of locations |
| 401         | Not logged in                     |

---

## 5. /logout

### Methods

- `POST`

### Description

This endpoint logs out the user by clearing the session.

### Responses

| Status Code | Description       |
| ----------- | ----------------- |
| 200         | Successful logout |

---

##