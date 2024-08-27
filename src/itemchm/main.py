from entities_repr import User
from test_books import books
from test_user import generate_users
from hybrid_recommender import HybridRecommender

users = generate_users()
system = HybridRecommender(books, users)

selected_user = User(1241241241, "BritoAlv", { 4 : 5})

result = system.recommend(selected_user, 5)

for book in result:
    print(book)

print("")
print(selected_user)