from entities_repr import Book, User
from itemchm.hybrid_recommender import HybridRecommender

principito = Book("El Principito", "Antoine de Saint-Exupéry", 1943, "Spanish", ["Fiction", "Children"])
alquimista = Book("El Alquimista", "Paulo Coelho", 1988, "Spanish", ["Fiction"])
angel_demonio = Book("Ángeles y Demonios", "Dan Brown", 2000, "Spanish", ["Fiction", "Mystery"])
probability_essentials = Book("Probability Essentials", "Jean Jacod", 2003, "English", ["Mathematics"])
harry_potter = Book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 1997, "English", ["Fiction", "Fantasy"])
to_kill_a_mockingbird = Book("To Kill a Mockingbird", "Harper Lee", 1960, "English", ["Fiction", "Classic"])

user1 = User("Alice", {"El Principito": 5.0, "El Alquimista": 4.0, "Ángeles y Demonios": 4.5, "Harry Potter and the Philosopher's Stone": 4.0, "To Kill a Mockingbird": 3.5})
user2 = User("Bob", {"El Principito": 4.0, "El Alquimista": 3.5, "Ángeles y Demonios": 4.0, "Harry Potter and the Philosopher's Stone": 4.5, "To Kill a Mockingbird": 3.0})
user3 = User("Charlie", {"El Principito": 3.0, "El Alquimista": 3.5, "Ángeles y Demonios": 4.0, "Harry Potter and the Philosopher's Stone": 4.5, "To Kill a Mockingbird": 3.0})

books = [principito, alquimista, angel_demonio, probability_essentials, harry_potter, to_kill_a_mockingbird]
users = [user1, user2, user3]

system = HybridRecommender(books, users)

print(system.recommend(user1, 3))