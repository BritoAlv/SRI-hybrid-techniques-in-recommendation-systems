from queue import PriorityQueue
import random
import uuid
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload
from entities import Book, BookGenre, Genre, User, UserBook
import numpy as np

pd.set_option('future.no_silent_downcasting', True) # Avoid downcasting warnings

# Constants
ENGINE = create_engine("sqlite:///../../../bookshelf.db", echo=True)
HYPERPLANES = 10

# ** Inner helper functions
# TODO: Must be implemented
def overall_rate(user_book : UserBook) -> float:
    return random.randint(0, 5)

def hamming_similarity_estimate(hamming_distance : int, total_hyperplanes : int) -> float:
    if hamming_distance < 0 or hamming_distance > total_hyperplanes:
        raise ValueError("Hamming distance must be between 0 and total_hyperplanes")
    return -(2 / total_hyperplanes) * hamming_distance + 1

def estimate_top(utility_matrix : DataFrame, lsh_matrix : DataFrame, user_id : int, non_rated_books : list[Book], rated_books_ids : list[int], total : int = 20) -> PriorityQueue[tuple[float, int]]:
    pq : PriorityQueue[tuple[float, int]] = PriorityQueue()

    for non_rated_book in non_rated_books:
        non_rated_book_id = non_rated_book.id
        non_rated_binary = lsh_matrix.loc[non_rated_book_id].values

        weighted_sum = 0.0
        similarity_sum = 0.0

        for rated_book_id in rated_books_ids:
            rated_binary = lsh_matrix.loc[rated_book_id].values
            
            hamming_distance = np.count_nonzero(rated_binary != non_rated_binary)

            # TODO: Reflect about negative similarities
            estimated_similarity = hamming_similarity_estimate(hamming_distance, HYPERPLANES)

            user_rating = utility_matrix.loc[rated_book_id, user_id]

            weighted_sum += estimated_similarity * user_rating

            similarity_sum += estimated_similarity
    
        estimated_rating = weighted_sum / similarity_sum if similarity_sum > 0 else 0.

        pq.put((estimated_rating, non_rated_book_id))
        
        if pq.qsize() > total:
            pq.get()
    
    return pq


## ** .NET interactive functions
def utility_matrix() -> DataFrame:    
    with Session(ENGINE) as session:
        users = session.query(User).all() # Get all users
        books = session.query(Book).all() # Get all books
        
        user_books = session.query(UserBook).all() # Get all user_books

        utility_matrix = DataFrame(index=[book.id for book in books], columns=[user.id for user in users]) # Create utility matrix

        for user_book in user_books:
            utility_matrix.loc[user_book.bookId, user_book.userId] = overall_rate(user_book) # Populate utility matrix

    utility_matrix = utility_matrix.fillna(0)
    return utility_matrix

def lsh_matrix(utility_matrix : DataFrame) -> DataFrame:
    hyperplanes = HYPERPLANES
    dimension = utility_matrix.shape[1] # Take vector dimensions

    lsh_matrix = pd.DataFrame(index=utility_matrix.index, columns=[i for i in range(hyperplanes)], dtype=np.int64)

    plane_norms = np.random.rand(hyperplanes, dimension) - .5

    for index, row in utility_matrix.iterrows():
        row_centered = row - row.mean() # Center the row to zero mean.
        row_vector = row_centered.values # Take the row vector

        row_dot = np.dot(row_vector, plane_norms.T) # Compute the dot product with each plane.
        row_dot = (row_dot > 0).astype(int) # Convert the result to binary.

        lsh_matrix.loc[index] = row_dot # Assign the binary representation to the corresponding row in the LSH matrix.

    return lsh_matrix

def recommend_books(utility_matrix : DataFrame, lsh_matrix : DataFrame, user_id : int, total : int = 20):
    with Session(ENGINE) as session:
        rated_user_books = session.query(UserBook).filter(UserBook.userId == user_id).all()
        rated_books_ids = [user_book.bookId for user_book in rated_user_books]

        non_rated_books = session.query(Book).filter(~Book.id.in_(rated_books_ids)).all()

    estimate_pq = estimate_top(utility_matrix, lsh_matrix, user_id, non_rated_books, rated_books_ids, total)
    optimal_pq : PriorityQueue[tuple[float, int]] = PriorityQueue()

    while estimate_pq.qsize() > 0:
        _, non_rated_book_id = estimate_pq.get()

        non_rated_vector = utility_matrix.loc[non_rated_book_id] - utility_matrix.loc[non_rated_book_id].mean()
        non_rated_vector = non_rated_vector.values

        non_rated_norm = np.linalg.norm(non_rated_vector)

        weighted_sum = .0
        similarity_sum = .0

        for rated_book_id in rated_books_ids:
            rated_vector = utility_matrix.loc[rated_book_id] -  utility_matrix.loc[rated_book_id].mean()
            rated_vector = rated_vector.values

            rated_norm = np.linalg.norm(rated_vector)

            dot_product = np.dot(non_rated_vector, rated_vector)
            
            user_rating = utility_matrix.loc[rated_book_id, user_id]
            similarity = dot_product / non_rated_norm * rated_norm if non_rated_norm * rated_norm != 0 else 0
            weighted_sum += user_rating * similarity
            similarity_sum += similarity
        
        estimated_ranking = weighted_sum / similarity_sum if similarity_sum > 0 else 0.
        optimal_pq.put((estimated_ranking, non_rated_book_id))

    recommendation = []
    while(optimal_pq.qsize() > 0):
        recommendation.append(optimal_pq.get())
    return recommendation