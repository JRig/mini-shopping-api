# Shopping API

A part of a mini shopping app.

## Installation

### Windows

Python 3.8+ must be installed.

Navigate to project folder in CLI, and use

> pip install -r requirements.txt

Run the service by typing

> python app.py

### Docker

Build the project using

> docker build -t [tagname] .

Run the service using

> docker run -p 5000:[port] [tagname]

where [port] could be 5000. In that case, the service will be available on //localhost:5000

## Models

### Product

```yaml
[*] title: str
    description: str
[*] price: int
    currency: str
```

### Cart

```yaml
[*] orders: [Order]
    total: float
```

### Order

```yaml
    amount: int
[*] product_id: int
```

**: required*

## Endpoints

### Create product

> POST /product

Input:

`Product`

Example:

```json
{
    "title": "Computeractic",
    "description": "didactic",
    "price": "17",
    "currency": "USD"
}
```

Response:

> 200 OK

```yaml
product_id: int
```

### Get product

> GET /product/:id

Parameters

```yaml
id: int
```

Response:

```yaml
product_id: int
title: str
description: str
price: float
currency: str
stock: int
```

### Get all products

> GET /product

Response:

> 200 OK

```yaml
products: [Product]
```

### Delete product

> DELETE /product/:id

Parameters

```yaml
id: int
```

### Create Cart

> POST /cart

Input:

`Cart`

Response:

> 200 OK

```yaml
cart_id: int
total: float
```

### Get Cart

> GET /cart/:id

Parameters

```yaml
id: int
```

### Add Order to Cart

> POST /cart/:id/add

    Rules:
    - Every fifth item free
    - Maximum 100 usd total
    - Discount of 1 usd above 20

    Rule violation results in Error (see Error_msg for details).

Parameters

```yaml
id: int
```

Input:

`Order`

Results:

> 204 OK

    [No Body]

> 400 Error

```json
{"Error": Error_msg}
```

### Get Orders per Cart

> POST /cart/:id/orders

Parameters

```yaml
id: int
```
