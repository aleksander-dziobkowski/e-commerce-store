=======
# 🛍️ E-commerce Django Project

A complete online store project built with **Python**,**Django**, **Django REST Framework** i **PostgreSQL**, featuring **PayU** payment integration.

---

## 🚀 Functions

- 🧩 Store module (products, cart, orders)
- 👤 User system (registration, login)
- 💳 PayU integration (sandbox)
- 🗂️ Django admin panel
- ⚙️ REST API (Django REST Framework)

---

## 🛠️ Installation and Local Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/aleksander-dziobkowski/e-commerce-store.git
cd your_repo
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create a PostgreSQL database
Using pgAdmin 4 or PostgreSQL shell:
CREATE DATABASE ecommerce_db;
Make sure you have a PostgreSQL user (e.g. postgres) with access to this database.

### 5️⃣ Copy and edit the .env file
Copy the example environment file:
```bash
cp .env.example .env
```
Then fill it with your local configuration

### 6️⃣ Apply migrations
python manage.py migrate

### 7️⃣ (Optional) Create a superuser
python manage.py createsuperuser

### 8️⃣ Run the local development server
python manage.py runserver

Your project will be available at:
👉 http://127.0.0.1:8000/

Now you can add and modify Main Categories, Categories, Products by admin panel:
👉 http://127.0.0.1:8000/admin

🧾 License
This project is released under the MIT License — feel free to use and modify it for learning or personal projects.
