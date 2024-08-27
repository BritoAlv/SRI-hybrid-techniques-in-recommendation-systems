class Book:
    def __init__(self, title : str, author : str, year : int, language : str, genres : list[str]):
        self.title = title
        self.author = author
        self.year = year
        self.language = language
        self.genres = genres

    def __hash__(self) -> int:
        return self.title.__hash__()
    
    def __str__(self) -> str:
        return self.title + " by " + self.author + " (" + str(self.year) + ")" + " in " + self.language + " genres: " + str(self.genres)
    
    @staticmethod
    def similarity(one : "Book", other : "Book") -> float:
        
        matches = 10
        if one.author == other.author:
            matches += 3
        
        if one.year == other.year:
            matches += 1

        if one.language == other.language:
            matches += 1

        return (matches / 15) * len(set(one.genres).intersection(set(other.genres))) / len(set(one.genres).union(set(other.genres)))

class User:
    def __init__(self, name : str, ratings : dict[str, float]):
        self.name = name
        self.ratings = ratings
    
    def __hash__(self) -> int:
        return self.name.__hash__()
    
    def __str__(self) -> str:
        rs = self.name + " rated :" + "\n"
        to_order = []
        for title in self.ratings.keys():
            to_order.append((title, self.ratings[title]))
        to_order.sort(key = lambda x: x[1], reverse = True)
        for title, rating in to_order:
            rs += title + " : " + str(rating) + "\n"
        return rs