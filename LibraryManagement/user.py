import uuid  #παραγει μοναδικα id 
# user.py
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.id = str(uuid.uuid4())  # Generate a unique ID for each user

class Librarian(User):
    def __init__(self, username, password):
        super().__init__(username, password)
    
    def add_book(self, library_system, book):
        library_system.add_book(book)
    
    def check_reservations(self, library_system):
        return library_system.get_reserved_books()


class Member(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def borrow_book(self, library_system, book_id):
        """Borrow a book by its ID (legacy)."""
        return library_system.borrow_book(self, book_id)


    def borrow_book_by_title(self, library_system, title):
        """Borrow a book by its title."""
        for book in library_system.books:
            # DEBUG: Check if the correct book is retrieved
            print(f"DEBUG: Checking book '{book.title}' with {book.available_copies} available copies.")
            if book.title == title:
                print(f"DEBUG: Attempting to borrow '{book.title}' with {book.available_copies} available copies.")
                if book.available_copies > 0:  # Ensure there are available copies
                    return library_system.borrow_book(self, book.id)
                else:
                    print(f"DEBUG: No available copies for '{book.title}'.")
        return False

    
    def return_book(self, library_system, book_id):
        """Return a book by its ID (legacy)."""
        return library_system.return_book(self, book_id)


    def return_book_by_title(self, library_system, title):
            """Return a book by its title."""
            for book in library_system.books:
                if book.title == title and book.available_copies < book.total_copies:
                    return library_system.return_book(self, book.id)
            return False

    
    def reserve_book(self, library_system, book_id):
        """Reserve a book by its ID (legacy)."""
        return library_system.reserve_book(self, book_id)

    def reserve_book_by_title(self, library_system, title):
        """Reserve a book by its title."""
        # Find the book with the given title
        for book in library_system.books:
            if book.title == title and book.status == "Available":
                return library_system.reserve_book(self, book.id)
        return False  # If no book is found or if the book is not available
    def decline_reserve_by_title(self, library_system, title):
        """Decline a reserved book by its title."""
        for book in library_system.books:
            if book.title == title and book.status == "Reserved":
                return library_system.decline_reserve(self, book.id)
        return False

class Manager(User):
    def __init__(self, username, password):
        super().__init__(username, password)
    
    def view_reports(self, library_system):
        return library_system.generate_reports()
