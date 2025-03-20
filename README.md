# Todo List + CRUD with PyQt5 and <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/SQLite370.svg/1200px-SQLite370.svg.png" alt="SQLite" width="90">

Graphical interface in Python using the PyQt5 library to build a todo list with CRUD operations (Create, Read, Update, Delete). In addition to allowing the user to add, view, edit, and remove tasks, the application has an integrated database using Python's sqlite3 library.

> Project Status: ✔️ (completed)

## 🔧 Technologies Used
Python V.: 3.11.1 || PyQt5 V.: 5.15.9

## ⚙️ Setting Up the Virtual Environment
* In your terminal, navigate to the project's root folder and run the following command to create a virtual environment:

  ```bash
  python -m venv name_of_virtualenv
  ```

* Run the command according to your system to activate your virtual environment:

  Windows
  ```bash
  .\name_of_virtualenv\Scripts\activate
  ```

  Linux or macOS
  ```bash
  source name_of_virtualenv/bin/activate
  ``` 

## 🧑‍🔬 Installing Dependencies
* With the virtual environment **activated**, install the project dependencies with the following command:

  ```bash
  pip install -r requirements.txt
  ```

## 🚀 Running the Project
* Run the main file from the list as follows:

  ```bash
  python main.py
  ```

## 🗄️ About the Database
* Just add a task in the application and a <code>tasks.db</code> database is automatically generated with the tasks included in it.

  **Note:** For each change in the application, remember to update the file by closing and reopening it. If you are using a database manager, just press F5 to refresh it.
