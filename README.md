# API Usage Documentation

This documentation provides information about the usage of the API endpoints available in the provided Flask application. The API allows users to register, log in, manage animals, retrieve services, and log out.

## Base URL

The base URL for accessing the API endpoints is: `https://itsar-project-work-api.vercel.app/`

```
## Endpoints

### Register

**URL**: `/register`

**Method**: `POST`

This endpoint allows users to register an account.

#### Request Parameters

| Parameter | Type   | Description            |
|-----------|--------|------------------------|
| username  | string | The username of the user|
| password  | string | The password of the user|
| mail      | string | The email of the user   |

#### Request Example

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "username": "john_doe",
  "password": "password123",
  "mail": "john.doe@example.com"
}' http://localhost:5000/register
```

#### Response Example

```
Status: 200 OK
```

### Login

**URL**: `/login`

**Method**: `POST`

This endpoint allows users to log in to their account.

#### Request Parameters

| Parameter | Type   | Description            |
|-----------|--------|------------------------|
| username  | string | The username of the user|
| password  | string | The password of the user|

#### Request Example

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "username": "john_doe",
  "password": "password123"
}' http://localhost:5000/login
```

#### Response Example

```
Status: 200 OK
```

### Logout

**URL**: `/logout`

**Method**: `POST`

This endpoint allows users to log out of their account.

#### Request Example

```bash
curl -X POST http://localhost:5000/logout
```

#### Response Example

```
Status: 200 OK
```

### Animals

**URL**: `/animals`

**Method**: `GET`

This endpoint allows authenticated users to retrieve a list of animals associated with their account.

#### Request Example

```bash
curl -X GET -H "Authorization: Basic base64(username:password)" http://localhost:5000/animals
```

#### Response Example

```
Status: 200 OK

[
  {
    "nomeAnimale": "Max",
    "sesso": "M",
    "data_di_nascita": "2020-01-01",
    "nomeRazza": "Labrador Retriever",
    "nomeSpecie": "Dog"
  },
  {
    "nomeAnimale": "Lucy",
    "sesso": "F",
    "data_di_nascita": "2019-05-10",
    "nomeRazza": "Siamese",
    "nomeSpecie": "Cat"
  }
]
```

### Create Animal

**URL**: `/animals`

**Method**: `POST`

This endpoint allows authenticated users to create a new animal associated with their account.

#### Request Parameters

| Parameter         | Type   | Description                    |
|-------------------|--------|--------------------------------

|
| nome_animale      | string | The name of the animal          |
| sesso             | string | The gender of the animal        |
| data_di_nascita   | string | The date of birth of the animal |
| razza             | string | The breed of the animal         |

#### Request Example

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Basic base64(username:password)" -d '{
  "nome_animale": "Max",
  "sesso": "M",
  "data_di_nascita": "2020-01-01",
  "razza": "Labrador Retriever"
}' http://localhost:5000/animals
```

#### Response Example

```
Status: 200 OK
```

### Services

**URL**: `/servizi`

**Method**: `GET`

This endpoint allows authenticated users to retrieve a list of services.

#### Request Example

```bash
curl -X GET -H "Authorization: Basic base64(username:password)" http://localhost:5000/servizi
```

#### Response Example

```
Status: 200 OK

[
  {
    "nomeLuogo": "Pet Clinic",
    "latitudine": "40.7128",
    "longitudine": "-74.0060",
    "nomeTipo": "Veterinary",
    "nomeLocalita": "New York City",
    "provincia": "New York",
    "regione": "New York"
  },
  {
    "nomeLuogo": "Dog Park",
    "latitudine": "34.0522",
    "longitudine": "-118.2437",
    "nomeTipo": "Park",
    "nomeLocalita": "Los Angeles",
    "provincia": "California",
    "regione": "California"
  }
]
```

## Conclusion

This concludes the API usage documentation for the provided Flask application. The endpoints described above allow users to register, log in, manage animals, retrieve services, and log out. Please ensure to include the appropriate authentication headers when making requests to the authenticated endpoints.