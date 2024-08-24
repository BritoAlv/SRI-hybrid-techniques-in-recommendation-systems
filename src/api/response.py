class Response:
    @staticmethod
    def user(id, email):
        return {
            'id': id,
            'email': email
        }
    
    @staticmethod
    def features(genres, authors, time_periods):
        return {
            'genres': genres,
            'authors': authors,
            'time_periods': time_periods
        }

    @staticmethod
    def error(message):
        return {
            'message': message,
        }