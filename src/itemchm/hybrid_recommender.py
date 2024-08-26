import random
import numpy as np
from itemchm.entities_repr import Book, User


class HybridRecommender:
    def __init__(self, books: list[Book], users: list[User]):
        self.books = books
        self.users = users
        self.item_rating: None | dict[Book, User] = None
        self.group_rating: None | dict[Book, list[float]] = None
        self.item_rating_similitud: None | dict[Book, dict[Book, float]] = None
        self.group_rating_similitud: None | dict[Book, dict[Book, float]] = None
        self.averages_book: None | dict[Book, float] = None
        self.averages_user: None | dict[User, float] = None

    def build_item_rating(self):
        result = {}
        for book in self.books:
            for user in self.users:
                if book.title in user.ratings:
                    result[book][user] = user.ratings[book]
        self.item_rating = result

    def build_group_rating(self, number_clusters=2):
        result = {}
        number_clusters = min(number_clusters, len(self.books))
        for book in self.books:
            result[book] = [0] * number_clusters

        def assign_clusters(clusters, centroids):
            for book in self.books:
                similarity = [Book.similarity(book, centroid) for centroid in centroids]
                cluster = similarity.index(max(similarity))
                clusters[cluster].append(book)

        def update_centroids(clusters, centroids):
            new_centroids = []
            for i in range(number_clusters):
                if clusters[i]:
                    max_similarity_product = -1
                    new_centroid = None
                    for book in clusters[i]:
                        similarity_product = 1
                        for other in clusters[i]:
                            similarity_product *= Book.similarity(book, other)
                        if similarity_product > max_similarity_product:
                            max_similarity_product = similarity_product
                            new_centroid = book
                    new_centroids.append(new_centroid)
            return new_centroids

        for _ in range(100):
            clusters = [[] for _ in range(number_clusters)]
            centroids = random.sample(self.books, number_clusters)
            assign_clusters(clusters, centroids)
            new_centroids = update_centroids(clusters, centroids)
            if new_centroids == centroids:
                break

        maxx_similarity = max(
            [
                Book.similarity(book, centroid)
                for book in self.books
                for centroid in new_centroids
            ]
        )

        for book in self.books:
            for i in range(number_clusters):
                result[book][i] = (
                    Book.similarity(book, new_centroids[i]) / maxx_similarity
                )

        self.group_rating = result

    def build_averages_book(self):
        averages = {}
        for book in self.books:
            averages[book] = sum(self.item_rating[book].values()) / len(
                self.item_rating[book]
            )
        self.averages_book = averages

    def build_averages_user(self):
        averages = {}
        for user in self.users:
            averages[user] = sum(user.ratings.values()) / len(user.ratings)
        self.averages_user = averages

    def build_item_rating_similitud(self):
        if self.item_rating is None:
            self.build_item_rating()
        if self.averages_book is None:
            self.build_averages_book()
        assert self.item_rating != None
        result = {}

        for book in self.books:
            result[book] = {}
            users = []
            for user in self.users:
                if book in user.ratings:
                    users.append(user)
            for other in self.books:
                num = 0
                den1 = 0
                den2 = 0
                for user in self.users:
                    if other in user.ratings:
                        num += (
                            self.item_rating[book][user] - self.averages_book[book]
                        ) * (self.item_rating[other][user] - self.averages_book[other])
                        den1 += (
                            self.item_rating[book][user] - self.averages_book[book]
                        ) ** 2
                        den2 += (
                            self.item_rating[other][user] - self.averages_book[other]
                        ) ** 2
                result[book][other] = num / (np.sqrt(den1) * np.sqrt(den2))
        self.item_rating_similitud = result

    def build_group_rating_similitud(self):
        if self.group_rating is None:
            self.build_group_rating()
        if self.averages_user is None:
            self.build_averages_user()
        assert self.group_rating != None

        result = {}
        for book in self.books:
            result[book] = {}
            for other in self.books:
                num = 0
                den1 = 0
                den2 = 0
                for user in self.users:
                    if book.title in user.ratings and other.title in user.ratings:
                        num += (user.ratings[book.title] - self.averages_user[user]) * (
                            user.ratings[other.title] - self.averages_user[user]
                        )
                        den1 += (user.ratings[book.title] - self.averages_user[user]) ** 2
                        den2 += (user.ratings[other.title] - self.averages_user[user]) ** 2
                result[book][other] = num / (np.sqrt(den1) * np.sqrt(den2))

        self.group_rating_similitud = result

    def build_similitud_matrix(self, linear_coef=0.4):
        if self.item_rating_similitud is None:
            self.build_item_rating_similitud()
        if self.group_rating_similitud is None:
            self.build_group_rating_similitud()
        assert self.item_rating_similitud != None
        assert self.group_rating_similitud != None

        result = {}
        for book in self.books:
            result[book] = {}
            for other in self.books:
                result[book][other] = (
                    linear_coef * self.item_rating_similitud[book][other]
                    + (1 - linear_coef) * self.group_rating_similitud[book][other]
                )

        self.similitud_matrix = result

    def predict(self, user: User, book: Book) -> float:
        if self.similitud_matrix is None:
            self.build_similitud_matrix()
        assert self.similitud_matrix != None

        average_rating_book = self.averages_book[book]
        num = 0
        den = 0
        for other in self.books:
            if other.title in user.ratings:
                sim = self.similitud_matrix[book][other]
                num += (user.ratings[other.title] - self.averages_book[other]) * sim
                den += abs(sim)
        return average_rating_book + num / den

        pass

    def recommend(self, user: User, top: int) -> list[Book]:
        preds = []
        for book in self.books:
            preds.append((book, self.predict(user, book)))

        preds.sort(key=lambda x: x[1], reverse=True)
        return [x[0] for x in preds[:top]]