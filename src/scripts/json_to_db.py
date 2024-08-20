import json
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from entities import Book

# Constants
ENGINE = create_engine("sqlite:///bookshelf.db", echo=True)

with Session(ENGINE) as session:
    for i in range(1, 501):
        file_name = f'./gutenberg_data/gutenberg_{i}.json'
        with open(file_name, 'r') as file:
            data = json.load(file)

        for book in data['results']:
            name = book['title']
            language = book['languages'][0]
            author = book['authors'][0]['name'] if len(book['authors']) > 0 else 'Anonymous'
            year = book['authors'][0]['birth_year'] if len(book['authors']) > 0 and book['authors'][0]['birth_year'] != None else None    

            book = Book()
            book.name = name
            book.language = language
            book.author = author
            book.year = year
            session.add(book)

        print(f'{file_name} processed')
    session.commit()
        