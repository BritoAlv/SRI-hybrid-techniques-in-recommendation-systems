import json
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session

from api.recommender_handler import RecommenderHandler
from itemchm.hybrid_recommender import HybridRecommender
from itemchm.persistence.entities import Book, Genre, User, UserBook
from api.response import Response

app = Flask(__name__)
CORS(app)

ENGINE = create_engine("sqlite:///../../bookshelf.db", echo=True) # From file directory

DATA_DIRECTORY = './data/'

RECOMMENDER_HANDLER = RecommenderHandler()

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

@app.route('/bookshelf/rating', methods = ['GET'])
def rating_get():
    user_id = int(request.args.get('user_id'))
    book_id = int(request.args.get('book_id'))

    with Session(ENGINE) as session:
        user_book = session.query(UserBook).filter(UserBook.userId == user_id, UserBook.bookId == book_id).first()

    if user_book == None:
        return jsonify(Response.error(f"User with id {user_id} has never visited book with id {book_id}"))
    
    response = Response.rating(user_book.readRatio, user_book.rating, user_book.comment)
    return jsonify(response), 200

@app.route('/bookshelf/rating', methods = ['POST'])
def rating_post():
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
        response = [(book.name, book.id) for book in session.query(Book).filter(Book.name.contains(query)).all()]
    return jsonify(response), 200

@app.route('/bookshelf/recommend/<user_id>', methods = ['GET'])
def recommend(user_id):
    user = RecommenderHandler.instantiate_user(user_id)
    recommender = RECOMMENDER_HANDLER.get_recommender()

    response = [book.title for book in recommender.recommend(user, 10)]
    RECOMMENDER_HANDLER.dispose()

    return jsonify(response), 200
    
if __name__ == '__main__':
    app.run(debug=False, port=5000)