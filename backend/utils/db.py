import mysql.connector


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aadi2k07",  # your MySQL password

        )

        print("Connected to MySQL successfully!")
        return connection

    except Exception as e:
        print("Connection failed:", e)
        return None


def execute_query(query, params=None):
    connection = get_db_connection()

    if connection is None:
        print("Database connection failed.")
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        connection.commit()
        return result

    except Exception as e:
        print("Query execution error:", e)
        return None

    finally:
        cursor.close()
        connection.close()
