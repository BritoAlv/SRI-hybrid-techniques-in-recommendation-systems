from abc import ABC, abstractmethod
import random

class ISimilar(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def similarity(self, other : "ISimilar") -> float:
        """
        expected to be in [0, 1] with 0 not similar. this function should be symetric ie, and reflexive.
        f(x, y) = f(y, x)
        f(x, x) = 1
        """
        pass

def Kmeans( objects : list[ISimilar] , number_clusters = 40):
        result = {}
        number_clusters = min(number_clusters, len(objects))
        for obj in objects:
            result[obj] = [0] * number_clusters

        def assign_clusters(clusters: list[list[ISimilar]], centroids: list[ISimilar]):
            for obj in objects:
                similarity = [obj.similarity(centroid) for centroid in centroids]
                cluster = similarity.index(max(similarity))
                clusters[cluster].append(obj)

        def update_centroids(clusters: list[list[ISimilar]], centroids: list[ISimilar]):
            new_centroids = []
            for i in range(number_clusters):
                if clusters[i]:
                    max_similarity_product = -1
                    new_centroid = None
                    for obj in clusters[i]:
                        similarity_product = 1
                        for other in clusters[i]:
                            similarity_product *= obj.similarity(other)
                        if similarity_product > max_similarity_product:
                            max_similarity_product = similarity_product
                            new_centroid = obj
                    new_centroids.append(new_centroid)
            return new_centroids

        clusters = [[] for _ in range(number_clusters)]
        centroids = random.sample(objects, number_clusters)
        for _ in range(10):
            assign_clusters(clusters, centroids)
            new_centroids = update_centroids(clusters, centroids)
            if new_centroids == centroids:
                break
            else:
                centroid = new_centroids

        for obj in objects:
            result[obj] = []
            for centroid in centroids:
                result[obj].append(obj.similarity(centroid))

        return result