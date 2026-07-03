# Utensils Store Backend API

A RESTful backend API for an online utensils store built with **Flask** and **MySQL**. The application provides user authentication, product management, customer reviews, an admin dashboard, and M-Pesa payment integration.

---

## Features

### User Management

* User registration
* User login
* Password reset
* Profile update

### Product Management

* Add new products with images
* Retrieve all products
* Delete products (Admin only)

### Customer Reviews

* Add product reviews
* View all reviews
* Delete reviews (User/Admin)

### Admin Dashboard

* View all users
* View all products
* View all customer orders
* View all reviews

### Payment Integration

* M-Pesa STK Push payment using Safaricom Sandbox

---

## Technologies Used

* Python
* Flask
* MySQL
* PyMySQL
* Flask-CORS
* Plotly (Frontend visualization support)
* Safaricom M-Pesa Daraja API

---

## Project Structure

```
project/
│
├── app.py
├── static/
│   └── images/
├── requirements.txt
└── README.md
```

---

## Database

Database Name

```
utensils
```

Main Tables

* users
* products
* reviews
* orders

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/utensils-backend.git

cd utensils-backend
```

---

### 2. Create a virtual environment

Windows

```bash
python -m venv venv
```

Activate it

```bash
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure MySQL

Create a MySQL database called

```
utensils
```

Update the connection details in

```python
get_db()
```

with your own

* Host
* Username
* Password
* Port

---

### 5. Run the application

```bash
python app.py
```

The server starts on

```
http://127.0.0.1:5000/
```

---

# API Endpoints

## Authentication

| Method | Endpoint        | Description     |
| ------ | --------------- | --------------- |
| POST   | /signup         | Register a user |
| POST   | /login          | User login      |
| POST   | /reset_password | Reset password  |
| POST   | /update_profile | Update profile  |

---

## Products

| Method | Endpoint                     | Description                   |
| ------ | ---------------------------- | ----------------------------- |
| POST   | /add_products                | Add a new product             |
| GET    | /get_products                | Retrieve all products         |
| POST   | /delete_product/<product_id> | Delete a product (Admin only) |

---

## Reviews

| Method | Endpoint                   | Description          |
| ------ | -------------------------- | -------------------- |
| POST   | /add_review                | Add a review         |
| GET    | /get_reviews               | Retrieve all reviews |
| POST   | /delete_review/<review_id> | Delete a review      |

---

## Admin

| Method | Endpoint         | Description                   |
| ------ | ---------------- | ----------------------------- |
| POST   | /admin-dashboard | Retrieve admin dashboard data |

---

## Payments

| Method | Endpoint       | Description                      |
| ------ | -------------- | -------------------------------- |
| POST   | /mpesa_payment | Initiate M-Pesa STK Push payment |

---

# Image Uploads

Uploaded product images are stored inside

```
static/images/
```

---

# Security Notes

Current implementation is intended for educational purposes.

Future improvements include:

* Password hashing using bcrypt
* JWT authentication
* Environment variables for API keys and database credentials
* Input validation
* Rate limiting
* Better exception handling

---

# Future Improvements

* Shopping cart
* Order tracking
* Wishlist
* Product search
* Product categories
* Inventory management
* Email verification
* Password reset via email
* Docker deployment
* Cloud deployment (Render, Railway, AWS)

---

# Author

Christine Mwaniki

Full Stack Software Development Student

---

# License

This project is licensed under the MIT License.

Feel free to modify and use it for learning purposes.
