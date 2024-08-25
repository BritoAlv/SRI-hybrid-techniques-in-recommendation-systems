from enum import Enum
import logging
from queue import PriorityQueue
import random
import requests
import json
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import create_engine
from faker import Faker
import difflib

from entities import Book, BookGenre, Genre, User, UserBook

TOP_SIZE = 1000

class TimePeriod(Enum):
    ANCIENT = 0
    MODERN = 1
    CONTEMPORARY = 2

class DataCollector:
    def __init__(self, directory : str, connection_string : str) -> None:
        self.directory = directory
        self.connection_string = connection_string

    # Load from Gutendex Web-API
    def load_from_api(self) -> None:
        TOTAL_PAGES = 2300
        GUTENDEX_URL = 'https://gutendex.com/books/'

        for i in range(1, TOTAL_PAGES + 1):
            url = f'{GUTENDEX_URL}?page={i}'
            response = requests.get(url)

            if response.status_code == 200:
                with open(f'{self.directory}/gutendex_{i}.json', 'wb') as file:
                    file.write(response.content)
            else:
                raise Exception(f"Invalid response code {response.status_code}")
    
    # Bring data into db
    def store_into_db(self) -> None:

        ENGINE = create_engine(self.connection_string, echo=True)

        books_pq : PriorityQueue[tuple[float, int]] = PriorityQueue()
        authors_pq : PriorityQueue[tuple[float, str]] = PriorityQueue()

        with Session(ENGINE) as session:

            # Get genres and store them
            with open('./data/genres.json', 'r') as file:
                genre_data = json.load(file)
            for genre in genre_data['genres']:
                session.add(Genre(genre))

            for i in range(1, 51):
                file_name = f'{self.directory}/gutendex_{i}.json'
                with open(file_name, 'r') as file:
                    data = json.load(file)

                for book in data['results']:
                    # Extract meaningful data from json
                    id = book['id']
                    name = book['title']
                    language = book['languages'][0]
                    author = book['authors'][0]['name'] if len(book['authors']) > 0 else 'Anonymous'
                    year = book['authors'][0]['birth_year'] if len(book['authors']) > 0 and book['authors'][0]['birth_year'] != None else None    
                    downloads = book['download_count']
                    subjects = book['subjects']

                    # Create Book and store it
                    book = Book()
                    book.id = id
                    book.name = name
                    book.language = language
                    book.author = author
                    book.year = year

                    if session.query(Book).filter(Book.id == id).first() != None:
                        print(f'Warning repeated id {id} at file {file_name}')
                        continue
                    else:
                        session.add(book)

                    # Derive and store genres from subjects
                    genres = set()
                    for subject in subjects:
                        genre = self._find_most_similar(subject, genre_data['genres']) # Find most similar genre to the given subject
                        # Ensure each genre is store once
                        if genre not in genres:
                            session.add(BookGenre(id, genre))
                            genres.add(genre)

                    books_pq.put((downloads, id))
                    authors_pq.put((downloads, author))
                    if books_pq.qsize() > TOP_SIZE:
                        books_pq.get()
                    if authors_pq.qsize() > 3 * TOP_SIZE:
                        authors_pq.get()

                print(f'{file_name} processed')
            session.commit()
        
        top_authors = []
        while authors_pq.qsize() > 0:
            author = authors_pq.get()[1]
            if author in top_authors:
                top_authors.remove(author)
            top_authors.insert(0, author)

        top_authors = {
            'authors': top_authors
        }
        data = json.dumps(top_authors)
        with open('./data/top_authors.json', 'w', encoding='UTF-8') as file:
                file.write(data)
        
        top_books = []
        while books_pq.qsize() > 0:
            book = books_pq.get()[1]
            if book in top_books:
                top_books.remove(book)
            top_books.insert(0, book)

        top_books = {
            'books': top_books
        }
        data = json.dumps(top_books)
        with open('./data/top_books.json', 'w', encoding='UTF-8') as file:
                file.write(data)

        print("top_authors.json and top_books.json successfully created")
        
    def generate_user_books(self):
        ENGINE = create_engine(self.connection_string, echo=True)
        fake = Faker()
        users = [0, 0]

        with Session(ENGINE) as session:
            genres = session.query(Genre).all()

            with open('./data/top_authors.json') as file:
                top_authors = json.load(file)
            top_authors = top_authors['authors']

            with open('./data/top_books.json') as file:
                top_books = json.load(file)
            top_books = top_books['books']

            # Take only 300 from top_authors
            top_authors = top_authors[:100]

            for i in range(1, 100):
                user = User()
                user.id = i
                user.name = fake.name()
                user.email = f'{i}{random.randint(0, 500)}{fake.email()}'
                session.add(user)

                #** Generate user features
                time_period = random.choice([TimePeriod.ANCIENT, TimePeriod.MODERN, TimePeriod.CONTEMPORARY])
                k_genres = random.choices(population=genres, k=random.randint(1, 15))
                k_authors = random.choices(population=top_authors, k=random.randint(1, 10))

                chosen_books = set()
                for book_id in random.choices(population=top_books, k=random.randint(1, 600)):
                    if book_id in chosen_books:
                        continue
                    chosen_books.add(book_id)
                    
                    book = session.query(Book).filter(Book.id == book_id).options(joinedload(Book.genres)).first()
                    
                    match_genre = False
                    for genre in book.genres:
                        if genre in k_genres:
                            match_genre = True
                            break
                    
                    if book.author in k_authors or match_genre or (book.year != None and self._get_time_period(book.year) == time_period):
                        users[0] += 1
                        user_book = self._positive_user_book(i, book_id)
                        session.add(user_book)
                    else:
                        users[1] += 1
                        user_book = self._negative_user_book(i, book_id)
                        session.add(user_book)

            session.commit()
        print(f'''
Positive users: {users[0]},
Negative users: {users[1]}
''')

    def _find_most_similar(self, input_string : str, string_set : set[str]):
        input_string = input_string.lower()
        matcher = difflib.SequenceMatcher(None, input_string)

        for str in string_set:
            if str in input_string:
                return str

        most_similar = None
        max_similarity = 0

        for string in string_set:
            # Calculate the similarity score
            matcher.set_seq2(string)
            similarity = matcher.ratio()

            if similarity > max_similarity:
                most_similar = string
                max_similarity = similarity

        return most_similar

    def _get_time_period(self, year : int):
        if year <= 500:
            return TimePeriod.ANCIENT
        elif year <= 1500:
            return TimePeriod.MODERN
        else:
            return TimePeriod.CONTEMPORARY

    def _positive_user_book(self, user_id : int, book_id : int):
        shared = random.randint(3, 20)
        read_ratio = random.randint(50, 100) / 100
        rating = random.randint(3, 5)
        comment = random.choice([
            'It is a really good book. I would read it again',
            'Just love it',
            'I would recommend this book to anyone. It is a hidden diamond'
        ])

        user_book = UserBook(user_id, book_id)
        user_book.shared = shared
        user_book.readRatio = read_ratio
        user_book.rating = rating
        user_book.comment = comment
        return user_book

    def _neutral_user_book(self, user_id : int, book_id : int):
        shared = random.randint(2, 5)
        read_ratio = random.randint(40, 80) / 100
        rating = random.randint(2, 4)
        comment = random.choice([
            'If you put the effort might learn things from it',
            'Not good for everyone',
            "It was good to read it, but I'm not sure that I would do it again"
        ])

        user_book = UserBook(user_id, book_id)
        user_book.shared = shared
        user_book.readRatio = read_ratio
        user_book.rating = rating
        user_book.comment = comment
        return user_book

    def _negative_user_book(self, user_id : int, book_id : int):
        shared = random.randint(0, 2)
        read_ratio = random.randint(0, 50) / 100
        rating = random.randint(0, 2)
        comment = random.choice([
            "Simply don't like the book",
            "It's awful",
            "Terrible book! (in the bad sense)"
        ])

        user_book = UserBook(user_id, book_id)
        user_book.shared = shared
        user_book.readRatio = read_ratio
        user_book.rating = rating
        user_book.comment = comment
        return user_book

DIRECTORY = './data/gutendex_data'
CONNECTION_STRING = "sqlite:///bookshelf.db"
collector = DataCollector(DIRECTORY, CONNECTION_STRING)

# collector.store_into_db()
collector.generate_user_books()

# delete from Genres
# delete from Books