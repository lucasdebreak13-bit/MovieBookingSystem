class Movie:
    def __init__(self, movie_id, title, genre, duration, age_rating, language):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.duration = duration
        self.age_rating = age_rating
        self.language = language
    def display_info(self):
        print('Movie ID:',self.movie_id)
        print('Title:', self.title)
        print('Genre',self.genre)
        print('Duration',self.duration,'minutes')
        print('Age rating',self.age_rating)
        print('Language', self.language)
movie1 = Movie('M01','Avatar','Sci-fi',192,'T13','English')
movie2 = Movie('M02','Conan','Animation',110,'P','Vietsub')
movie3= Movie('M03','Jurassic World','Adventure',124,'T18','English')
movie4= Movie('M04','Interstella','Sci-fi',169,'T16','English')
movie5= Movie('M05','The Conjuring','Horror', 112,'K','Japanese')
movies=[movie1, movie2, movie3, movie4, movie5]
for movie in movies:
    print('..................')
    movie.display_info()