from database import get_connection
from datetime import datetime, timedelta

def add_author(name):
    try:
        db = get_connection()
        cursor = db.cursor()

        sql = "INSERT INTO Authors (author_name) VALUES (%s)"
        cursor.execute(sql, (name,))

        db.commit()
        print(f"Author '{name}' added successfully!")

    except Exception as e:
        print(f"Error adding author: {e}")

    finally:
        cursor.close()
        db.close()

def add_book(title, author_id):
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("USE LibraryDB")

        # We set status to 'Available' by default in the DB, 
        # so we only need title and author_id here.
        sql = "INSERT INTO Books (title, author_id) VALUES (%s, %s)"
        cursor.execute(sql, (title, author_id))
        
        db.commit()
        print(f"Book '{title}' added successfully!")
    except Exception as e:
        print(f"Error adding book: {e}")
   
    finally:
        cursor.close()
        db.close()


def add_member(name, email):
    try:
        db = get_connection()
        cursor = db.cursor()

        sql = "INSERT INTO Members (name, email) VALUES (%s, %s)"
        cursor.execute(sql, (name, email))

        db.commit()
        print(f"Member '{name}' added successfully!")

    except Exception as e:
        print(f"Error adding member: {e}")

    finally:
        cursor.close()
        db.close()


def borrow_book(book_id, member_id):
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("USE LibraryDB")

        
        # Check if the member exists
        cursor.execute("SELECT name FROM Members WHERE member_id = %s", (member_id,))
        member = cursor.fetchone()

        if not member:
            print(f"\n[!] Acknowledgment: Member ID {member_id} is not registered in our system.")
            print("Please register as a member (Option 3) before borrowing books.")
            return # This stops the function right here

        # Check if the book exists and is available
        cursor.execute("SELECT title, status FROM Books WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()

        if not book:
            print(f"\n[!] Error: Book ID {book_id} does not exist in the library.")
            return
        
        if book[1] == 'Borrowed':
            print(f"\n[!] Sorry: '{book[0]}' is already borrowed by someone else.")
            return

        # 1. Calculate Dates
        loan_date = datetime.now().date()
        due_date = loan_date + timedelta(days=7) # Book is due in 1 week

        # 2. Create the Loan Record
        loan_sql = """
            INSERT INTO Loans (book_id, member_id, loan_date, due_date) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(loan_sql, (book_id, member_id, loan_date, due_date))

        # 3. Update the Book Status
        update_sql = "UPDATE Books SET status = 'Borrowed' WHERE book_id = %s"
        cursor.execute(update_sql, (book_id,))

        db.commit()
        print(f"Book {book_id} successfully borrowed by Member {member_id}.")
        print(f"Please return by: {due_date}")

    except Exception as e:
        print(f"Transaction failed: {e}")
    finally:
        cursor.close()
        db.close()

def return_book(book_id):
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("USE LibraryDB")

        # 1. Find the due date for this book (from the active loan)
        # We look for the row where return_date is still NULL
        cursor.execute("""
            SELECT loan_id, due_date FROM Loans 
            WHERE book_id = %s AND return_date IS NULL
        """, (book_id,))
        
        result = cursor.fetchone()

        if result:
            loan_id, due_date = result
            return_date = datetime.now().date()
            
            # 2. Calculate Late Fee (₹10 per day)
            fine = 0
            if return_date > due_date:
                days_late = (return_date - due_date).days
                fine = days_late * 10
                print(f"Book is {days_late} days late. Fine: ₹{fine}")
            else:
                print("Book returned on time. No fine.")

            # 3. Update Loans table with return date
            cursor.execute("""
                UPDATE Loans SET return_date = %s 
                WHERE loan_id = %s
            """, (return_date, loan_id))

            # 4. Make the book 'Available' again
            cursor.execute("UPDATE Books SET status = 'Available' WHERE book_id = %s", (book_id,))

            db.commit()
            print(f"Book {book_id} returned successfully.")
        else:
            print("Error: No active loan found for this book ID.")

    except Exception as e:
        print(f"Return failed: {e}")

    finally:
        cursor.close()
        db.close()