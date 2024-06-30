## Endpoints

### 1. Create a Fund

- **URL**: `/funds`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "id": 1,
        "name": "Growth Fund",
        "manager": "Alice Johnson",
        "description": "A fund focusing on long-term growth investments.",
        "nav": 150.25,
        "date": "2021-05-01",
        "performance": 12.5
    }
    ```
- **Success Response**:
    - **Code**: `201 Created`
    - **Content**:
        ```json
        1
        ```
- **Error Response**:
    - **Code**: `400 Bad Request`
    - **Content**:
        ```json
        {
            "error": "<error_message>"
        }
        ```

### 2. Get all Fund

- **URL**: `/funds`
- **Method**: `GET`
- **Success Response**:
    - **Code**: `200 OK`
    - **Content**:
        ```json
        [
            {
                "id": 1,
                "name": "Growth Fund",
                "manager": "Alice Johnson",
                "description": "A fund focusing on long-term growth investments.",
                "nav": 150.25,
                "date": "2021-05-01",
                "performance": 12.5
            }
        ]
        ```

### 3. Get a Fund

- **URL**: `/funds/<int:fund_id>`
- **Method**: `GET`
- **Success Response**:
    - **Code**: `200 OK`
    - **Content**:
        ```json
        {
            "id": 1,
            "name": "Growth Fund",
            "manager": "Alice Johnson",
            "description": "A fund focusing on long-term growth investments.",
            "nav": 150.25,
            "date": "2021-05-01",
            "performance": 12.5
        }
        ```
- **Error Response**:
    - **Code**: `404 Not Found`
    - **Content**:
        ```json
        {
            "error": "<error_message>"
        }
        ```

### 4. Update a Fund

- **URL**: `/funds/<int:fund_id>`
- **Method**: `PATCH`
- **Request Body**:
    ```json
    {
        "performance": 30.5
    }
    ```
- **Success Response**:
    - **Code**: `200 OK`
    - **Content**:
        ```json
        {
            "id": 1,
            "name": "Updated Growth Fund",
            "manager": "Alice Johnson",
            "description": "A fund focusing on long-term growth investments.",
            "nav": 150.25,
            "date": "2021-05-01",
            "performance": 30.5
        }
        ```
- **Error Response**:
    - **Code**: `404 Not Found`
    - **Content**:
        ```json
        {
            "error": "<error_message>"
        }
        ```

    - **Code**: `400 Bad Request`
    - **Content**:
        ```json
        {
            "error": "<error_message>"
        }
        ```

### 5. Delete a Fund

- **URL**: `/funds/<int:fund_id>`
- **Method**: `DELETE`
- **Success Response**:
    - **Code**: `204 No Content`
    - **Content**: `None`
- **Error Response**:
    - **Code**: `404 Not Found`
    - **Content**:
        ```json
        {
            "error": "<error_message>"
        }
        ```

## Example Requests

### Create a Fund

```bash
curl -X POST http://localhost:5000/funds -H "Content-Type: application/json" -d '{
    "id": 1,
    "name": "Growth Fund",
    "manager": "Alice Johnson",
    "description": "A fund focusing on long-term growth investments.",
    "nav": 150.25,
    "date": "2021-05-01",
    "performance": 12.5
}'
```

### Update a Fund

```bash
curl -X PATCH http://localhost:5000/funds/1 -H "Content-Type: application/json" -d '{"performance": 12.5}'
```

### Get a Fund

```bash
curl -X GET http://localhost:5000/funds/1
```

### Get all Fund

```bash
curl -X GET http://localhost:5000/funds
```

### Delete a Fund

```bash
curl -X DELETE http://localhost:5000/funds/1
```


## SQL Schema

### Table: funds

#### Columns

- id (INT Primary Key)
- name (VARCHAR(255))
- manager_name (VARCHAR(255))
- description (TEXT)
- nav (DOUBLE)
- date (DATE)
- performance (DOUBLE)


## Usage

In the project's root directory, execute the following steps.

### 1. Create virtual environment and install project dependencies

```bash
> python -m venv venv
> venv\scripts\activate
> pip install -r requirements.txt
```

### 2. Start the flask server

```bash
> flask --app funds_api run
```

### 3. Create MySQL schema

```bash
> flask --app funds_api create-schema --user <user> --password <password>
```


### 4. Migrate data to MySQL schema

```bash
> flask --app funds_api migrate-database --user <user> --password <password>
```


### 5. Run the follow for flask app help

```bash
> flask --app funds_api --help
```
