import mysql.connector

def get_connection():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'priyaddharshan',
        'database': 'LibraryDB'   # ✅ ADD THIS
    }
    return mysql.connector.connect(**config)


def init_db():
    db = get_connection()
    cursor = db.cursor() # executes sql command and fetch result

    cursor.execute("CREATE DATABASE IF NOT EXISTS LibraryDB")

    #Author ID
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            author_id INT AUTO_INCREMENT PRIMARY KEY,
            author_name VARCHAR(255) NOT NULL
        )
    ''')

    #Book table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INT,
            status VARCHAR(50) DEFAULT 'Available',
            FOREIGN KEY (author_id) REFERENCES Authors(author_id)
        )
    ''')

    #Member Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Members (
            member_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE
        )
    ''')

    # 5. Loans Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Loans (
            loan_id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT,
            member_id INT,
            loan_date DATE,
            due_date DATE,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES Books(book_id),
            FOREIGN KEY (member_id) REFERENCES Members(member_id)
        )
    ''')

    print("Step 1 Complete: LibraryDB and Tables are initialized.")
    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    init_db()
    