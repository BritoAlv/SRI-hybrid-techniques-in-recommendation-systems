class Response:
    @staticmethod
    def user(id, email):
        return {
            'id': id,
            'email': email
        }
    
    @staticmethod
    def rating(read_ratio, rating, comment):
        return {
            'read_ratio': read_ratio,
            'rating': rating,
            'comment': comment
        }

    @staticmethod
    def error(message):
        return {
            'message': message,
        }