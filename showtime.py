from datetime import datetime

SEAT_ROWS = 'ABCDE'      # 5 hàng ghế (giống database.py)
SEATS_PER_ROW = 10       # mỗi hàng 10 ghế -> A1..E10
ALL_SEATS = [f'{r}{c}' for r in SEAT_ROWS for c in range(1, SEATS_PER_ROW + 1)]


class Showtime:
    def __init__(self, showtime_id, movie_id, room, show_date, show_time, ticket_price,
                 title='', available_seats=None):
        # gán qua setter -> mỗi thuộc tính được kiểm tra ở property bên dưới
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.room = room
        self.show_date = show_date
        self.show_time = show_time
        self.ticket_price = ticket_price
        self.title = title                      # tên phim (tuần 5)
        self.available_seats = available_seats  # vị trí ghế khả dụng (tuần 5)

    @staticmethod
    def _check_text(value, field):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{field} cannot be empty')
        return value.strip()

    @property
    def showtime_id(self):
        return self._showtime_id

    @showtime_id.setter
    def showtime_id(self, value):
        self._showtime_id = self._check_text(value, 'Showtime ID').upper()

    @property
    def movie_id(self):
        return self._movie_id

    @movie_id.setter
    def movie_id(self, value):
        self._movie_id = self._check_text(value, 'Movie ID').upper()

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, value):
        self._room = self._check_text(value, 'Room').upper()

    @property
    def show_date(self):
        return self._show_date

    @show_date.setter
    def show_date(self, value):
        value = self._check_text(value, 'Date')
        try:
            datetime.strptime(value, '%Y-%m-%d')   # quy ước: YYYY-MM-DD
        except ValueError:
            raise ValueError('Date must be in format YYYY-MM-DD (e.g. 2026-10-25)')
        self._show_date = value

    @property
    def show_time(self):
        return self._show_time

    @show_time.setter
    def show_time(self, value):
        value = self._check_text(value, 'Time')
        try:
            datetime.strptime(value, '%H:%M')      # quy ước: HH:MM 24 giờ
        except ValueError:
            raise ValueError('Time must be in format HH:MM (e.g. 19:30)')
        self._show_time = value

    @property
    def ticket_price(self):
        return self._ticket_price

    @ticket_price.setter
    def ticket_price(self, value):
        if type(value) not in (int, float) or value < 0:
            raise ValueError('Ticket price cannot be negative')
        self._ticket_price = float(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # tên phim không bắt buộc khi tạo (lấy từ Movie qua movie_id)
        if not isinstance(value, str):
            raise ValueError('Title must be text')
        self._title = value.strip()

    @property
    def available_seats(self):
        return self._available_seats

    @available_seats.setter
    def available_seats(self, value):
        # None = suất chiếu mới, còn trống toàn bộ 50 ghế
        if value is None:
            value = list(ALL_SEATS)
        for seat in value:
            if seat not in ALL_SEATS:
                raise ValueError(f'Seat {seat} does not exist')
        self._available_seats = list(value)

    @property
    def number_of_available_seats(self):
        return len(self.available_seats)

    def __str__(self):
        movie = f'{self.movie_id} {self.title}'.strip()
        return (f'{self.showtime_id} | Movie: {movie} | Room: {self.room} | '
                f'{self.show_date} {self.show_time} | {self.ticket_price:,.0f} VND | '
                f'Free: {self.number_of_available_seats}/{len(ALL_SEATS)}')


if __name__ == '__main__':
    s = Showtime('S01', 'M01', 'R1', '2026-10-25', '19:30', 90000, 'Avatar 10')
    print(s)
    s.available_seats = [x for x in ALL_SEATS if x not in ('A1', 'A2')]
    print('After booking A1, A2:', s.number_of_available_seats, 'seats free')

    tests = [
        ('S02', 'M01', 'R1', '25/10/2026', '19:30', 90000),   # sai định dạng ngày
        ('S02', 'M01', 'R1', '2026-10-25', '7pm', 90000),     # sai định dạng giờ
        ('S02', 'M01', 'R1', '2026-10-25', '19:30', -1),      # giá âm
        ('', 'M01', 'R1', '2026-10-25', '19:30', 90000),      # ID rỗng
    ]
    for data in tests:
        try:
            Showtime(*data)
        except ValueError as e:
            print('Caught error:', e)
