import pickle
import random

import numpy as np
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from surprise import Dataset, KNNWithMeans, Reader, KNNBasic

from entities import Book, User, UserBook

# Constants
ENGINE = create_engine("sqlite:///../../bookshelf.db", echo=True)
HYPERPLANES = 8

class Recommender:
    def __init__(self, data_dir : str) -> None:
        self.data_dir = data_dir
        self.trained_algo : KNNWithMeans = self._get_trained_algo()
        self.utility_matrix = self._get_utility_matrix()
        self.lsh_dict, self.book_lsh = self._get_lsh()

    def _get_trained_algo(self):
        with open(f'{self.data_dir}rating_frame.pkl', 'rb') as file:
            rating_frame = pickle.load(file)

        reader = Reader(rating_scale=(1, 5))
        dataset = Dataset.load_from_df(rating_frame[['book_id', 'user_id', 'overall_rating']], reader)

        sim_options = {
            "name": "cosine",
            "user_based": False,  # Compute  similarities between items
        }

        algo = KNNBasic(sim_options=sim_options)

        trainingSet = dataset.build_full_trainset()
        algo.fit(trainingSet)
        
        return algo
    
    def _get_utility_matrix(self):
        with open(f'{self.data_dir}utility_matrix.pkl', 'rb') as file:
            utility_matrix = pickle.load(file)
        return utility_matrix

    def _get_lsh(self):
        lsh_dict : dict[str, list[int]]= {}
        book_lsh : dict[int, str] = {}

        hyperplanes = HYPERPLANES
        dimension = self.utility_matrix.shape[1] # Take vector dimensions

        plane_norms = np.random.rand(hyperplanes, dimension) - .5

        for index, row in self.utility_matrix.iterrows():
            row_centered = row - row.mean() # Center the row to zero mean.
            row_vector = row_centered.values # Take the row vector

            row_dot = np.dot(row_vector, plane_norms.T) # Compute the dot product with each plane.
            row_dot = (row_dot > 0).astype(int) # Convert the result to binary.
            hash_str = ''.join(row_dot.astype(str)) # Convert to string

            # Save in dictionary
            if hash_str in lsh_dict:
                lsh_dict[hash_str].append(index)
            else:
                lsh_dict[hash_str] = [index] 
            
            book_lsh[index] = hash_str

        return (lsh_dict, book_lsh)
    
    def update_rating_frame(self):
        with Session(ENGINE) as session:
            user_books = session.query(UserBook).all() # Get all user_books

            rating_frame = DataFrame(columns=['book_id', 'user_id', 'overall_rating']) # Create utility matrix

            for i, user_book in enumerate(user_books):
                rating_frame.loc[i] = (user_book.bookId, user_book.userId, self._overall_rate(user_book))

        with open('./data/rating_frame.pkl', 'wb') as file:
            pickle.dump(rating_frame, file)
        
        # Update training algo
        self.trained_algo = self.get_trained_algo()

    def update_utility_matrix(self) -> DataFrame:    
        with Session(ENGINE) as session:
            users = session.query(User).all() # Get all users
            books = session.query(Book).all() # Get all books
            
            user_books = session.query(UserBook).all() # Get all user_books

            utility_matrix = DataFrame(index=[book.id for book in books], columns=[user.id for user in users]) # Create utility matrix

            for user_book in user_books:
                utility_matrix.loc[user_book.bookId, user_book.userId] = self._overall_rate(user_book) # Populate utility matrix

        utility_matrix = utility_matrix.fillna(0)

        with open(f'{self.data_dir}utility_matrix.pkl', 'wb') as file:
            pickle.dump(utility_matrix, file)
        
        self.utility_matrix = utility_matrix
        self.lsh_dict, self.book_lsh = self._get_lsh()

    def _get_closest_books(self, user_id : int):
        with Session(ENGINE) as session:
            # Select book-ids from user's user_books
            user_books = session.query(UserBook).filter(UserBook.userId == user_id).all()
        rated_books = [user_book.bookId for user_book in user_books]

        # Sort by overall rating
        rated_books = sorted(rated_books, key=lambda x: self.utility_matrix.loc[x, user_id])

        # Take top ten rated_books
        if len(rated_books) > 10:
            rated_books = rated_books[0:10]

        target_books : set[int] = set() 
        for book in rated_books:
            hash_str = self.book_lsh[book]
            close_books = self.lsh_dict[hash_str]

            if len(close_books) > 10:
                close_books = random.choices(close_books, k=10)
            
            for close_book in close_books:
                if close_book not in target_books and close_book not in rated_books:
                    target_books.add(close_book)
            
        return target_books
    
    def recommend(self, user_id : int):
        closest_books = self._get_closest_books(user_id)

        pairs = []
        for book in closest_books:
            pairs.append((self.trained_algo.predict(user_id, book).est, book))

        return sorted(pairs, key=lambda x: -x[0])
    
    # ** Inner helper functions
    # TODO: Must be implemented
    def _overall_rate(user_book : UserBook) -> float:
        return random.randint(1, 5)
    
DATA_DIR = './data/'
r = Recommender(DATA_DIR)

for i in range(100):
    print(r.recommend(i))