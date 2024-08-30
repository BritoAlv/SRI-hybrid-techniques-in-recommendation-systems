from flask import Flask, Response, jsonify, request, send_file

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    return send_file("./public/index.html")

@app.route('/register', methods = ['GET'])
def register():
    return send_file("./public/register.html")

@app.route('/login', methods = ['GET'])
def login():
    return send_file("./public/login.html")

@app.route('/recommended', methods = ['GET'])
def recomended():
    return send_file("./public/recomended.html")

@app.route('/search', methods = ['GET'])
def searchPage():
    return send_file("./public/search.html")

@app.route('/book', methods = ['GET'])
def book():
    return send_file("./public/book.html")

if __name__ == '__main__':
    app.run(debug=True, port=5050)