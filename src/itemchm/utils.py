from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import itemchm.persistence.entities as db

def sentiment_analysis(text : str):
    # Create a SentimentIntensityAnalyzer object
    sia = SentimentIntensityAnalyzer()

    # Perform sentiment analysis
    sentiment_scores = sia.polarity_scores(text)
    
    if sentiment_scores['compound'] < -0.1:
        return 1
    elif sentiment_scores['compound'] < 0.1:
        return 4
    else:
        return 6
        
def overall_rate(user_book : db.UserBook) -> float:
    RATING_WEIGHT = 4
    COMMENT_WEIGHT = 3
    SHARED_WEIGHT = 2
    READ_RATIO_WEIGHT = 1

    if user_book.rating == None:
        rating_value = 4
    else:
        rating_value = user_book.rating + 1
    
    if user_book.comment == None:
        comment_value = 4
    else:
        comment_value = sentiment_analysis(user_book.comment)
    
    read_ration_value = user_book.readRatio * 5 + 1

    if user_book.shared <= 0:
        shared_value = 1
    elif user_book.shared < 3:
        shared_value = 2
    elif user_book.shared < 6:
        shared_value = 3
    elif user_book.shared < 8:
        shared_value = 4
    elif user_book.shared < 12:
        shared_value = 5
    else:
        shared_value = 6

    return (RATING_WEIGHT * rating_value + COMMENT_WEIGHT * comment_value + SHARED_WEIGHT * shared_value + READ_RATIO_WEIGHT * read_ration_value) / (RATING_WEIGHT + COMMENT_WEIGHT + SHARED_WEIGHT + READ_RATIO_WEIGHT)