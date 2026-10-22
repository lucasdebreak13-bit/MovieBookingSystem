
import os
import sqlite3
from datetime import date, datetime, timedelta

import database as db
from movie import Movie
from showtime import Showtime
from booking import Booking


CLEANING_MINUTES = 15   # thời gian dọn phòng giữa 2 suất chiếu


class CinemaManager:
    def __init__(self):
        db.init_db()

    # ============================== MOVIE ==============================

    def get_movies(self, sort_by='movie_id'):
        return db.get_all_movies(sort_by)

    def search_movies(self, keyword):
        return db.search_movies(keyword.strip())

    def find_movie(self, movie_id):
        row = db.get_movie(movie_id.strip().upper())
        if row is None:
            raise ValueError(f'Movie {movie_id} not found')
        return row

    def new_movie_id(self):
        return db.next_id('movies', 'movie_id', 'M', 2)

    def add_movie(self, movie):
        if db.get_movie(movie.movie_id) is not None:
            raise ValueError(f'Movie ID {movie.movie_id} already exists')
        db.add_movie(movie)

    def update_movie(self, movie):
        if not db.update_movie(movie):
            raise ValueError(f'Movie {movie.movie_id} not found')

    def delete_movie(self, movie_id):
        movie_id = movie_id.strip().upper()
        if db.get_showtimes(movie_id):
            raise ValueError('Cannot delete: this movie still has showtimes')
        if not db.delete_movie(movie_id):
            raise ValueError(f'Movie {movie_id} not found')

    @staticmethod
    def row_to_movie(row):
        """chuyển 1 dòng trong database thành object movie (để sửa phim)"""
        return Movie(row['movie_id'], row['title'], row['genre'], row['duration'],
                     row['age_rating'], row['language'], row['ticket_price'],
                     row['release_year'], row['status'])

    # ============================= SHOWTIME ============================

    def get_showtimes(self, movie_id=None):
        return db.get_showtimes(movie_id.strip().upper() if movie_id else None)

    def find_showtime(self, showtime_id):
        row = db.get_showtime(showtime_id.strip().upper())
        if row is None:
            raise ValueError(f'Showtime {showtime_id} not found')
        return row

    def new_showtime_id(self):
        return db.next_id('showtimes', 'showtime_id', 'S', 2)

    def find_movie_for_showtime(self, movie_id):
        """phim phải tồn tại và chưa 'Ended' thì mới tạo suất chiếu được"""
        movie = self.find_movie(movie_id)
        if movie['status'] == 'Ended':
            raise ValueError('Cannot create showtime for an ended movie')
        return movie

    @staticmethod
    def _start_end(show_date, show_time, duration):
        """tính giờ bắt đầu và giờ phòng trống lại (hết phim + dọn phòng)"""
        start = datetime.strptime(f'{show_date} {show_time}', '%Y-%m-%d %H:%M')
        end = start + timedelta(minutes=duration + CLEANING_MINUTES)
        return start, end

    def add_showtime(self, showtime):
        movie = self.find_movie_for_showtime(showtime.movie_id)
        if db.get_showtime(showtime.showtime_id) is not None:
            raise ValueError(f'Showtime ID {showtime.showtime_id} already exists')

        new_start, new_end = self._start_end(showtime.show_date, showtime.show_time,
                                             movie['duration'])
        # không tạo suất chiếu trong quá khứ
        if new_start <= datetime.now():
            raise ValueError('Cannot create a showtime in the past')

        # không trùng lịch trong cùng phòng (tính cả thời lượng phim + dọn phòng)
        for other in db.get_showtimes_in_room(showtime.room):
            old_start, old_end = self._start_end(other['show_date'], other['show_time'],
                                                 other['duration'])
            if new_start < old_end and old_start < new_end:   # 2 khoảng thời gian giao nhau
                raise ValueError(
                    f"Room {showtime.room} is busy: {other['showtime_id']} "
                    f"({other['title']}) runs {old_start:%Y-%m-%d %H:%M} - {old_end:%H:%M} "
                    f"(incl. {CLEANING_MINUTES} min cleaning)")
        try:
            db.add_showtime(showtime)
        except sqlite3.IntegrityError:
            raise ValueError(f'Room {showtime.room} already has a show at '
                             f'{showtime.show_date} {showtime.show_time}')

    def delete_showtime(self, showtime_id):
        showtime_id = showtime_id.strip().upper()
        if db.get_booked_seats(showtime_id):
            raise ValueError('Cannot delete: this showtime already has bookings')
        if not db.delete_showtime(showtime_id):
            raise ValueError(f'Showtime {showtime_id} not found')

    def get_available_seats(self, showtime_id):
        self.find_showtime(showtime_id)
        return db.get_available_seats(showtime_id.strip().upper())

    def get_seat_map(self, showtime_id):
        """trả về list các dòng chữ của sơ đồ ghế, ghế đã đặt là [ X ]"""
        st = self.find_showtime(showtime_id)
        booked = db.get_booked_seats(st['showtime_id'])
        lines = ['=' * 25 + ' SCREEN ' + '=' * 26]
        for row in db.SEAT_ROWS:
            cells = []
            for col in range(1, db.SEATS_PER_ROW + 1):
                code = f'{row}{col}'
                if code in booked:
                    cells.append('[ X ]')
                else:
                    cells.append(f'[{code:^3}]')   # căn giữa 3 ký tự: [A1 ] / [A10]
            lines.append(' '.join(cells))
        return lines

    # ============================== BOOKING ============================

    def book_tickets(self, showtime_id, customer_name, phone, seats):
        """trả về (booking_id, total)."""
        st = self.find_showtime(showtime_id)
        booking = Booking(db.next_id('bookings', 'booking_id', 'B', 3),
                          st['showtime_id'], customer_name, phone, seats)
        taken = [s for s in booking.seats if s in db.get_booked_seats(st['showtime_id'])]
        if taken:
            raise ValueError(f'Seat(s) already booked: {", ".join(taken)}')
        total = db.create_booking(booking.booking_id, booking.showtime_id,
                                  booking.customer_name, booking.phone,
                                  str(date.today()), booking.seats)
        return booking.booking_id, total

    def get_booking(self, booking_id):
        row, seats = db.get_booking(booking_id.strip().upper())
        if row is None:
            raise ValueError(f'Booking {booking_id} not found')
        return row, seats

    def get_all_bookings(self):
        return db.get_all_bookings()

    def change_seats(self, booking_id, new_seats):
        row, _ = self.get_booking(booking_id)
        # dùng booking để kiểm tra danh sách ghế mới hợp lệ
        checked = Booking(row['booking_id'], row['showtime_id'],
                          row['customer_name'], row['phone'], new_seats)
        return db.change_booking_seats(checked.booking_id, checked.seats)

    def cancel_booking(self, booking_id):
        if not db.cancel_booking(booking_id.strip().upper()):
            raise ValueError('Booking not found or already cancelled')

    # ============================== REPORT =============================

    def revenue_report(self):
        return db.revenue_by_movie()

    def import_movies_from_text(self, path):
        """
        đọc phim từ file .txt (cùng định dạng với file export):
            dòng 1: movie_id|title|genre|duration|age_rating|language|ticket_price|release_year|status
            các dòng sau: M01|Avatar 10|Sci-fi|192|T13|English|80000|2026|Now Showing
        mỗi dòng đi qua class Movie để kiểm tra trả về (added, skipped, errors)
        """
        if not os.path.exists(path):
            raise ValueError(f'File not found: {path}')
        added, skipped, errors = [], [], []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        for number, line in enumerate(lines, start=1):
            line = line.strip()
            if line == '' or line.startswith('movie_id'):   # bỏ dòng trống và dòng tiêu đề
                continue
            parts = [p.strip() for p in line.split('|')]
            try:
                if len(parts) != 9:
                    raise ValueError(f'expected 9 fields, got {len(parts)}')
                try:
                    duration = int(parts[3])
                    price = float(parts[6])
                    year = int(parts[7])
                except ValueError:
                    raise ValueError('duration, ticket_price and release_year must be numbers')
                movie = Movie(parts[0], parts[1], parts[2], duration, parts[4],
                              parts[5], price, year, parts[8])
                if db.get_movie(movie.movie_id) is not None:
                    skipped.append(movie.movie_id)
                    continue
                db.add_movie(movie)
                added.append(movie.movie_id)
            except ValueError as e:      # int()/float() sai hoặc Movie báo lỗi
                errors.append(f'Line {number}: {e}')
        return added, skipped, errors

    def export_to_text(self, folder=None):
        """xuất 3 bảng ra file .txt """
        folder = folder or os.path.dirname(db.DB_PATH)
        os.makedirs(folder, exist_ok=True)
        files = {
            'movies.txt': db.get_all_movies(),
            'showtimes.txt': db.get_showtimes(),
            'bookings.txt': db.get_all_bookings(),
        }
        for name, rows in files.items():
            with open(os.path.join(folder, name), 'w', encoding='utf-8') as f:
                if rows:
                    f.write('|'.join(rows[0].keys()) + '\n')
                for r in rows:
                    f.write('|'.join(str(v) for v in r) + '\n')
        return [os.path.join(folder, n) for n in files]
