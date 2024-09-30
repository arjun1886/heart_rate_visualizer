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
            timestamp = record.get('timestamp')
            heart_rate = float(record.get('heart_rate'))
            query = "INSERT INTO heart_rate (timestamp, heart_rate) VALUES (%s, %s) ON DUPLICATE KEY UPDATE heart_rate = VALUES(heart_rate);"
            cursor.execute(query, (timestamp, heart_rate))
    except mysql.connector.Error as err:
        error_message = err
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.commit()
        connection.close()
        return error_message