class Book:
    def __init__(self, title, author, isbn, category, total_copies, date_added, status="Available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.category = category
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.date_added = date_added
        self.status = status
        self.borrowed_by = []  # Store a list of user IDs who have borrowed this book
        self.id = None  # Book ID
        self.reserved_by = None  # User ID που έχει κάνει κράτηση το βιβλίο
        self.date_borrowed = None 