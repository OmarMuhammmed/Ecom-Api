

# Ecom-Api

Ecom-Api is an eCommerce API built using Django. This project aims to provide an API interface for managing products, orders, and users in an eCommerce application.

## Requirements

- Python 3.8 or higher
- Django 3.2 or higher
- Django REST framework 3.12 or higher

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/OmarMuhammmed/Ecom-Api.git
   cd Ecom-Api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

5. **Run the local server:**
   ```bash
   python manage.py runserver
   ```

   You can now access the API at [http://localhost:8000/](http://localhost:8000/).


## Usage

Api Docs with Postman ==> https://documenter.getpostman.com/view/35038234/2sA3kdAxTG#94f521f6-dd69-4b6b-9c39-d97d7654542f

## License

This project is licensed under the [MIT License](LICENSE).
