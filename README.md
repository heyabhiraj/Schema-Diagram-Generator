# Schema-Diagram-Generator
The SQL Diagram Generator is a Python script that generates HTML-based schema diagrams for MySQL databases. It connects to a MySQL database, retrieves schema information, and creates an HTML file representing the database schema with tables and their columns. Primary keys are marked with yellow key, and the first column that is referenced as a foreign key is marked with gray key'.

### Features
- Connects to a MySQL database and retrieves schema information.
- Generates an HTML-based schema diagram with tables and columns.
- Marks primary keys with yellow and foreign key columns with gray keys.
- Simple and easy-to-use.

## Requirements

- Python 3.x
- MySQL connector for Python

## Usage

1. Install the required Python packages using pip:
2. Modify the script to provide your MySQL database connection details:

```python
host = "your_host"
user = "your_username"
password = "your_password"
database = "your_database"
```

```bash
pip install req.txt
```
OR
```bash
pip install mysql-connector-python 
```

```bash
python schema.py
```
## OUTPUT
![alt text](https://github.com/heyabhiraj/Schema-Diagram-Generator/blob/main/schema-diagram.png)
