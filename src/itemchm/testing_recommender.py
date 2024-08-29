import pickle as pk
from itemchm.entities_repr import Book, User
from itemchm.hybrid_recommender import HybridRecommender

with open("system.pk", "rb") as s:
    system = pk.load(s)

assert(isinstance(system, HybridRecommender))

with open("books.pk", "rb") as b:
    books = pk.load(b)

book_dict : dict[int, Book] = {}

for book in books:
    assert(isinstance(book, Book))
    book_dict[book.id] = book

with open("users_test.pk", "rb") as u:
    users_test = pk.load(u)

n  = 0
sum = 0
for user in users_test:
    assert(isinstance(user, User))
    for book_id in user.ratings:
        n += 1
        predicted_rating = system.predict(user, book_dict[book_id])
        real_rating = user.ratings[book_id]
        sum += abs(real_rating - predicted_rating)

print( sum / n)