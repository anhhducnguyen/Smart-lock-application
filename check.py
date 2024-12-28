import mysql.connector
from mysql.connector import Error

def check_rds_connection():
    try:
        # Kết nối đến MySQL RDS
        connection = mysql.connector.connect(
            host='students.cfi6ykkacnb2.us-east-1.rds.amazonaws.com',
            user='nodeapp',
            password='student12',
            database='STUDENTS'
        )

        if connection.is_connected():
            # Lấy thông tin server
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL RDS: {db_info}")
            
            # Lấy tên cơ sở dữ liệu hiện tại
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record}")
            
            # Lấy cấu trúc bảng 'students'
            cursor.execute("DESCRIBE students;")
            columns = cursor.fetchall()
            print("\nTable structure for 'students' table:")
            
            # In ra header của bảng
            print("+----------------+-------------------+")
            print("| Column Name    | Data Type         |")
            print("+----------------+-------------------+")
            
            # In ra thông tin cấu trúc bảng
            for column in columns:
                column_name = column[0]
                data_type = column[1].decode() if isinstance(column[1], bytes) else column[1]
                print(f"| {column_name:<14} | {data_type:<17} |")
            
            print("+----------------+-------------------+")
            
            # Lấy dữ liệu từ bảng 'students'
            cursor.execute("SELECT * FROM students;")
            rows = cursor.fetchall()
            
            # In ra dữ liệu
            print("\nData from 'students' table:")
            print("+----+------------------+-------------+-----------+-----------+---------------------------+------------+")
            print("| id | name             | address     | city      | state     | email                     | phone      |")
            print("+----+------------------+-------------+-----------+-----------+---------------------------+------------+")
            
            for row in rows:
                print(f"| {row[0]:<2} | {row[1]:<16} | {row[2]:<11} | {row[3]:<9} | {row[4]:<9} | {row[5]:<25} | {row[6]:<10} |")
            
            print("+----+------------------+-------------+-----------+-----------+---------------------------+------------+")

    except Error as e:
        print(f"Connection error: {e}")
    
    finally:
        # Đóng kết nối
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection to MySQL closed.")

check_rds_connection()