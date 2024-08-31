from itemchm.entities_repr import User
from itemchm.hybrid_recommender import HybridRecommender

import pickle as pk
import random as rd
import time
import csv

with open("../system.pk", "rb") as s:
    system = pk.load(s)

with open("../users.pk", "rb") as u:
    users = pk.load(u)

assert isinstance(system, HybridRecommender)
print("Done Loading System")

with open("execution_times.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Execution Time"])

    for i in range(0, 100):
        selected_user = rd.sample(users, k=1)[0]
        start_time = time.time()
        result = system.recommend(selected_user, 5)
        end_time = time.time()
        execution_time = end_time - start_time
        writer.writerow([execution_time])