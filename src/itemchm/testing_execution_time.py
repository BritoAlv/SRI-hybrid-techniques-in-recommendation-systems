from itemchm.entities_repr import User
from itemchm.hybrid_recommender import HybridRecommender

import pickle as pk
import random as rd
import time

with open("system.pk", "rb") as s:
    system = pk.load(s)

with open("users.pk", "rb") as u:
    users = pk.load(u)


assert(isinstance(system, HybridRecommender))
print("Done Loading System")
for i in range(0, 100):
    selected_user = rd.sample(users, k = 1)[0]
    start_time = time.time()
    result = system.recommend(selected_user, 5)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

for book in result:
    print(book)

print("")
print(selected_user)