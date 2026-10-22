SEAT_ROWS = 'ABCDE'      # 5 hàng ghế (giống database.py)
SEATS_PER_ROW = 10       # mỗi hàng 10 ghế -> A1..E10


class Booking:
    def __init__(self, booking_id, showtime_id, customer_name, phone, seats):
        self.booking_id = booking_id
        self.showtime_id = showtime_id
        self.customer_name = customer_name
        self.phone = phone
        self.seats = seats

    @staticmethod
    def _check_text(value, field):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{field} cannot be empty')
        return value.strip()

    @property
    def booking_id(self):
        return self._booking_id

    @booking_id.setter
    def booking_id(self, value):
        self._booking_id = self._check_text(value, 'Booking ID').upper()

    @property
    def showtime_id(self):
        return self._showtime_id

    @showtime_id.setter
    def showtime_id(self, value):
        self._showtime_id = self._check_text(value, 'Showtime ID').upper()

    @property
    def customer_name(self):
        return self._customer_name

    @customer_name.setter
    def customer_name(self, value):
        self._customer_name = self._check_text(value, 'Customer name')

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        value = self._check_text(value, 'Phone')
        # sdt VN 10 chữ số bắt đầu bằng 0
        if not value.isdigit() or len(value) != 10 or value[0] != '0':
            raise ValueError('Phone must be 10 digits and start with 0')
        self._phone = value

    @property
    def seats(self):
        return self._seats

    @seats.setter
    def seats(self, value):
        """value có thể là list ['A1', 'A2'] hoặc chuỗi 'A1, a2'"""
        if isinstance(value, str):
            value = value.split(',')
        seats = []
        for seat in value:
            seat = seat.strip().upper()
            if seat == '':
                continue
            if not Booking.is_valid_seat(seat):
                raise ValueError(f'Seat {seat} does not exist (valid: A1..E10)')
            if seat in seats:
                raise ValueError(f'Seat {seat} is entered twice')
            seats.append(seat)
        if len(seats) == 0:
            raise ValueError('Please choose at least 1 seat')
        self._seats = seats

    @staticmethod
    def is_valid_seat(seat):
        if len(seat) < 2 or seat[0] not in SEAT_ROWS or not seat[1:].isdigit():
            return False
        return 1 <= int(seat[1:]) <= SEATS_PER_ROW

    @property
    def number_of_tickets(self):
        return len(self.seats)

    def calculate_total(self, ticket_price):
        return self.number_of_tickets * ticket_price

    def __str__(self):
        return (f'{self.booking_id} | Showtime: {self.showtime_id} | '
                f'{self.customer_name} ({self.phone}) | Seats: {", ".join(self.seats)}')


if __name__ == '__main__':
    b = Booking('B001', 'S01', 'Khoa', '0901234567', 'a1, A2')
    print(b)
    print('Total:', f'{b.calculate_total(90000):,.0f} VND')

    tests = [
        ('B002', 'S01', 'Khoa', '12345', 'A1'),         # sđt sai
        ('B002', 'S01', 'Khoa', '0901234567', 'F1'),    # ghế không tồn tại
        ('B002', 'S01', 'Khoa', '0901234567', 'A1,A1'), # ghế trùng
        ('B002', 'S01', '', '0901234567', 'A1'),        # tên rỗng
    ]
    for data in tests:
        try:
            Booking(*data)
        except ValueError as e:
            print('Caught error:', e)
