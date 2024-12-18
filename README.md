# Account-transfer-task

This is a Django-based web application for a basic banking system that allows users to upload account data via CSV, view account details, and perform transactions between accounts.

## Features

- **Upload CSV Files**: Allows uploading account data in CSV format.
  ![Upload CSV Form](images/upload.png)
- **View Accounts**: Displays a list of all accounts.
  ![View Accounts](images/accounts.png)
- **Perform Transactions**: Enables transferring funds between accounts.
  ![Perform Transactions](images/transaction.png)


## Requirements

- Python 3.10
- Django 5.0.6
- PostgreSQL 13
- Docker

## Project Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.10
- Docker
- Docker Compose

### Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/shahdhesham5/Account-transfer-task.git
    cd Account trans
    ```

2. **Create a `.env` file**:

    Create a `.env` file in the project root directory with the following content:

    ```env
    POSTGRES_DB=postgresdb
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=1234
    ```

3. **Build and run the Docker containers**:

    ```sh
    docker-compose up --build
    ```

4. **Create a superuser**:

    ```sh
    docker-compose exec django_sessionsbank_backend_web python manage.py createsuperuser
    ```

5. **Run the development server**:

    The development server should already be running from the `docker-compose up` command. You can access it at `http://localhost:8000`.

## Usage

### Uploading CSV Files

1. Go to the home page.
2. Use the upload form to select and upload a CSV file containing account data.
3. The file should have columns: Identifier, Name, Balance.

### Viewing Accounts

1. Navigate to the "Accounts" page.
2. All uploaded accounts will be displayed in a table format.

### Performing Transactions

1. Go to the "Transactions" page.
2. Select the source account and the destination account from the dropdown menus.
3. Enter the amount to be transferred and submit the form.

## Running Tests

The project uses `pytest` and `pytest-django` for testing.

1. **Install testing dependencies**:

    ```sh
    pip install pytest pytest-django
    ```

2. **Run tests**:

    ```sh
    docker-compose exec -it django_sessionsbank_backend_web pytest
    ```

