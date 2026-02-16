import crud

def menu():
    while True:
        print("\n--- Library Management System ---")
        print("1. Add Author")
        print("2. Add Book")
        print("3. Add Member")
        print("4. Borrow a Book")
        print("5. Return a Book")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            name = input("Enter Author Name: ")
            crud.add_author(name)
        elif choice == '2':
            title = input("Enter Book Title: ")
            author_id = input("Enter Author ID: ")
            crud.add_book(title, author_id)
        elif choice == '3':
            name = input("Enter Member Name: ")
            email = input("Enter Member Email: ")
            crud.add_member(name, email)
        elif choice == '4':
            b_id = input("Enter Book ID: ")
            m_id = input("Enter Member ID: ")
            crud.borrow_book(b_id, m_id)
        elif choice == '5':
            b_id = input("Enter Book ID to Return: ")
            crud.return_book(b_id)
        elif choice == '6':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()