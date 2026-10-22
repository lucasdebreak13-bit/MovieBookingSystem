from datetime import datetime


class Showtime:
    def __init__(self, showtime_id, movie_id, room, show_date, show_time, ticket_price):
        # gán qua setter -> mỗi thuộc tính được kiểm tra ở property bên dưới
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.room = room
        self.show_date = show_date
        self.show_time = show_time
        self.ticket_price = ticket_price

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

    def __str__(self):
        return (f'{self.showtime_id} | Movie: {self.movie_id} | Room: {self.room} | '
                f'{self.show_date} {self.show_time} | {self.ticket_price:,.0f} VND')


if __name__ == '__main__':
    s = Showtime('S01', 'M01', 'R1', '2026-10-25', '19:30', 90000)
    print(s)

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
