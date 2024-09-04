import mysql.connector
from entities.error import ErrorMessage

def add_records(records) -> str:
    """
    Add heart rate records to MySQL database.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='heart'
    )
    cursor = connection.cursor()
    error_message = ""
    try:
        for record in records:
            time = record.get('time')
            heart_rate = record.get('heartRate')
            query = "INSERT INTO heart_rates (time, heart_rate) VALUES (%s, %s)"
            cursor.execute(query, (time, heart_rate))

        connection.commit()
    except mysql.connector.Error as err:
        error_message = err
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
        return error_message

"""def get_records():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='heart'
    )
    cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for JSON-like output
    error_message = ""
    try:
        query = "SELECT * FROM heart_rates"
        cursor.execute(query)

        records = cursor.fetchall()  # Fetch all rows from the executed query
        return records
    except mysql.connector.Error as err:
        error_message = err
        raise
    finally:
        cursor.close()
        connection.close()
        return error_message"""
