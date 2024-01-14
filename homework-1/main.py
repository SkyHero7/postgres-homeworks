import csv
import psycopg2
from psycopg2 import sql

def execute_sql_query(query, values=None):
    connection = psycopg2.connect(
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
        database="north"
    )

    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    connection.commit()
    connection.close()


# Чтение данных из файла и вставка в таблицу
def create_tables():
    with open("create_tables.sql", "r") as file:
        create_tables_sql = file.read()
        execute_sql_query(create_tables_sql)
def record_exists(table_name, id_column_name, value):
    connection = psycopg2.connect(
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
        database="north"
    )

    cursor = connection.cursor()
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {id_column_name} = %s"

    cursor.execute(query, (value,))
    count = cursor.fetchone()[0]
    connection.close()

    return count > 0
# Функция для вставки данных в таблицу
def insert_data_into_table(table_name, csv_file_path):
    with open(csv_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            columns = ", ".join(row.keys())
            values = ", ".join(["%s"] * len(row))

            id_column_name = f"{table_name[:-1]}_id"  # Assuming that the table name ends with 's' (plural form)
            id_value = row.get(id_column_name)

            if not record_exists(table_name, id_column_name, id_value):
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                execute_sql_query(query, tuple(row.values()))

create_tables()
insert_data_into_table("employees", "north_data/employees_data.csv")
# insert_data_into_table("customers", "north_data/customers_data.csv")
# insert_data_into_table("orders", "north_data/orders_data.csv")
# #
