import mysql.connector

host="Localhost"
user="root"
password=""
database="can1"

# Connect to MySQL database
conn = mysql.connector.connect(host=host, user=user, password=password, database=database)

#  key svg
pri = """<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="24" height="20" viewBox="0 0 48 48">
<path fill="#FFA000" d="M30 41L26 45 22 45 18 41 18 21 30 21 30 29 28 31 30 33 30 35 28 37 30 39z"></path><path fill="#FFA000" d="M38,7.8C37.5,6,36,4.7,34.3,4.2C31.9,3.7,28.2,3,24,3s-7.9,0.7-10.3,1.2C12,4.7,10.5,6,10,7.8c-0.5,1.7-1,4.1-1,6.7c0,2.6,0.5,5,1,6.7c0.5,1.8,1.9,3.1,3.7,3.5C16.1,25.3,19.8,26,24,26s7.9-0.7,10.3-1.2c1.8-0.4,3.2-1.8,3.7-3.5c0.5-1.7,1-4.1,1-6.7C39,11.9,38.5,9.5,38,7.8z M29,13H19c-1.1,0-2-0.9-2-2V9c0-0.6,3.1-1,7-1s7,0.4,7,1v2C31,12.1,30.1,13,29,13z"></path><path fill="#D68600" d="M23 26H25V45H23z"></path>
</svg>"""
fk = """<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="24" height="20" viewBox="0 0 48 48">
<path fill="#a2a2a2" d="M30 41L26 45 22 45 18 41 18 21 30 21 30 29 28 31 30 33 30 35 28 37 30 39z"></path><path fill="#a2a2a2" d="M38,7.8C37.5,6,36,4.7,34.3,4.2C31.9,3.7,28.2,3,24,3s-7.9,0.7-10.3,1.2C12,4.7,10.5,6,10,7.8c-0.5,1.7-1,4.1-1,6.7c0,2.6,0.5,5,1,6.7c0.5,1.8,1.9,3.1,3.7,3.5C16.1,25.3,19.8,26,24,26s7.9-0.7,10.3-1.2c1.8-0.4,3.2-1.8,3.7-3.5c0.5-1.7,1-4.1,1-6.7C39,11.9,38.5,9.5,38,7.8z M29,13H19c-1.1,0-2-0.9-2-2V9c0-0.6,3.1-1,7-1s7,0.4,7,1v2C31,12.1,30.1,13,29,13z"></path><path fill="#fff" d="M23 26H25V45H23z"></path>
</svg>"""

# Create cursor
cursor = conn.cursor()

# Query the database schema for table names
cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{database}';")
tables = [table[0] for table in cursor.fetchall()]

# Generate HTML for the schema diagram
html = '<!DOCTYPE html>\n<html>\n<head>\n<title>Schema Diagram</title>\n'
html += '<style>\n'
html += 'table {\nborder-collapse: collapse;\n}\n'
html += 'table, th, td {\nborder: 1px solid black;\npadding: auto;\n}\n'
html += '.grid-container {\nwidth: 80%;\nmargin: 0 auto;\ndisplay: grid;\ngrid-template-columns: auto auto auto;\n gap: 15px;\n}\n'
html += '.grid {\n\n}\n'
html += '</style>\n'
html += '</head>\n<body>\n'
html += f'<p align="center"> {pri} = Primary Key {fk} = Foreign Key </p>\n'
html += '<div class="grid-container">\n'

html += '<table class="grid">\n'
html += '<tr><th>Table</th><th>Primary Key</th></tr>\n'
for table in tables:
    conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()
    cursor.execute(f"SHOW INDEX FROM {table} WHERE Key_name = 'PRIMARY';")
    primary_keys = cursor.fetchall()
    for key in primary_keys:
        html += f'<tr><td>{table}</td><td>{key[4]} {pri}</td></tr>\n'
    cursor.close()
    conn.close()
html += '</table>\n'

# Iterate over tables
for table in tables:
    conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()
    html += '<table class="grid">\n'
    html += f'<tr><th>{table}</th><th>Type</th></tr>\n'
    
    # Query foreign key information for the table
    cursor.execute(f"SELECT column_name FROM information_schema.key_column_usage WHERE table_schema = '{database}' AND table_name = '{table}' AND referenced_table_name IS NOT NULL;")
    foreign_keys = set(fk[0] for fk in cursor.fetchall())
    
    # Query column information for the table
    cursor.execute(f"SHOW COLUMNS FROM {table};")
    columns = cursor.fetchall()
    
    # Flag to indicate if the first column is a foreign key
    first_column_fk = False
    
    # Iterate over columns
    for column in columns:
        column_name = column[0]
        column_type = column[1]
        
        # Check if the column is a primary key
        if column[3] == 'PRI':
            html += f'<tr><td>{pri} {column_name}</td><td>{column_type}</td></tr>\n'
        # Check if the column is a foreign key and it's the first one encountered
        elif column_name in foreign_keys and not first_column_fk:
            html += f'<tr><td>{fk} {column_name}</td><td>{column_type}</td></tr>\n'
            first_column_fk = True
        else:
            html += f'<tr><td>{column_name}</td><td>{column_type}</td></tr>\n'
    
    html += '</table>\n'

# Close cursor and MySQL connection
cursor.close()
conn.close()
html += '<div>\n'
html += '</body>\n</html>'

# Save HTML to a file
with open('schema_diagram.html', 'w') as f:
    f.write(html)
