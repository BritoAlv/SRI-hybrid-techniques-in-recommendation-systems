import random as rd
from entities_repr import Book, User
from test_books import books

# Generate random ratings for the books
def generate_random_ratings( books : list[Book]) -> dict[str, float]:
    ratings = {}
    selected_books = rd.sample(books, rd.randint(1, len(books)))
    for book in selected_books:
        rating = round(rd.uniform(1.0, 5.0), 1)
        ratings[book.title] = rating
    return ratings

def generate_users() -> list[User]:
    users = []
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack", "Kate", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Ryan", "Sophia", "Thomas", "Uma", "Victor", "Wendy", "Xavier", "Yara", "Zoe"]
    for name in names:
        user = User(name, generate_random_ratings(books))
        users.append(user)
    return users
