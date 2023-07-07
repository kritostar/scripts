import csv
import pymysql
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--table_name", help = "table name to update", required=True)
parser.add_argument("-f", "--field_name", help = "field name within table to update", required=True)
args = parser.parse_args()
# if not really necessary as this is a required parameter
if args.table_name:
    print(f"Updating table: {args.table_name}")
    table_name = args.table_name
if args.table_name:
    print(f"Updating field name: {args.field_name}")
    field_name = args.field_name
# MySQL connection information
host = ''
user = ''
password = ''
database = ''
csv_file = "C:\\Users\\krito\\Desktop\\scripts\\remitModificationDate.csv"
connection = pymysql.connect(host=host, user=user, password=password, database=database)
# Open the CSV file and read the ID/value pairs
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    # next(reader)  # This would skip the header row
    # Iterate over each row in the CSV file
    count=0
    for row in reader:
        id_value = row[0]  # Assuming the ID is in the first column
        value = row[1]  # Assuming the value is in the second column
        print(f"Updating id: {id_value} value: {value}")
        # Perform the update in MySQL
        with connection.cursor() as cursor:
            sql = f"UPDATE {table_name} SET {field_name} = %s WHERE id = %s"
            cursor.execute(sql, (value, id_value))
        # Commit the changes
        count=count+1
        connection.commit()
print(f"Records updates: {count}")
# Close the MySQL connection
connection.close()