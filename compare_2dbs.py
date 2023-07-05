import hashlib
import csv
import pymysql
import pymssql

# Function to generate hash for data
def generate_hash(data):
    return hashlib.sha256(str(data).encode()).hexdigest()

# Read the CSV file
def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    return rows

# Connect to the first database
# MSSQL connection details
mssql_host = ''
mssql_user = ''
mssql_password = ''
mssql_database = ''

# Connect to MSSQL
connection1 = pymssql.connect(host=mssql_host, user=mssql_user, password=mssql_password, database=mssql_database)

# MySQL connection details
mysql_host = ''
mysql_user = ''
mysql_password = ''
mysql_database = ''

# Connect to MySQL
connection2 = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)

table_info = "C:\\Users\\krito\\Desktop\\tables.csv"

with open(table_info, 'r') as file:
    reader = csv.reader(file)
    # next(reader)  # This would skip the header row
    # Iterate over each row in the CSV file
    for row in reader:
        table = table_info[0]
        columns = table_info[1]
        print(f"Checking: {table} Coumn: {columns}")
        # Perform the update in MySQL
        with connection1.cursor() as cursor:
            sql = f"SELECT {columns} FROM {table}"
            cursor.execute(sql)
            data1 = cursor.fetchall()
        with connection2.cursor() as cursor:
            sql = f"SELECT {columns} FROM {table}"
            cursor.execute(sql)
            data2 = cursor.fetchall()
    
    # Generate hashes for the data
    hash1 = generate_hash(data1)
    hash2 = generate_hash(data2)

    # Compare the hashes
    if hash1 == hash2:
        print(f"Data from {table} is identical.")
    else:
        print(f"Data from {table} is different.")
# Close the MySQL connection
connection1.close()
connection2.close()