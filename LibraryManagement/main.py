import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from library_system import LibrarySystem
from book import Book
from user import Librarian, Member, Manager

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library System")
        self.root.geometry("800x600")

        # Load the background image
        self.bg_image = Image.open("photo.jpg")
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize image to fit window
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set background label
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Create LibrarySystem object
        self.library_system = LibrarySystem()
        # Load existing books and users from CSV (if available)
        self.library_system.load_books_from_csv("library_books.csv")
        self.library_system.load_users_from_csv("users.csv")

        # Main Menu
        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()


        # Set background label again because widgets destroy the image label
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text="Welcome to the Library System", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Login", command=self.login_screen).pack(pady=5)
        tk.Button(self.root, text="Create Account", command=self.create_account_screen).pack(pady=5)

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show='*')
        password_entry.pack()

        def login_action():
            username = username_entry.get()
            password = password_entry.get()
            user = self.library_system.login(username, password)

            if user:
                self.current_user = user  # Αποθήκευση του τρέχοντα χρήστη
                messagebox.showinfo("Login Success", f"Welcome, {user.username}!")
                self.user_menu(user)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

        tk.Button(self.root, text="Login", command=login_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    def create_account_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        tk.Label(self.root, text="Create Account", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show='*')
        password_entry.pack()

        tk.Label(self.root, text="Role (1: Librarian, 2: Member, 3: Manager)").pack()
        role_entry = tk.Entry(self.root)
        role_entry.pack()

        def create_account_action():
            username = username_entry.get()
            password = password_entry.get()
            role = role_entry.get()

            if role == "1":
                user = Librarian(username, password)
            elif role == "2":
                user = Member(username, password)
            elif role == "3":
                user = Manager(username, password)
            else:
                messagebox.showerror("Error", "Invalid role selected")
                return

            self.library_system.add_user(user)
            messagebox.showinfo("Success", "Account created successfully!")
            self.main_menu()

        tk.Button(self.root, text="Create Account", command=create_account_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    def manager_menu(self, manager):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text="Manager Menu", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Borrowed Books by Specific User", command=self.borrowed_books_by_user_screen).pack(pady=5)
        tk.Button(self.root, text="Borrowed Books by Date", command=self.borrowed_books_by_date_screen).pack(pady=5)
        tk.Button(self.root, text="Total Borrowed Books", command=self.total_borrowed_books_screen).pack(pady=5)
        tk.Button(self.root, text="Reserved Books by Specific User", command=self.reserved_books_by_user_screen).pack(pady=5)
        tk.Button(self.root, text="Total Books in Borrow Process", command=self.total_books_in_borrow_process_screen).pack(pady=5)
        
        tk.Button(self.root, text="Export Member Names to CSV", command=lambda: self.export_member_names()).pack(pady=5)
        tk.Button(self.root, text="Export Books Borrowed Per Member to CSV", command=lambda: self.export_books_borrowed_per_member()).pack(pady=5)
        tk.Button(self.root, text="Export All Book Entries to CSV", command=lambda: self.export_all_books()).pack(pady=5)
        tk.Button(self.root, text="Export Total Borrowed Books Per Day to CSV", command=lambda: self.export_total_borrowed_books_per_day()).pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.main_menu).pack(pady=10)

    def borrowed_books_by_user_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter User ID", font=("Arial", 16)).pack(pady=10)
        user_id_entry = tk.Entry(self.root)
        user_id_entry.pack()

        def show_borrowed_books_by_user():
            user_id = user_id_entry.get()
            count = self.library_system.borrowed_books_by_user(user_id)
            messagebox.showinfo("Result", f"User {user_id} has borrowed {count} books.")

        tk.Button(self.root, text="Show", command=show_borrowed_books_by_user).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.manager_menu(self.current_user)).pack(pady=5)

    def borrowed_books_by_date_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Date (DD-MM-YYYY)", font=("Arial", 16)).pack(pady=10)
        date_entry = tk.Entry(self.root)
        date_entry.pack()

        def show_borrowed_books_by_date():
            date_str = date_entry.get()
            count = self.library_system.borrowed_books_by_date(date_str)
            messagebox.showinfo("Result", f"On {date_str}, {count} books were borrowed.")

        tk.Button(self.root, text="Show", command=show_borrowed_books_by_date).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.manager_menu(self.current_user)).pack(pady=5)


    def total_borrowed_books_screen(self):
        count = self.library_system.total_borrowed_books()
        messagebox.showinfo("Result", f"Total borrowed books: {count}.")
        self.manager_menu(self.current_user)

    def reserved_books_by_user_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter User ID", font=("Arial", 16)).pack(pady=10)
        user_id_entry = tk.Entry(self.root)
        user_id_entry.pack()

        def show_reserved_books_by_user():
            user_id = user_id_entry.get()
            count = self.library_system.reserved_books_by_user(user_id)
            messagebox.showinfo("Result", f"User {user_id} has reserved {count} books.")

        tk.Button(self.root, text="Show", command=show_reserved_books_by_user).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.manager_menu(self.current_user)).pack(pady=5)

    def total_books_in_borrow_process_screen(self):
        count = self.library_system.total_books_in_borrow_process()
        messagebox.showinfo("Result", f"Total books in borrow process: {count}.")
        
        self.manager_menu(self.current_user)




    def user_menu(self, user):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        tk.Label(self.root, text=f"Welcome, {user.username}", font=("Arial", 16)).pack(pady=10)

        if isinstance(user, Librarian):
            tk.Button(self.root, text="Add Book", command=lambda: self.add_book_screen(user)).pack(pady=5)
            tk.Button(self.root, text="Check Reservations", command=lambda: self.check_reservations(user)).pack(pady=5)
        elif isinstance(user, Member):
            tk.Button(self.root, text="Borrow Book", command=lambda: self.borrow_book_screen(user)).pack(pady=5)
            tk.Button(self.root, text="Return Book", command=lambda: self.return_book_screen(user)).pack(pady=5)
            tk.Button(self.root, text="Reserve Book", command=lambda: self.reserve_book_screen(user)).pack(pady=5)
        elif isinstance(user, Manager):
            self.manager_menu(user)
            
        tk.Button(self.root, text="Logout", command=self.main_menu).pack(pady=10)

    def add_book_screen(self, librarian):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        tk.Label(self.root, text="Add Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Title").pack()
        title_entry = tk.Entry(self.root)
        title_entry.pack()

        tk.Label(self.root, text="Author").pack()
        author_entry = tk.Entry(self.root)
        author_entry.pack()

        tk.Label(self.root, text="ISBN").pack()
        isbn_entry = tk.Entry(self.root)
        isbn_entry.pack()

        tk.Label(self.root, text="Category").pack()
        category_entry = tk.Entry(self.root)
        category_entry.pack()

        tk.Label(self.root, text="Copies").pack()
        copies_entry = tk.Entry(self.root)
        copies_entry.pack()

        tk.Label(self.root, text="Date Added (DDMMYY)").pack()
        date_added_entry = tk.Entry(self.root)
        date_added_entry.pack()

        def add_book_action():
            title = title_entry.get()
            author = author_entry.get()
            isbn = isbn_entry.get()
            category = category_entry.get()
            copies = int(copies_entry.get())
            date_added = date_added_entry.get()

            book = Book(title, author, isbn, category, copies, date_added)
            librarian.add_book(self.library_system, book)
            messagebox.showinfo("Success", f"Book '{title}' added to the system.")
            self.user_menu(librarian)

        tk.Button(self.root, text="Add Book", command=add_book_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.user_menu(librarian)).pack(pady=5)

    def check_reservations(self, librarian):
        reservations = self.library_system.get_reserved_books()  # Καλούμε από το library_system
        
        if reservations:
            messagebox.showinfo("Reservations", "\n".join([f"{book.title} by {book.author}" for book in reservations]))
        else:
            messagebox.showinfo("Reservations", "No books reserved.")
        
        self.librarian_menu(librarian)


    def get_reserved_books(self):
        reserved_books = [book for book in self.books if book.status == "Reserved"]
        
        # DEBUG: Εκτυπώνουμε τα κρατημένα βιβλία
        print(f"DEBUG: Found {len(reserved_books)} reserved books.")
        
        return reserved_books

            
    def borrow_book_screen(self, member):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Get a list of books with available copies for borrowing
        book_titles = [f"{book.title} (Available: {book.available_copies})" for book in self.library_system.books if book.available_copies > 0]

        if not book_titles:
            messagebox.showinfo("No Books", "No books available for borrowing.")
            self.user_menu(member)
            return

        tk.Label(self.root, text="Borrow a Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Select a book to borrow:").pack()

        selected_book_title = tk.StringVar(self.root)
        selected_book_title.set(book_titles[0])

        book_menu = tk.OptionMenu(self.root, selected_book_title, *book_titles)
        book_menu.pack()

        def borrow_book_action():
            title_with_available = selected_book_title.get()
            title = title_with_available.split(" (Available: ")[0]  # Extract the title
            
            success = member.borrow_book_by_title(self.library_system, title)
            if success:
                messagebox.showinfo("Success", f"Book '{title}' has been borrowed successfully!")
            else:
                messagebox.showerror("Error", f"Failed to borrow '{title}' (no available copies).")
            self.user_menu(member)

        tk.Button(self.root, text="Borrow Book", command=borrow_book_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.user_menu(member)).pack(pady=5)

    def return_book_screen(self, member):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        # List of books borrowed by the specific user (filter by user ID)
        borrowed_books = [f"{book.title} (Borrowed: {book.borrowed_by.count(member.id)})"
                        for book in self.library_system.books if member.id in book.borrowed_by]

        # Check if there are any borrowed books
        if not borrowed_books:
            messagebox.showinfo("No Books", "You have no books to return.")
            self.user_menu(member)
            return

        tk.Label(self.root, text="Return a Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Select a book to return:").pack()

        # Dropdown menu for borrowed books
        selected_book_title = tk.StringVar(self.root)
        selected_book_title.set(borrowed_books[0])  # Default value is the first borrowed book

        book_menu = tk.OptionMenu(self.root, selected_book_title, *borrowed_books)
        book_menu.pack()

        def return_book_action():
            title_with_borrowed = selected_book_title.get()
            title = title_with_borrowed.split(" (Borrowed: ")[0]  # Extract the title
            
            # Attempt to return the book
            success = member.return_book_by_title(self.library_system, title)
            if success:
                messagebox.showinfo("Success", f"Book '{title}' has been returned successfully!")
            else:
                messagebox.showerror("Error", f"Failed to return the book '{title}'.")
            self.user_menu(member)

        tk.Button(self.root, text="Return Book", command=return_book_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.user_menu(member)).pack(pady=5)

    def reserve_book_screen(self, member):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Get a list of books with available copies for reservation
        available_books = [f"{book.title} (Available: {book.available_copies})" for book in self.library_system.books if book.available_copies > 0]

        # Get a list of reserved books by the member (for declining the reservation)
        reserved_books = [f"{book.title} (Reserved)" for book in self.library_system.books if book.status == "Reserved"]

        # Check if there are any available books for reservation
        if not available_books:
            messagebox.showinfo("No Books", "No books available for reservation.")
            self.user_menu(member)
            return

        tk.Label(self.root, text="Reserve a Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Select a book to reserve:").pack()

        # Dropdown menu for available books
        selected_book_title = tk.StringVar(self.root)
        selected_book_title.set(available_books[0])  # Default value is the first book

        book_menu = tk.OptionMenu(self.root, selected_book_title, *available_books)
        book_menu.pack()

        def reserve_book_action():
            title_with_status = selected_book_title.get()
            title = title_with_status.split(" (Available: ")[0]  # Extract the title
            
            # Try to reserve the book
            success = member.reserve_book_by_title(self.library_system, title)
            if success:
                messagebox.showinfo("Success", f"Book '{title}' has been reserved successfully!")
            else:
                messagebox.showerror("Error", f"Failed to reserve the book '{title}'.")
            self.user_menu(member)

        tk.Button(self.root, text="Reserve Book", command=reserve_book_action).pack(pady=10)

        # Decline reservation section
        if reserved_books:
            tk.Label(self.root, text="Select a reserved book to decline:").pack()

            # Dropdown menu for reserved books
            selected_reserved_book_title = tk.StringVar(self.root)
            selected_reserved_book_title.set(reserved_books[0])  # Default value is the first reserved book

            reserved_book_menu = tk.OptionMenu(self.root, selected_reserved_book_title, *reserved_books)
            reserved_book_menu.pack()

            def decline_reserve_action():
                title_with_reserved = selected_reserved_book_title.get()
                title = title_with_reserved.split(" (Reserved)")[0]  # Extract the title

                # Try to decline the reservation
                success = member.decline_reserve_by_title(self.library_system, title)
                if success:
                    messagebox.showinfo("Success", f"Reservation for '{title}' has been declined.")
                else:
                    messagebox.showerror("Error", f"Failed to decline the reservation for '{title}'.")
                self.user_menu(member)

            tk.Button(self.root, text="Decline Reserve", command=decline_reserve_action).pack(pady=10)

        tk.Button(self.root, text="Back", command=lambda: self.user_menu(member)).pack(pady=5)

    def borrow_for_member_screen(self, librarian):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.root, text="Borrow Book for a Member", font=("Arial", 16)).pack(pady=10)

        # Dropdown to select a member
        tk.Label(self.root, text="Select Member:").pack()
        member_list = [f"{member.username} (ID: {member.id})" for member in self.library_system.users if isinstance(member, Member)]
        
        if not member_list:
            messagebox.showinfo("No Members", "There are no members to borrow a book for.")
            self.librarian_menu(librarian)
            return
        
        selected_member = tk.StringVar(self.root)
        selected_member.set(member_list[0])  # Default selection is the first member

        member_menu = tk.OptionMenu(self.root, selected_member, *member_list)
        member_menu.pack()

        # Dropdown to select a book
        tk.Label(self.root, text="Select a Book to Borrow:").pack()
        book_titles = [f"{book.title} (Available: {book.available_copies})" for book in self.library_system.books if book.available_copies > 0]
        
        if not book_titles:
            messagebox.showinfo("No Books", "No books are available for borrowing.")
            self.librarian_menu(librarian)
            return

        selected_book_title = tk.StringVar(self.root)
        selected_book_title.set(book_titles[0])  # Default selection is the first available book

        book_menu = tk.OptionMenu(self.root, selected_book_title, *book_titles)
        book_menu.pack()

        def borrow_book_action():
            member_info = selected_member.get()
            member_id = member_info.split("(ID: ")[1][:-1]  # Extract member ID
            book_info = selected_book_title.get()
            book_title = book_info.split(" (Available: ")[0]  # Extract book title

            # Find the selected member object by ID
            member = next((user for user in self.library_system.users if user.id == member_id), None)

            # Find the selected book object by title
            book = next((b for b in self.library_system.books if b.title == book_title), None)

            if member and book:
                success = self.library_system.borrow_book_librarian(member, book.id)
                if success:
                    messagebox.showinfo("Success", f"Book '{book.title}' has been successfully borrowed for {member.username}.")
                else:
                    messagebox.showerror("Error", f"Failed to borrow '{book.title}'. No copies available.")
            else:
                messagebox.showerror("Error", "Error in borrowing process. Please try again.")
            
            self.librarian_menu(librarian)

        tk.Button(self.root, text="Borrow Book", command=borrow_book_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.librarian_menu(librarian)).pack(pady=5)


    def export_member_names(self):
        self.library_system.export_member_names_to_csv("member_names.csv")
        messagebox.showinfo("Export Complete", "Member names exported to member_names.csv")

    def export_books_borrowed_per_member(self):
        self.library_system.export_books_borrowed_per_member_to_csv("books_borrowed_per_member.csv")
        messagebox.showinfo("Export Complete", "Books borrowed per member exported to books_borrowed_per_member.csv")

    def export_all_books(self):
        self.library_system.export_all_books_to_csv("all_books.csv")
        messagebox.showinfo("Export Complete", "All book entries exported to all_books.csv")

    def export_total_borrowed_books_per_day(self):
        self.library_system.export_total_borrowed_books_per_day_to_csv("borrowed_books_per_day.csv")
        messagebox.showinfo("Export Complete", "Total borrowed books per day exported to borrowed_books_per_day.csv")

    def view_reports(self, manager):
        reports = manager.view_reports(self.library_system)
        report_str = "\n".join([f"{key}: {value}" for key, value in reports.items()])
        messagebox.showinfo("Reports", report_str)

    def librarian_menu(self, librarian):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Librarian Menu", font=("Arial", 16)).pack(pady=10)

        
        tk.Button(self.root, text="Add New Book", command=lambda: self.add_book_screen(librarian)).pack(pady=5)
        tk.Button(self.root, text="Check Reservations", command=lambda: self.check_reservations(librarian)).pack(pady=5)
        tk.Button(self.root, text="Borrow Book for Member", command=lambda: self.borrow_for_member_screen(librarian)).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.main_menu).pack(pady=10)
        
    def on_closing(self):
        # Save all books and users before closing
        self.library_system.save_books_to_csv("library_books.csv")
        self.library_system.save_users_to_csv("users.csv")
        self.root.destroy()

def main():
    root = tk.Tk()
    app = LibraryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Save on exit
    root.mainloop()

if __name__ == "__main__":
    main()
