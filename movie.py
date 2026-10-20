VALID_RATINGS = ['P', 'K', 'T13', 'T16', 'T18']
VALID_STATUS = ['Now Showing', 'Coming Soon', 'Ended']


class Movie:
    def __init__(self, movie_id, title, genre, duration, age_rating,
                 language, ticket_price, release_year, status='Now Showing'):
        # SỬA: gán qua setter -> việc kiểm tra nằm ở 1 chỗ duy nhất (property bên dưới)
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.duration = duration
        self.age_rating = age_rating
        self.language = language
        self.ticket_price = ticket_price
        self.release_year = release_year
        self.status = status

    # SỬA: hàm phụ kiểm tra chuỗi rỗng, dùng lại cho nhiều thuộc tính
    @staticmethod
    def _check_text(value, field):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{field} cannot be empty')
        return value.strip()

    @property
    def movie_id(self):
        return self._movie_id

    @movie_id.setter
    def movie_id(self, value):
        self._movie_id = self._check_text(value, 'Movie ID').upper()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = self._check_text(value, 'Title')

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = self._check_text(value, 'Genre')

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = self._check_text(value, 'Language')

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if type(value) is not int or value <= 0:
            raise ValueError('Duration must be a positive integer')
        self._duration = value

    @property
    def age_rating(self):
        return self._age_rating

    @age_rating.setter
    def age_rating(self, value):
        if value not in VALID_RATINGS:
            raise ValueError(f'Age rating must be one of {VALID_RATINGS}')
        self._age_rating = value

    @property
    def ticket_price(self):
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, value):
        if type(value) not in (int, float) or value < 0:
            raise ValueError('Ticket price cannot be negative')
        self._ticket_price = float(value)

    @property
    def release_year(self):
        return self._release_year

    @release_year.setter
    def release_year(self, value):
        if type(value) is not int or value < 1888:
            raise ValueError('Invalid release year')
        self._release_year = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in VALID_STATUS:
            raise ValueError(f'Status must be one of {VALID_STATUS}')
        self._status = value

    def display_info(self):
        # SỬA: thêm dấu ':' cho đồng bộ giá có dấu phẩy ngăn cách
        print('Movie ID    :', self.movie_id)
        print('Title       :', self.title)
        print('Genre       :', self.genre)
        print('Duration    :', self.duration, 'minutes')
        print('Age rating  :', self.age_rating)
        print('Language    :', self.language)
        print(f'Ticket price: {self.ticket_price:,.0f} VND')
        print('Release year:', self.release_year)
        print('Status      :', self.status)

    def __str__(self):
        return f'{self.movie_id} - {self.title} - {self.genre} - {self.ticket_price:,.0f} VND'


# SỬA: code test chỉ chạy khi mở trực tiếp file này, KHÔNG chạy khi file khác import
if __name__ == '__main__':
    movies = [
        Movie('M01', 'Avatar 10', 'Sci-fi', 192, 'T13', 'English', 80000.0, 2026),
        Movie('M02', 'Cyberfun 2099', 'Animation', 110, 'P', 'Vietnamese', 120000.0, 2099, 'Coming Soon'),
    ]
    for m in movies:
        print('-' * 20)
        m.display_info()

    # Thử dữ liệu sai setter phải báo lỗi chứ không crash
    try:
        Movie('', 'X', 'Y', 100, 'P', 'EN', 1000, 2026)
    except ValueError as e:
        print('Bắt được lỗi:', e)