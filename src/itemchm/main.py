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