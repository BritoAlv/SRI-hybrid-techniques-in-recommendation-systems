import numpy as np
from itemchm.entities_repr import Book, User
from itemchm.kmeans import Kmeans

class HybridRecommender:
    def __init__(self, books: list[Book], users: list[User]):
        self.books = books
        self.users = users

        self.item_rating: None | dict[Book, User] = None
        self.group_rating_by_book: None | dict[Book, list[float]] = None

        self.item_rating_similitud: None | dict[Book, dict[Book, float]] = None
        self.group_rating_similitud_book: None | dict[Book, dict[Book, float]] = None
        self.similitud_matrix: None | dict[Book, dict[Book, float]] = None
        self.averages_book: None | dict[Book, float] = None
        self.averages_user: None | dict[User, float] = None

    def build_item_rating(self):
        """
        build item - item matrix
        """
        print("Start building Item Rating Matrix")
        result = {}
        for book in self.books:
            result[book] = {}
            for user in self.users:
                if book.id in user.ratings:
                    result[book][user] = user.ratings[book.id]
        self.item_rating = result
        print("End building Item Rating Matrix")

    def build_group_rating(self, number_clusters=40):
        """
        build group - item matrix using K - Means
        """
        print("Start building Group Rating Matrix")
        self.group_rating_by_book = Kmeans(self.books, number_clusters)
        print("End building Group Rating Matrix")

    def build_averages_book(self):
        """
        compute average rating of book
        """
        print("Start building Averages Book Array")
        averages = {}
        for book in self.books:
            averages[book] = 0
            raters = 0
            for user in self.users:
                if book.id in user.ratings:
                    averages[book] += user.ratings[book.id]
                    raters += 1
            if raters > 0:
                averages[book] /= raters
        self.averages_book = averages
        print("End building Averages Book Array")

    def build_averages_user(self):
        """
        compute average rating of user.
        """
        print("Start building Averages User Array")
        averages = {}
        for user in self.users:
            averages[user] = sum(user.ratings.values()) / len(user.ratings)
        self.averages_user = averages
        print("End building Averages User Array")

    def build_item_rating_similitud(self):
        """
        build item - item similitud matrix.
        """
        print("Start building Item Rating Similitud")
        if self.item_rating is None:
            self.build_item_rating()
        if self.averages_book is None:
            self.build_averages_book()
        result = {}
        for book in self.books:
            result[book] = {}
            users_with_book: list[User] = []
            for user in self.users:
                if book.id in user.ratings:
                    users_with_book.append(user)
            for other in self.books:
                num = 0
                den1 = 0
                den2 = 0
                for user in users_with_book:
                    if other.id in user.ratings:
                        num += (
                            self.item_rating[book][user] - self.averages_book[book]
                        ) * (self.item_rating[other][user] - self.averages_book[other])
                        den1 += (
                            self.item_rating[book][user] - self.averages_book[book]
                        ) ** 2
                        den2 += (
                            self.item_rating[other][user] - self.averages_book[other]
                        ) ** 2
                if den1 == 0 or den2 == 0:
                    result[book][other] = 0
                else:
                    result[book][other] = num / (np.sqrt(den1) * np.sqrt(den2))
        self.item_rating_similitud = result
        print("End building Item Rating Similitud")

    def build_group_rating_similitud(self):
        """
        build group - group rating matrix.
        """
        print("Start building Group Rating Similitud")
        if self.group_rating_by_book is None :
            self.build_group_rating()
        if self.averages_user is None:
            self.build_averages_user()
        assert self.group_rating_by_book != None

        cluster_avgs = [0] * len(self.group_rating_by_book[self.books[0]])
        for book in self.books:
            for i in range(len(self.group_rating_by_book[book])):
                cluster_avgs[i] += self.group_rating_by_book[book][i]
        for i in range(len(cluster_avgs)):
            cluster_avgs[i] /= len(self.books)

        result = {}
        for book in self.books:
            result[book] = {}
            for other in self.books:
                num = 0
                den1 = 0
                den2 = 0
                for cluster in range(len(self.group_rating_by_book[book])):
                    num += (
                        self.group_rating_by_book[book][cluster] - cluster_avgs[cluster]
                    ) * (self.group_rating_by_book[other][cluster] - cluster_avgs[cluster])
                    den1 += (
                        self.group_rating_by_book[book][cluster] - cluster_avgs[cluster]
                    ) ** 2
                    den2 += (
                        self.group_rating_by_book[other][cluster] - cluster_avgs[cluster]
                    ) ** 2
                if den1 == 0 or den2 == 0:
                    result[book][other] = 0
                else:
                    result[book][other] = num / (np.sqrt(den1) * np.sqrt(den2))

        self.group_rating_similitud_book = result
        print("End building Group Rating Similitud")

    def build_similitud_matrix(self, linear_coef=0.4):
        """
        combine matrix to produce final matrix.
        """
        print("Start Mixing Matrix")
        if self.item_rating_similitud is None:
            self.build_item_rating_similitud()
        if self.group_rating_similitud_book is None:
            self.build_group_rating_similitud()
        assert self.item_rating_similitud != None
        assert self.group_rating_similitud_book != None

        result = {}
        for book in self.books:
            result[book] = {}
            for other in self.books:
                result[book][other] = (
                    linear_coef * self.item_rating_similitud[book][other]
                    + (1 - linear_coef) * self.group_rating_similitud_book[book][other]
                )

        self.similitud_matrix = result
        print("End Mixing Matrix")

    def compute_data(self):
        if self.similitud_matrix is None:
            self.build_similitud_matrix()

    def predict(self, user: User, book: Book) -> float:
        """
        predict given User and book.
        """
        if self.similitud_matrix is None:
            self.build_similitud_matrix()
        assert self.similitud_matrix != None
        prediction = self.averages_book[book]
        num = 0
        den = 0
        for other in self.books:
            if other.id in user.ratings:
                sim = self.similitud_matrix[book][other]
                num += (user.ratings[other.id] - self.averages_book[other]) * sim
                den += abs(sim)
        if den != 0:
            prediction += num / den
        return prediction

    def recommend(self, user: User, top: int) -> list[Book]:
        """
        use top predictions to recommend a book.
        """
        preds = []
        for book in self.books:
            #print(f"Start computing prediction of {book.title} for user {user.name}")
            preds.append((book, self.predict(user, book)))
            #print(f"End computing prediction of {book.title} for user {user.name}")

        preds.sort(key=lambda x: x[1], reverse=True)
        return [x[0] for x in preds[:top]]