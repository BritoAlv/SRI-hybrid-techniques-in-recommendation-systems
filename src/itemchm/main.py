from itemchm.entities_repr import User
from itemchm.hybrid_recommender import HybridRecommender

import pickle as pk

with open("system.pk", "wb") as s:
    system = pk.load(s)

assert(isinstance(system, HybridRecommender))

selected_user = User(1241241241, "BritoAlv", { 4 : 5})

result = system.recommend(selected_user, 5)

for book in result:
    print(book)

print("")
print(selected_user)