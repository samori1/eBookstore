import sqlite3

db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            quantity INTEGER
               )
               ''')

cursor.execute('SELECT COUNT(*) FROM book')
if cursor.fetchone()[0] == 0:
    books = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
        (3003, 'The Lion the Witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]
    cursor.executemany('''
                       INSERT INTO book (id, title, author, quantity)
                       VALUES (?, ?, ?, ?)
                       ''', books)
    db.commit()


def add_book():
    ''' 
    Function to add a new book record to the database.
    Asks the user to complete the ID, title, author and quantity fields of a
    new book, then creates a record of it in the database.
    '''
    try:
        id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        quantity = int(input("Enter book quantity: "))
        cursor.execute('''
        INSERT INTO book (id, title, author, quantity)
        VALUES (?, ?, ?, ?)
        ''', (id, title, author, quantity))
        db.commit()
        print(f"Book '{title}' added successfully\n")
    except:
        print("Error: Book already exists\n")


def update_book():
    '''
    Function to update the record of a book within the database.
    Allows the user to update information for an existing book via its ID.
    '''
    try:
        id = int(input("Enter book ID to update: "))
        cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
        book = cursor.fetchone()

        if book:
            print(f"Current details: ID={book[0]}, Title='{book[1]}',\
                  Author='{book[2]}', Quantity={book[3]}")
            title = input("Enter new title (leave blank to keep current): ")\
                or book[1]
            author = input("Enter new author (leave blank to keep current): ")\
                or book[2]
            quantity = input('Enter new quantity (leave blank to keep\
                             current): ') or book[3]

            cursor.execute('''
                           UPDATE book SET title = ?, author = ?, quantity = ?\
                           WHERE id = ?
                           ''', (title, author, quantity, id))
            db.commit()
            print(f"Book with ID {id} updated successfully\n")
        else:
            print(f"Book with ID {id} not found\n")
    except ValueError:
        print("Invalid input\n")


def delete_book():
    '''
    Function to delete a book from the database.
    Asks the user to input a book ID and deletes the corresponding book from 
    the database.
    '''
    try:
        id = int(input("Enter book ID to delete: "))
        cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
        book = cursor.fetchone()

        if book:
            cursor.execute("DELETE FROM book WHERE id = ?", (id,))
            db.commit()
            print(f"Book with ID {id} deleted successfully\n")
        else:
            print(f"Book with ID {id} not found\n")
    except ValueError:
        print("Invalid input\n")


def search_books():
    '''
    Function to create a search engine for books within the database via the
    title and author fields.
    Asks the user to input a search term (title or author) and
    locates the corresponding books.

    '''
    search_term = input("Enter title or author to search for: ")
    cursor.execute('''
                   SELECT * FROM book WHERE title LIKE ? OR author LIKE ?''',
                   (f'%{search_term}%', f'%{search_term}%'))
    results = cursor.fetchall()

    if results:
        print("Search results:")
        for book in results:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]},\
                  Quantity: {book[3]}")
            print()
    else:
        print("No books found matching the search criteria\n")


def menu():
    '''
    Function to display a menu to the user and executes the selected function.
    The main menu is in a while loop until the user chooses the exit function.
    '''
    while True:
        print("Please select from the following options")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_books()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid input\n")

menu()

db.close()