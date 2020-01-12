# Built-ins
import csv
import pandas as pd
# Class imports
from movie import Movie

# Globals
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
moviesList = []

f = open("output.txt","w+")

df = pd.merge(ratings, movies, on="movieId")

movie_matrix = df.pivot_table(index="userId", columns="title", values="rating")
corr_matrix = movie_matrix.corr(method="pearson", min_periods=50)
movie_matrix_shape = movie_matrix.shape



def parse_movies():
    with open('movies.csv', 'r', encoding="utf8") as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        firstLine = True
        for row in filereader:
            if firstLine:
                firstLine = False
                continue
            x = Movie()
            x.setMovieId(int(row[0]))
            x.setMovieTitle(row[1])
            moviesList.append(x)

def getRecommendations():
    for i in range(1, movie_matrix_shape[0]):
        userratings = movie_matrix.iloc[i].dropna()
        recommend = pd.Series()

        for j in range(0, len(userratings)):
            #print("*****Adding similar movies to " + userratings.index[j] + "*****")
            similar = corr_matrix[userratings.index[j]].dropna()
            similar = similar.map(lambda x: x * userratings[j])
            recommend = recommend.append(similar)

        recommend.sort_values(inplace=True, ascending=False)
        recommend = recommend.drop_duplicates(keep='first', inplace=False)
        f.write("\nUser-Id" + str(i))

    
        x = pd.DataFrame(recommend)
        recommend_filter = x[~x.index.isin(userratings.index)]
    
        count = 0
        top5 = []
        for index, row in recommend_filter.iterrows():
            if index not in top5:
                top5.append(index)
            if len(top5) == 5:
                break

        top5ID = []
        for item in top5:
            for movie in moviesList:
                if item == movie.getMovieTitle():
                    top5ID.append(movie.getMovieId())

        for item in top5ID:
            f.write(" " + str(item))

if __name__ == "__main__":
    print("Parsing movies..")
    parse_movies()
    print("Getting recommendations..")
    getRecommendations()
    print("All done! - answers can be found in output.txt")
    f.close()