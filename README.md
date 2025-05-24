# Donation Management System

A Flask web application for managing donations, NGOs, users, and pickup requests, with MySQL as the backend.

## Features
- User registration and login (Donor, Volunteer, Admin, NGO)
- NGO registration and dashboard
- Make donations (money or goods)
- Request pickups for donations
- Admin management of users, NGOs, and donations
- Responsive Bootstrap UI

## Requirements
- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd donation
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Database
- **First, create the database in MySQL (this is not automatic):**
  ```sql
  CREATE DATABASE donation_system;
  ```
- Update `app/config.py` with your MySQL username, password, and database name:
  ```python
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@localhost/<database>'
  ```

### 5. Initialize the Database
- The app will automatically create all tables on first run using `db.create_all()`.
- If you want to use migrations, set up Flask-Migrate (optional, see below).

### 6. Run the Application
```bash
flask run
```
- Visit [http://localhost:5000](http://localhost:5000) in your browser.

## Database Schema
- All tables and columns are created automatically from the models in `app/models.py`.
- The `pickup_requests` table now includes an `ngo_id` foreign key for proper linkage.

## Default Roles
- `donor`, `volunteer`, `admin`, `ngo`
- Admin users must be created manually in the database or via the admin interface.

## Notes
- If you get MySQL errors about safe updates, see the README troubleshooting section or disable safe updates in your MySQL client.
- For first-time setup, make sure your MySQL user has privileges to create tables and foreign keys.

## Troubleshooting
- **TemplateNotFound**: Ensure all templates are in the correct folders (`auth/`, `user/`, `ngo/`, `donations/`, etc.).
- **ENUM errors**: Make sure your `users.role` column includes all roles (`donor`, `volunteer`, `admin`, `ngo`).
- **Foreign key errors**: When adding new columns, update existing rows to valid values before adding NOT NULL or foreign key constraints.

## License
MIT 
