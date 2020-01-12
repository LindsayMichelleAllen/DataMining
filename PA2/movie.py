class Movie:
    movieId = 0
    movieTitle = ""
    year = 0
    genre = []

    def getMovieId(self):
        return self.movieId

    def setMovieId(self, newId):
        self.movieId = newId

    def getMovieTitle(self):
        return self.movieTitle

    def setMovieTitle(self, newTitle):
        self.movieTitle = newTitle

    def getYear(self):
        return self.year

    def setYear(self, newYear):
        self.year = newYear

    def getGenreList(self):
        return self.genre

    def addGenre(self, newGenre):
        self.genre.append(newGenre)
    