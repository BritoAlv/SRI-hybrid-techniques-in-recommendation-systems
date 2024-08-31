import pickle as pk
from itemchm.entities_repr import Book, User
from itemchm.hybrid_recommender import HybridRecommender
import csv

with open("../system.pk", "rb") as s:
    system = pk.load(s)

assert(isinstance(system, HybridRecommender))

with open("../books.pk", "rb") as b:
    books = pk.load(b)

book_dict : dict[int, Book] = {}

for book in books:
    assert(isinstance(book, Book))
    book_dict[book.id] = book

with open("../users_test.pk", "rb") as u:
    users_test = pk.load(u)

# Specify the path and filename for the CSV file
csv_file = "recommendation_results.csv"

# Open the CSV file in write mode
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["Real Rating", "Predicted Rating"])

    # Iterate over the users and their ratings
    for user in users_test:
        assert(isinstance(user, User))
        for book_id in user.ratings:
            predicted_rating = system.predict(user, book_dict[book_id])
            real_rating = user.ratings[book_id]
            
            # Write the real rating and predicted rating to the CSV file
            writer.writerow([real_rating, predicted_rating])