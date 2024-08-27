import random
from entities_repr import Book, User
from test_books import books
from test_user import generate_users
from hybrid_recommender import HybridRecommender


users = generate_users()
system = HybridRecommender(books, users)

selected_user = User("BritoAlv", { "Probability Essentials" : 5})

result = system.recommend(selected_user, 5)

for book in result:
    print(book)

print("")
print(selected_user)