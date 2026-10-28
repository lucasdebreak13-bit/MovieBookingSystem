
import os

from management import CinemaManager
from movie import Movie, VALID_RATINGS, VALID_STATUS
from showtime import Showtime

manager = CinemaManager()


# ============================ INPUT HELPERS ============================

def input_text(prompt, default=None):
    """nhập chuỗi có default thì enter để giữ giá trị cũ"""
    if default is not None:
        value = input(f'{prompt} [{default}]: ').strip()
        return value if value else str(default)
    while True:
        value = input(f'{prompt}: ').strip()
        if value:
            return value
        print('  -> This field cannot be empty.')


def input_int(prompt, default=None):
    while True:
        value = input_text(prompt, default)
        try:
            return int(value)
        except ValueError:
            print('  -> Please enter an integer.')


def input_float(prompt, default=None):
    while True:
        value = input_text(prompt, default)
        try:
            return float(value)
        except ValueError:
            print('  -> Please enter a number.')


def input_choice(title, options):
    """options: list (key, label). Trả về key được chọn, Enter = lựa chọn đầu tiên."""
    print(title + '   ' + '   '.join(f'{i}. {label}' for i, (_, label) in enumerate(options, 1)))
    while True:
        value = input('Choose [1]: ').strip() or '1'
        if value.isdigit() and 1 <= int(value) <= len(options):
            return options[int(value) - 1][0]
        print(f'  -> Please enter a number from 1 to {len(options)}.')


def input_order():
    """hỏi thứ tự sắp xếp, trả về True nếu giảm dần"""
    return input_choice('Order:', [(False, 'Ascending'), (True, 'Descending')])


def pause():
    input('\nPress Enter to continue...')


# ============================== DISPLAY ================================

def print_movies(rows):
    if not rows:
        print('  (no movies)')
        return
    print(f"{'ID':<5}{'Title':<22}{'Genre':<12}{'Min':>5}  {'Rating':<7}"
          f"{'Language':<12}{'Price':>10}  {'Year':<6}{'Status'}")
    print('-' * 95)
    for r in rows:
        print(f"{r['movie_id']:<5}{r['title'][:21]:<22}{r['genre'][:11]:<12}{r['duration']:>5}  "
              f"{r['age_rating']:<7}{r['language'][:11]:<12}{r['ticket_price']:>10,.0f}  "
              f"{r['release_year']:<6}{r['status']}")


def print_showtimes(rows):
    if not rows:
        print('  (no showtimes)')
        return
    print(f"{'ID':<5}{'Movie':<24}{'Room':<6}{'Date':<12}{'Time':<7}{'Price':>10}  {'Free'}")
    print('-' * 72)
    for r in rows:
        free = len(manager.get_available_seats(r['showtime_id']))
        print(f"{r['showtime_id']:<5}{(r['movie_id'] + ' ' + r['title'])[:23]:<24}{r['room']:<6}"
              f"{r['show_date']:<12}{r['show_time']:<7}{r['ticket_price']:>10,.0f}  {free}/50")


def print_bookings(rows):
    if not rows:
        print('  (no bookings)')
        return
    print(f"{'ID':<6}{'Show':<6}{'Movie':<20}{'Room':<6}{'Customer':<16}{'Phone':<12}"
          f"{'Booked on':<12}{'Total':>11}  {'Status'}")
    print('-' * 100)
    for r in rows:
        print(f"{r['booking_id']:<6}{r['showtime_id']:<6}{r['title'][:19]:<20}{r['room']:<6}"
              f"{r['customer_name'][:15]:<16}{r['phone']:<12}{r['booking_date']:<12}"
              f"{r['total_price']:>11,.0f}  {r['status']}")


# ============================== MOVIE MENU =============================

def menu_movie():
    while True:
        print('\n========== MOVIES ==========')
        print('1. View all movies')
        print('2. Sort movies (by title / price / duration, ascending or descending)')
        print('3. Search movies (by ID / title / genre)')
        print('4. Add movie')
        print('5. Update movie')
        print('6. Delete movie')
        print('0. Back')
        choice = input('Choose: ').strip()
        try:
            if choice == '1':
                print_movies(manager.get_movies())
            elif choice == '2':
                by = input_choice('Sort by:', [('title', 'Title'), ('price', 'Ticket price'),
                                               ('duration', 'Duration')])
                print_movies(manager.sort_movies(by, input_order()))
            elif choice == '3':
                field = input_choice('Search by:', [('all', 'ID / Title / Genre'), ('id', 'Movie ID'),
                                                    ('title', 'Title'), ('genre', 'Genre')])
                print_movies(manager.search_movies(input_text('Keyword'), field))
            elif choice == '4':
                add_movie()
            elif choice == '5':
                update_movie()
            elif choice == '6':
                movie_id = input_text('Movie ID to delete')
                if input(f'Delete {movie_id}? (y/n): ').strip().lower() == 'y':
                    manager.delete_movie(movie_id)
                    print('Deleted!')
            elif choice == '0':
                return
            else:
                print('Invalid choice.')
                continue
        except ValueError as e:
            print('Error:', e)
        pause()


