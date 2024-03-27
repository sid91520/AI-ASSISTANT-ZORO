import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('feedback')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Execute an SQL query to retrieve data from a table
cursor.execute('SELECT * FROM feedback ')
# cursor.execute("DELETE FROM feedback WHERE email = 'txdfgxcgfxfg';")


# Fetch all rows from the result set
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
