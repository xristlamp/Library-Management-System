import csv
import uuid
from user import Librarian, Member, Manager
from book import Book
from datetime import datetime
from collections import defaultdict


class LibrarySystem:
    def __init__(self):
        self.books = []
        self.users = []
        self.current_book_id = 1

    # Add a method to initialize the CSV files if they don't exist
    def initialize_csv_files(self):
        # Check and create empty CSV files if they don't exist
        try:
            with open("library_books.csv", mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Title', 'Author', 'ISBN', 'Category', 'Copies', 'Date Added', 'Status'])
        except FileExistsError:
            pass  # If the file already exists, do nothing

        try:
            with open("users.csv", mode='x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Username', 'Password', 'Role'])
        except FileExistsError:
            pass  # If the file already exists, do nothing

    def add_user(self, user):
        self.users.append(user)

    def save_users_to_csv(self, filename):
        """Save all users to the CSV file."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Username', 'Password', 'Role'])
            for user in self.users:
                writer.writerow([user.id, user.username, user.password, user.__class__.__name__])
        print(f"Users saved to {filename}.")



    def load_users_from_csv(self, filename):
        """Load users from the CSV file."""
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                for row in reader:
                    if len(row) == 0:  # Skip empty rows
                        continue
                    if len(row) < 4:  # Skip rows with insufficient data
                        print(f"Skipping incomplete row: {row}")
                        continue
                    
                    # Load user data from the row
                    user_id, username, password, role = row
                    
                    # Create user based on role
                    if role == 'Librarian':
                        user = Librarian(username, password)
                    elif role == 'Member':
                        user = Member(username, password)
                    elif role == 'Manager':
                        user = Manager(username, password)
                    
                    user.id = user_id if user_id else str(uuid.uuid4())  # Use existing ID or generate a new one
                    self.users.append(user)
            print(f"Users loaded from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found. No users loaded.")

    def add_book(self, book):
            # Assign the next available unique ID
            if self.books:
                # Find the highest ID among existing books and increment it
                self.current_book_id = max(book.id for book in self.books) + 1
            book.id = self.current_book_id
            self.books.append(book)
                    
    def load_books_from_csv(self, filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                for row in reader:
                    if len(row) == 10:  # Έλεγχος αν οι στήλες είναι 10
                        id_, title, author, isbn, category, total_copies, available_copies, date_added, status, borrowed_by_str = row
                        date_borrowed = None  # Αν δεν υπάρχει η 11η στήλη (ημερομηνία δανεισμού)
                    elif len(row) == 11:  # Αν υπάρχουν 11 στήλες (με την ημερομηνία δανεισμού)
                        id_, title, author, isbn, category, total_copies, available_copies, date_added, status, borrowed_by_str, date_borrowed = row
                    else:
                        continue  # Αν οι στήλες είναι λιγότερες ή περισσότερες, παράβλεψε τη γραμμή

                    # Μετατροπή του borrowed_by_str σε λίστα
                    borrowed_by = borrowed_by_str.strip('[]').split(',') if borrowed_by_str else []

                    # Δημιουργία αντικειμένου Book
                    book = Book(title, author, isbn, category, int(total_copies), date_added, status)
                    book.id = int(id_)
                    book.available_copies = int(available_copies)
                    book.borrowed_by = borrowed_by  # Ανάθεση των χρηστών που έχουν δανειστεί το βιβλίο
                    book.date_borrowed = date_borrowed  # Ανάθεση ημερομηνίας δανεισμού
                    self.books.append(book)
                    

            print(f"Books loaded from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found.")

    def save_books_to_csv(self, filename):
        """Save all books to the CSV file."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Author', 'ISBN', 'Category', 'Total Copies', 'Available Copies', 'Date Added', 'Status', 'Borrowed By'])
            for book in self.books:
                borrowed_by_str = ",".join(book.borrowed_by)  # Store user IDs as a comma-separated string
                writer.writerow([book.id, book.title, book.author, book.isbn, book.category, book.total_copies, book.available_copies, book.date_added, book.status, borrowed_by_str,book.date_borrowed])
        print(f"Books saved to {filename}.")

    def borrow_book(self, member, book_id):
        """Borrow one copy of a book by its ID if available copies exist."""
        book = self.find_book_by_id(book_id)
        if book and book.available_copies > 0:
            today_date = datetime.now().strftime("%d-%m-%Y")  # Τρέχουσα ημερομηνία
            book.date_borrowed = today_date  # Καταγραφή ημερομηνίας δανεισμού
            book.available_copies -= 1  # Reduce available copies by 1
            
            # Check if this user already borrowed the book, or append if another user borrows a copy
            if book.borrowed_by is None:
                book.borrowed_by = [member.id]  # Assign the user ID to `borrowed_by`
            else:
                book.borrowed_by.append(member.id)

            if book.available_copies == 0:
                book.status = "Borrowed"
            
            self.save_books_to_csv("library_books.csv")  # Save changes to CSV
            return True
        return False



    def borrow_book_librarian(self, member, book_id):
        """Librarian borrows a book for a member by its ID."""
        book = self.find_book_by_id(book_id)
        if book and book.available_copies > 0:
            today_date = datetime.now().strftime("%d-%m-%Y")  # Current date
            book.date_borrowed = today_date  # Record borrow date
            book.available_copies -= 1  # Decrease available copies

            # Check if the user has already borrowed the book, otherwise add the user to the borrowed_by list
            if book.borrowed_by is None:
                book.borrowed_by = [member.id]  # Add user ID to `borrowed_by`
            else:
                if member.id not in book.borrowed_by:
                    book.borrowed_by.append(member.id)

            if book.available_copies == 0:
                book.status = "Borrowed"  # Mark the book as fully borrowed if no copies are left

            self.save_books_to_csv("library_books.csv")  # Save changes to CSV
            return True
        return False



    def return_book(self, member, book_id):
        """Return one copy of a book and increase the available copies."""
        book = self.find_book_by_id(book_id)
        if book and member.id in book.borrowed_by:
            book.available_copies += 1  # Increase available copies by 1
            book.borrowed_by.remove(member.id)  # Remove the user ID from the borrowed list

            if book.available_copies == book.total_copies:
                book.status = "Available"  # If all copies are returned, mark the book as available

            self.save_books_to_csv("library_books.csv")  # Save changes to CSV
            return True
        return False




    def reserve_book(self, user, book_id):
        for book in self.books:
            if book.id == book_id and book.status == "Available":
                book.status = "Reserved"
                # Μπορείς να καταχωρήσεις και τον χρήστη που έκανε την κράτηση αν χρειάζεται
                book.reserved_by = user.id
                return True
        return False


    def find_book_by_id(self, book_id):
        """Helper method to find a book by its ID."""
        for book in self.books:
            if book.id == book_id:
                return book
        return None


    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None
    
    


    def generate_reports(self):
        total_borrowed = len([book for book in self.books if book.status == "Borrowed"])
        total_reserved = len([book for book in self.books if book.status == "Reserved"])
        return {
            "Total Borrowed Books": total_borrowed,
            "Total Reserved Books": total_reserved,
        }
    
    def save_report_to_csv(self, filename):
        reports = self.generate_reports()
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Report', 'Value'])
            for key, value in reports.items():
                writer.writerow([key, value])
        print(f"Report saved to {filename}.")

    def get_reserved_books(self):
        """Return a list of all reserved books."""
        reserved_books = [book for book in self.books if book.status == "Reserved"]
        return reserved_books
    

    def decline_reserve(self, member, book_id):
        """Cancel a book reservation by its ID."""
        book = self.find_book_by_id(book_id)
        if book and book.status == "Reserved":
            book.available_copies += 1  # Increase available copies
            if book.available_copies > 0:
                book.status = "Available"  # Mark as available if copies are available again
            self.save_books_to_csv("library_books.csv")  # Save changes to CSV
            return True
        return False

    # Μέσα στην κλάση LibrarySystem

    # Αριθμός δανεισμένων βιβλίων από συγκεκριμένο χρήστη
    def borrowed_books_by_user(self, user_id):
        count = 0
        for book in self.books:
            count += book.borrowed_by.count(user_id)
        return count

    # Αριθμός δανεισμένων βιβλίων σε συγκεκριμένη ημέρα
    def borrowed_books_by_date(self, date_str):
        count = 0
        for book in self.books:
            if book.date_borrowed == date_str:  # Χρειαζόμαστε την ημερομηνία δανεισμού
                count += 1
        return count

    # Συνολικός αριθμός δανεισμένων βιβλίων
    def total_borrowed_books(self):
        count = 0
        for book in self.books:
            count += (book.total_copies - book.available_copies)  # Δανεισμένες κόπιες
        return count

    # Συνολικός αριθμός κρατήσεων από συγκεκριμένο χρήστη
    def reserved_books_by_user(self, user_id):
        count = 0
        for book in self.books:
            if book.reserved_by == user_id:
                count += 1
        return count

    # Συνολικός αριθμός βιβλίων που βρίσκονται σε διαδικασία δανεισμού
    def total_books_in_borrow_process(self):
        count = 0
        for book in self.books:
            if book.available_copies < book.total_copies:
                count += 1
        return count



    def export_member_names_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Role'])
            for user in self.users:
                if isinstance(user, Member):  # Εξαγωγή μόνο των μελών
                    writer.writerow([user.username, 'Member'])
        print(f"Member names exported to {filename}.")

    def export_books_borrowed_per_member_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Borrowed Books Count'])
            for user in self.users:
                if isinstance(user, Member):
                    borrowed_books_count = sum(user.id in book.borrowed_by for book in self.books)
                    writer.writerow([user.username, borrowed_books_count])
        print(f"Books borrowed per member exported to {filename}.")

    def export_all_books_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Author', 'ISBN', 'Category', 'Total Copies', 'Available Copies', 'Date Added', 'Status'])
            for book in self.books:
                writer.writerow([book.id, book.title, book.author, book.isbn, book.category, book.total_copies, book.available_copies, book.date_added, book.status])
        print(f"All book entries exported to {filename}.")


    def export_total_borrowed_books_per_day_to_csv(self, filename):
        borrowed_per_day = defaultdict(int)
        
        for book in self.books:
            if book.date_borrowed:
                borrowed_per_day[book.date_borrowed] += 1
        
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Total Borrowed Books'])
            for date, count in borrowed_per_day.items():
                writer.writerow([date, count])
        
        print(f"Total borrowed books per day exported to {filename}.")