def add_movie():
    movie_id = input_text('Movie ID', manager.new_movie_id())
    movie = Movie(
        movie_id,
        input_text('Title'),
        input_text('Genre'),
        input_int('Duration (minutes)'),
        input_text(f'Age rating {VALID_RATINGS}').upper(),
        input_text('Language'),
        input_float('Ticket price (VND)'),
        input_int('Release year'),
        input_text(f'Status {VALID_STATUS}', 'Now Showing'),
    )
    manager.add_movie(movie)
    print('Added:', movie)


def update_movie():
    row = manager.find_movie(input_text('Movie ID to update'))
    print('(Press Enter to keep the current value)')
    movie = Movie(
        row['movie_id'],
        input_text('Title', row['title']),
        input_text('Genre', row['genre']),
        input_int('Duration (minutes)', row['duration']),
        input_text(f'Age rating {VALID_RATINGS}', row['age_rating']).upper(),
        input_text('Language', row['language']),
        input_float('Ticket price (VND)', row['ticket_price']),
        input_int('Release year', row['release_year']),
        input_text(f'Status {VALID_STATUS}', row['status']),
    )
    manager.update_movie(movie)
    print('Updated:', movie)


# ============================ SHOWTIME MENU ============================

def menu_showtime():
    while True:
        print('\n========== SHOWTIMES ==========')
        print('1. View all showtimes')
        print('2. View showtimes of a movie')
        print('3. View seat map')
        print('4. Add showtime')
        print('5. Delete showtime')
        print('6. Update showtime')
        print('7. Sort showtimes (by date / title / price, ascending or descending)')
        print('0. Back')
        choice = input('Choose: ').strip()
        try:
            if choice == '1':
                print_showtimes(manager.get_showtimes())
            elif choice == '2':
                print_showtimes(manager.get_showtimes(input_text('Movie ID')))
            elif choice == '3':
                show_seat_map(input_text('Showtime ID'))
            elif choice == '4':
                add_showtime()
            elif choice == '5':
                manager.delete_showtime(input_text('Showtime ID to delete'))
                print('Deleted!')
            elif choice == '6':
                update_showtime()
            elif choice == '7':
                by = input_choice('Sort by:', [('date', 'Date & time'), ('title', 'Movie title'),
                                               ('price', 'Ticket price')])
                print_showtimes(manager.sort_showtimes(by, input_order()))
            elif choice == '0':
                return
            else:
                print('Invalid choice.')
                continue
        except ValueError as e:
            print('Error:', e)
        pause()


def show_seat_map(showtime_id):
    for line in manager.get_seat_map(showtime_id):
        print(line)
    print('[ X ] = booked')


def add_showtime():
    movie = manager.find_movie_for_showtime(input_text('Movie ID'))
    print(f"Movie: {movie['title']} - default price {movie['ticket_price']:,.0f} VND")
    showtime = Showtime(
        input_text('Showtime ID', manager.new_showtime_id()),
        movie['movie_id'],
        input_text('Room (e.g. R1)'),
        input_text('Date (YYYY-MM-DD)'),
        input_text('Time (HH:MM)'),
        input_float('Ticket price (VND)', movie['ticket_price']),
    )
    manager.add_showtime(showtime)
    print('Added:', showtime)


def update_showtime():
    old = manager.find_showtime_for_update(input_text('Showtime ID to update'))
    print('Current:', old)
    print('(Press Enter to keep the current value)')
    movie = manager.find_movie_for_showtime(input_text('Movie ID', old.movie_id))
    showtime = Showtime(
        old.showtime_id,
        movie['movie_id'],
        input_text('Room (e.g. R1)', old.room),
        input_text('Date (YYYY-MM-DD)', old.show_date),
        input_text('Time (HH:MM)', old.show_time),
        input_float('Ticket price (VND)', old.ticket_price),
        movie['title'],
    )
    manager.update_showtime(showtime)
    print('Updated:', manager.get_showtime_object(showtime.showtime_id))


# ============================= BOOKING MENU ============================

