class Movie:
    def __init__(self, movie_id, title, genre, duration, age_rating, language, ticket_price, release_year, status="Now Showing"):
        if not movie_id.strip():
            raise ValueError(
                'Movie ID cannot be empty'
                )

        if not title.strip():
            raise ValueError(
                'Title cannot be empty'
                )

        if not isinstance(duration, int) or duration <= 0:
            raise ValueError(
                'Duration must be a positive integer'
                )

        if not isinstance(ticket_price, (int, float)) or ticket_price < 0:
            raise ValueError(
                'Ticket price cannot be negative'
                )
        
        if not genre.strip():
            raise ValueError(
                'Genre cannot be empty'
                )
        
        if not language.strip():
            raise ValueError(
                'Language cannot be empty'
                )
        if age_rating not in [
            'P', 'K', 'T13', 'T16', 'T18'
            ]:
            raise ValueError(
                'Invalid age rating'
                )

        if type(release_year) is not int or release_year < 1888:
            raise ValueError(
                'Invalid release year'
                )

        if status not in [
            'Now Showing', 'Coming Soon', 'Ended'
            ]:
            raise ValueError(
                'Invalid movie status'
                )
# thiếu try,except
#attribute
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.duration = duration
        self.age_rating = age_rating
        self.language = language
        self.ticket_price = ticket_price
        self.release_year = release_year
        self.status = status
    def display_info(self):
        print(
            'Movie ID:',self.movie_id
            )
        print(
            'Title:', self.title
            )
        print(
            'Genre',self.genre
            )
        print(
            'Duration',self.duration,'minutes'
            )
        print(
            'Age rating',self.age_rating
            )
        print(
            'Language', self.language
            )
        print(
            'Ticket Price:', self.ticket_price
            )
        print(
            'Release Year:', self.release_year
            )
        print(
            'Status:', self.status
            )
    def __str__(self):
          return (
                f'{self.movie_id} - '
                f'{self.title} - '
                f'{self.genre} - '
                f'{self.ticket_price:,.0f} VND'
                 )
    
    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if type(value) is not int or value <= 0:
            raise ValueError(
                'Duration must be a positive integer'
                )

        self._duration = value
    @property
    def ticket_price(self):
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, value):
        if type(value) not in (int, float) or value < 0:
            raise ValueError(
                'Ticket price cannot be negative'
                )

        self._ticket_price = float(value)
        
movie1 = Movie(
    'M01','Avatar 10','Sci-fi',192,'T13','English',80000.0,2026
    )
movie2 = Movie(
    'M02','Cyberfun 2099','Animation',110,'P','Vietnamese',120000.0,2099,'Coming Soon'
    )
movie3= Movie(
    'M03','Jurassic Worldt','Adventure',124,'T18','English',96000.0,2026
    )
movie4= Movie(
    'M04','Interstellate','Sci-fi',169,'T16','English',75000.0,2025,'Ended'
    )
movie5= Movie(
    'M05','The Conjuring1','Horror', 112,'K','Japanese',99000.0,2026
    )
movies=[movie1, movie2, movie3, movie4, movie5]
for movie in movies:
    print('..................')
    movie.display_info()