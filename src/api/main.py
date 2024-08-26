import json
import random
from flask import Flask, Response, jsonify, request, send_file
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session

from entities import Book, Genre, User, UserBook
from recommender import Recommender
from response import Response

app = Flask(__name__)

ENGINE = create_engine("sqlite:///../../bookshelf.db", echo=True) # From file directory
DATA_DIRECTORY = './data/'
RECOMMENDER = Recommender(DATA_DIRECTORY, ENGINE)
RECOMMENDER = Recommender(DATA_DIRECTORY, ENGINE)


@app.route('/', methods = ['GET'])
def home():
    return send_file("./public/index.html")

@app.route('/register', methods = ['GET'])
def register():
    return send_file("./public/register.html")

@app.route('/login', methods = ['GET'])
def login():
    return send_file("./public/login.html")


@app.route('/bookshelf/register', methods = ['POST'])
def register_user():
    data = request.get_json()
    name = data['name']
    email = data['email']

    # Verify email is not already registered
    with Session(ENGINE) as session:
        user = session.query(User).filter(User.email == email).first()
    
    if user != None:
        return jsonify(Response.error("User already registered")), 400

    # Create user
    user = User()
    user.name = name
    user.email = email

    # Persist user in DB
    with Session(ENGINE) as session:
        session.add(user)
        session.commit()
        user = session.query(User).filter(User.email == email).first()

    response = Response.user(user.id, email)
    return jsonify(response), 200

@app.route('/bookshelf/login', methods = ['POST'])
def login_user():
    data = request.get_json()
    email = data['email']

    # Verify email is already registered
    with Session(ENGINE) as session:
        user = session.query(User).filter(User.email == email).first()
    
    if user == None:
        return jsonify(Response.error("Email is not registered")), 400
    
    response = Response.user(user.id, email)
    return jsonify(response), 200


@app.route('/bookshelf/features', methods = ['GET'])
def features_get():
    # Retrieve genres
    with Session(ENGINE) as session:
        genres = [genre.name for genre in session.query(Genre).all()]

    # Retrieve top authors
    with open(f'{DATA_DIRECTORY}top_authors.json', 'r') as file:
        top_authors = json.load(file)

    response = Response.features(
        genres,
        top_authors['authors'][:20],
        [0, 1, 2]
    )

    return jsonify(response), 200


@app.route('/bookshelf/features', methods = ['POST'])
def features_post():
    # Extract data from request
    data = request.get_json()
    user_id = data['user_id']
    data = {
        'genres': data['genres'],
        'authors': data['authors'],
        'time_periods': data['time_periods']
    }
    data = json.dumps(data)

    # Update user's features
    with Session(ENGINE) as session:
        user = session.query(User).filter(User.id == user_id).first()
        
        if user == None:
            return jsonify(Response.error(f"user_id {user_id} is not registered"))

        statement = update(User).where(User.id == user_id).values(features=data)
        session.execute(statement)
        session.commit()

    return "200 OK", 200

@app.route('/bookshelf/rating', methods = ['POST'])
def rating():
    data = request.get_json()

    user_id = data['user_id']
    book_id = data['book_id']
    rating = data['rating']
    read_ratio = data['read_ratio']
    shared = data['shared']
    comment = data['comment']

    with Session(ENGINE) as session:
        user = session.query(User).filter(User.id == user_id).first()
        book = session.query(Book).filter(Book.id == book_id).first()

        if user == None:
            return jsonify(Response.error(f"user_id {user_id} does not exist"))            
        if book == None:
            return jsonify(Response.error(f"book_id {book_id} does not exist"))

        user_book = session.query(UserBook).filter(UserBook.userId == user_id and UserBook.bookId == book_id).first()

        if user_book == None:
            user_book = UserBook(user_id, book_id)
            user_book.readRatio = read_ratio
            user_book.shared = shared
            user_book.rating = rating if 0 <= rating <= 5 else None
            user_book.comment = comment if comment != "" else None
            session.add(user_book)
        else:
            shared += user_book.shared
            read_ratio = user_book.readRatio if read_ratio < user_book.readRatio else read_ratio
            statement = update(UserBook).where(UserBook.bookId == book_id and UserBook.userId == user_id).values(shared=shared, readRatio=read_ratio, comment=comment, rating=rating)
            session.execute(statement)
        session.commit()

    return "200 OK", 200

@app.route('/bookshelf/search/<query>', methods = ['GET'])
def search(query : str):
    query = query.lower()

    with Session(ENGINE) as session:
        response = [book.name for book in session.query(Book).filter(Book.name.contains(query)).all()]
    return jsonify(response), 200

@app.route('/bookshelf/recommend/<user_id>', methods = ['GET'])
def recommend(user_id):
    response = RECOMMENDER.recommend(int(user_id))

    return jsonify(response), 200
    

if __name__ == '__main__':
    app.run(debug=True)