def menu_booking():
    while True:
        print('\n========== BOOKINGS ==========')
        print('1. Book tickets')
        print('2. View a booking')
        print('3. View all bookings')
        print('4. Change seats / number of tickets')
        print('5. Cancel booking')
        print('6. Sort bookings (by date / movie / total / customer, ascending or descending)')
        print('0. Back')
        choice = input('Choose: ').strip()
        try:
            if choice == '1':
                book_tickets()
            elif choice == '2':
                view_booking(input_text('Booking ID'))
            elif choice == '3':
                print_bookings(manager.get_all_bookings())
            elif choice == '4':
                change_seats()
            elif choice == '5':
                booking_id = input_text('Booking ID to cancel')
                if input(f'Cancel {booking_id}? (y/n): ').strip().lower() == 'y':
                    manager.cancel_booking(booking_id)
                    print('Cancelled! Seats are free again.')
            elif choice == '6':
                by = input_choice('Sort by:', [('date', 'Booking date'), ('title', 'Movie title'),
                                               ('total', 'Total price'), ('customer', 'Customer name')])
                print_bookings(manager.sort_bookings(by, input_order()))
            elif choice == '0':
                return
            else:
                print('Invalid choice.')
                continue
        except ValueError as e:
            print('Error:', e)
        pause()


def book_tickets():
    print_showtimes(manager.get_showtimes())
    showtime_id = input_text('Showtime ID')
    show_seat_map(showtime_id)
    seats = input_text('Seats (e.g. A1, A2)')
    name = input_text('Customer name')
    phone = input_text('Phone (10 digits)')
    booking_id, total = manager.book_tickets(showtime_id, name, phone, seats)
    print(f'Booked successfully! Booking ID: {booking_id} - Total: {total:,.0f} VND')


def view_booking(booking_id):
    row, seats = manager.get_booking(booking_id)
    print(f"Booking ID  : {row['booking_id']}")
    print(f"Movie       : {row['title']}")
    print(f"Showtime    : {row['showtime_id']} - {row['show_date']} {row['show_time']}")
    print(f"Room        : {row['room']}")
    print(f"Customer    : {row['customer_name']} ({row['phone']})")
    print(f"Booked on   : {row['booking_date']}")
    print(f"Seats       : {', '.join(seats) if seats else '-'}")
    print(f"Ticket price: {row['ticket_price']:,.0f} VND")
    print(f"Total       : {row['total_price']:,.0f} VND")
    print(f"Status      : {row['status']}")


def change_seats():
    booking_id = input_text('Booking ID')
    row, seats = manager.get_booking(booking_id)
    if row['status'] != 'Active':
        raise ValueError('This booking was cancelled')
    print('Current seats:', ', '.join(seats))
    show_seat_map(row['showtime_id'])
    print('(Your current seats are shown as [ X ] but you can choose them again)')
    total = manager.change_seats(booking_id, input_text('New seats (e.g. A1, A2, A3)'))
    print(f'Updated! New total: {total:,.0f} VND')


# ============================= REPORT MENU =============================

def menu_report():
    print('\n========== REVENUE BY MOVIE ==========')
    rows = manager.revenue_report()
    print(f"{'Movie':<25}{'Tickets':>8}{'Revenue (VND)':>16}")
    print('-' * 49)
    total_tickets, total_revenue = 0, 0
    for r in rows:
        print(f"{r['title'][:24]:<25}{r['tickets_sold']:>8}{r['revenue']:>16,.0f}")
        total_tickets += r['tickets_sold']
        total_revenue += r['revenue']
    print('-' * 49)
    print(f"{'TOTAL':<25}{total_tickets:>8}{total_revenue:>16,.0f}")
    pause()


def import_movies():
    default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'movies.txt')
    path = input_text('File path', default_path)
    try:
        added, skipped, errors = manager.import_movies_from_text(path)
    except ValueError as e:
        print('Error:', e)
    else:
        print(f'Added  : {len(added)} {added}')
        print(f'Skipped: {len(skipped)} (ID already exists) {skipped}')
        print(f'Errors : {len(errors)}')
        for err in errors:
            print('   ', err)
    pause()


# ================================= MAIN ================================

def main():
    while True:
        print('\n======== MOVIE TICKET BOOKING SYSTEM ========')
        print('1. Movies')
        print('2. Showtimes')
        print('3. Bookings')
        print('4. Revenue report')
        print('5. Export data to text files')
        print('6. Import movies from text file')
        print('0. Exit')
        choice = input('Choose: ').strip()
        if choice == '1':
            menu_movie()
        elif choice == '2':
            menu_showtime()
        elif choice == '3':
            menu_booking()
        elif choice == '4':
            menu_report()
        elif choice == '5':
            for path in manager.export_to_text():
                print('Saved:', path)
            pause()
        elif choice == '6':
            import_movies()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Invalid choice.')


if __name__ == '__main__':
    main()
