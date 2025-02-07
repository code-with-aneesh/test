# Flask To-Do App

This is a simple Flask web application that allows users to register, log in, and manage a to-do list. The application uses MongoDB Atlas for data storage and supports both dark and light themes.

## Features

- User registration and login
- Add, toggle, and delete to-do items
- Dark and light theme toggle
- Responsive design using Bootstrap and Tailwind CSS

## Prerequisites

- Python 3.x
- Flask
- MongoDB Atlas
- Web browser

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/code-with-aneesh/test.git
    cd test
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your MongoDB Atlas connection:
    - Create a `.env` file in the root directory of the project.
    - Add your MongoDB URI and secret key to the `.env` file:
        ```env
        MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority
        SECRET_KEY=your_secret_key
        ```

5. Run the Flask application:
    ```sh
    flask run
    ```

6. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

- **Register**: Create a new account by providing a username and password.
- **Login**: Log in with your registered username and password.
- **Dashboard**: Manage your to-do list by adding, toggling, and deleting items.
- **Theme Toggle**: Switch between dark and light themes using the toggle button.

## Project Structure
