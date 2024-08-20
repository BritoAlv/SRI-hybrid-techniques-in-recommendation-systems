from typing import Any
from sqlalchemy import UUID, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    userBooks = relationship("UserBook", back_populates='user')

    def __repr__(self):
        return f'User({self.id}, {self.name}, {self.email})'
    
class Book(Base):
    __tablename__ = 'Books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    language = Column(String)
    year = Column(Integer)
    genres = relationship("BookGenre", back_populates="book")
    userBooks = relationship("UserBook", back_populates='book')

    def __repr__(self):
        return f'Book({self.id}, {self.name}, {self.author})'
    
class Genre(Base):
    __tablename__ = 'Genres'

    name = Column(String, primary_key=True)
    books = relationship("BookGenre", back_populates="genre")

    def __init__(self, name, **kw: Any):
        super().__init__(**kw)
        self.name = name

    def __repr__(self):
        return f'Genre({self.name})'


class BookGenre(Base):
    __tablename__ = 'BookGenre'

    booksId = mapped_column(ForeignKey('Books.id'), primary_key=True)
    genresName = mapped_column(ForeignKey('Genres.name'), primary_key=True)
    book = relationship("Book", back_populates='genres')
    genre = relationship("Genre", back_populates='books')

    def __init__(self, booksId, genresName, **kw: Any):
        super().__init__(**kw)
        self.booksId = booksId
        self.genresName = genresName

    def __repr__(self):
        return f'BookGenre(book-id: {self.booksId}, genre: {self.genresName})'

class UserBook(Base):
    __tablename__ = 'UserBooks'

    id = Column(Integer, primary_key=True)
    readRatio = Column(Float)
    rating = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)
    shared = Column(Integer)

    bookId = mapped_column(ForeignKey('Books.id'))
    userId = mapped_column(ForeignKey('Users.id'))
    book = relationship("Book", back_populates='userBooks')
    user = relationship("User", back_populates='userBooks')

    def __init__(self, userId, bookId, **kw: Any):
        super().__init__(**kw)
        self.userId = userId
        self.bookId = bookId

    def __repr__(self):
        return f'UserBook(id: {self.id}, user-id: {self.userId}, book-id: {self.bookId})'