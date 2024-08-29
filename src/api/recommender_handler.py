import pickle
from threading import Lock, Thread
import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload

from itemchm.hybrid_recommender import HybridRecommender
from itemchm.utils import overall_rate
import itemchm.persistence.entities as db
from itemchm.hybrid_recommender import HybridRecommender
from itemchm.entities_repr import User, Book


class RecommenderHandler:
    def __init__(self) -> None:
        self._recommender : HybridRecommender = None

        with open('./data/system.pkl', 'rb') as file:
            self._recommender = pickle.load(file)

        self._lock = Lock()
        self._acquired = False

        Thread(target=self._update).start()

    def acquire(self):
        with self._lock:
            while self._acquired:
                time.sleep(1)
            self._acquired = True

    def dispose(self):
        self._acquired = False

    def get_recommender(self):
        self.acquire()
        return self._recommender

    def _update(self):
        while True:
            time.sleep(3600)
            self._update_recommender()

    def _update_recommender(self):
        # Create engine
        ENGINE = create_engine("sqlite:///../../bookshelf.db", echo=True)

        with Session(ENGINE) as session:
            db_users = session.query(db.User).all()
            db_books = session.query(db.Book).options(joinedload(db.Book.genres)).all()
            db_user_books = session.query(db.UserBook).all()

        users_dict : dict[int, User] = {}

        for db_user in db_users:
            user = User(db_user.id, db_user.name, {})
            users_dict[db_user.id] = user

        books : list[Book] = []

        for db_book in db_books:
            genres = [book_genre.genresName for book_genre in db_book.genres]
            book = Book(db_book.id, db_book.name, db_book.author, db_book.year, db_book.language, genres)
            books.append(book)

        for user_book in db_user_books:
            rating = overall_rate(user_book)
            user = users_dict[user_book.userId]
            user.ratings[user_book.bookId] = rating

        # Required Input
        users = list(users_dict.values())

        recommender = HybridRecommender(books, users)
        recommender.compute_data()

        self.acquire()
        self._recommender = recommender
        self.dispose()

    @staticmethod
    def instantiate_user(user_id : int):
        # Create engine
        ENGINE = create_engine("sqlite:///../../bookshelf.db", echo=True)

        with Session(ENGINE) as session:
            db_user = session.query(db.User).where(db.User.id == user_id).first()

            if db_user == None:
                raise Exception("Non registered user-id")

            user_books = session.query(db.UserBook).join(db.User, db.UserBook.userId == db.User.id).filter(db.User.id == user_id).all()
        
        user = User(user_id, db_user.name, {})

        for user_book in user_books:
            rating = overall_rate(user_book)
            user.ratings[user_book.bookId] = rating

        return user