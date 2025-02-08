# Inventory Management System

The Inventory Management System is a web application built using Django that allows users to manage inventory items, checkouts, maintenance records, and reorder requests. The application provides a user-friendly interface for managing inventory-related tasks and is designed to be used by organizations to keep track of their assets.

## Features

- **User Authentication**: Secure login and logout functionality.
- **Inventory Management**: Add, update, and delete inventory items.
- **Checkouts**: Manage checkouts of inventory items.
- **Maintenance Records**: Track maintenance activities for inventory items.
- **Reorder Requests**: Handle reorder requests for inventory items.
- **Responsive Design**: Built with Bootstrap for a responsive and modern UI.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/inventory-management-system.git
   cd inventory-management-system
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

- **Login**: Use the credentials of the superuser or any other user to log in.
- **Manage Inventory**: Navigate to the Inventory section to add, update, or delete items.
- **Checkouts**: View and manage checkouts from the Checkouts section.
- **Maintenance**: Access maintenance records in the Maintenance section.
- **Reorder**: Handle reorder requests in the Reorder section.

## Project Structure

- `base/`: Contains the main application code including models, views, forms, and templates.
- `templates/`: HTML templates for rendering the UI.
- `static/`: Static files such as CSS and JavaScript.
- `manage.py`: Django's command-line utility for administrative tasks.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- UI powered by [Bootstrap](https://getbootstrap.com/)
