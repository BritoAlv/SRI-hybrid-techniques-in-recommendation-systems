from kmeans import ISimilar

class Book(ISimilar):
    def __init__(self, id : int, title : str, author : str, year : int, language : str, genres : list[str]):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.language = language
        self.genres = genres

    def __hash__(self) -> int:
        return self.title.__hash__() + self.id.__hash__()
    
    def __str__(self) -> str:
        return self.title + " by " + self.author + " (" + str(self.year) + ")" + " in " + self.language + " genres: " + str(self.genres)
    
    
    def similarity(self, other : "Book") -> float:
        one = self
        matches = 10
        if one.author == other.author:
            matches += 3
        
        if one.year == other.year:
            matches += 1

        if one.language == other.language:
            matches += 1

        result = matches / 15
        intersec = len(set(one.genres).intersection(set(other.genres)))
        union = len(set(one.genres).union(set(other.genres)))
        if union != 0:
            result *= intersec / union 

        return result

class User():
    def __init__(self, id : int, name : str, ratings : dict[int, float]):
        self.id = id
        self.name = name
        self.ratings = ratings
    
    def __hash__(self) -> int:
        return self.name.__hash__() + self.id.__hash__()
        
    def __str__(self) -> str:
        rs = self.name + " rated :" + "\n"
        to_order = []
        for id in self.ratings.keys():
            to_order.append((id, self.ratings[id]))
        to_order.sort(key = lambda x: x[1], reverse = True)
        for id, rating in to_order:
            rs += str(id) + " : " + str(rating) + "\n"
        return rs