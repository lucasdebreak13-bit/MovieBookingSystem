
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cinema.db")

SEAT_ROWS = "ABCDE"     # 5 hàng ghế
SEATS_PER_ROW = 10      # mỗi hàng 10 ghế -> A1..E10


def get_connection():
    """Mở kết nối tới file database (tự tạo thư mục data/ nếu chưa có)."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # truy cập cột bằng tên: row["title"]
    conn.execute("PRAGMA foreign_keys = ON")  # bật kiểm tra khoá ngoại
    return conn


def init_db():
    """Tạo 4 bảng nếu chưa tồn tại. Gọi 1 lần khi chương trình khởi động."""
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id     TEXT PRIMARY KEY,
            title        TEXT NOT NULL,
            genre        TEXT NOT NULL,
            duration     INTEGER NOT NULL CHECK (duration > 0),
            age_rating   TEXT NOT NULL,
            language     TEXT NOT NULL,
            ticket_price REAL NOT NULL CHECK (ticket_price >= 0),
            release_year INTEGER NOT NULL,
            status       TEXT NOT NULL DEFAULT 'Now Showing'
        );

        CREATE TABLE IF NOT EXISTS showtimes (
            showtime_id  TEXT PRIMARY KEY,
            movie_id     TEXT NOT NULL REFERENCES movies(movie_id),
            room         TEXT NOT NULL,
            show_date    TEXT NOT NULL,          -- 'YYYY-MM-DD'
            show_time    TEXT NOT NULL,          -- 'HH:MM'
            ticket_price REAL NOT NULL CHECK (ticket_price >= 0),
            UNIQUE (room, show_date, show_time)  -- 1 phòng không chiếu 2 suất cùng giờ
        );

        CREATE TABLE IF NOT EXISTS bookings (
            booking_id    TEXT PRIMARY KEY,
            showtime_id   TEXT NOT NULL REFERENCES showtimes(showtime_id),
            customer_name TEXT NOT NULL,
            phone         TEXT NOT NULL,
            booking_date  TEXT NOT NULL,
            total_price   REAL NOT NULL,
            status        TEXT NOT NULL DEFAULT 'Active'   -- Active / Cancelled
        );

        -- Mỗi dòng = 1 ghế của 1 booking.
        -- UNIQUE(showtime_id, seat_code): database tự chặn đặt trùng ghế.
        CREATE TABLE IF NOT EXISTS booking_seats (
            booking_id  TEXT NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
            showtime_id TEXT NOT NULL REFERENCES showtimes(showtime_id),
            seat_code   TEXT NOT NULL,
            UNIQUE (showtime_id, seat_code)
        );
        """)


# ============================== MOVIES ==============================

def add_movie(m):
    """m là object Movie. Báo lỗi nếu trùng movie_id."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (m.movie_id, m.title, m.genre, m.duration, m.age_rating,
             m.language, m.ticket_price, m.release_year, m.status),
        )


def get_all_movies(order_by="movie_id"):
    allowed = {"movie_id", "title", "ticket_price", "duration"}  # chống SQL injection
    if order_by not in allowed:
        order_by = "movie_id"
    with get_connection() as conn:
        return conn.execute(f"SELECT * FROM movies ORDER BY {order_by}").fetchall()


def get_movie(movie_id):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM movies WHERE movie_id = ?", (movie_id,)).fetchone()


def search_movies(keyword):
    """Tìm theo tên HOẶC thể loại, không phân biệt hoa thường."""
    like = f"%{keyword}%"
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM movies WHERE title LIKE ? OR genre LIKE ?", (like, like)
        ).fetchall()


def update_movie(m):
    with get_connection() as conn:
        cur = conn.execute(
            """UPDATE movies SET title=?, genre=?, duration=?, age_rating=?, language=?,
                   ticket_price=?, release_year=?, status=? WHERE movie_id=?""",
            (m.title, m.genre, m.duration, m.age_rating, m.language,
             m.ticket_price, m.release_year, m.status, m.movie_id),
        )
        return cur.rowcount == 1   # True nếu có phim để sửa


def delete_movie(movie_id):
    """Không cho xoá phim đã có suất chiếu (khoá ngoại sẽ báo lỗi)."""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM movies WHERE movie_id = ?", (movie_id,))
        return cur.rowcount == 1


# ============================= SHOWTIMES ============================

def add_showtime(s):
    """s là object Showtime (có movie_id, KHÔNG lưu title)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO showtimes VALUES (?, ?, ?, ?, ?, ?)",
            (s.showtime_id, s.movie_id, s.room, s.show_date, s.show_time, s.ticket_price),
        )


def get_showtimes(movie_id=None):
    """Lấy suất chiếu kèm tên phim (JOIN). Có thể lọc theo phim."""
    sql = """SELECT s.*, m.title FROM showtimes s
             JOIN movies m ON m.movie_id = s.movie_id"""
    params = ()
    if movie_id:
        sql += " WHERE s.movie_id = ?"
        params = (movie_id,)
    sql += " ORDER BY s.show_date, s.show_time"
    with get_connection() as conn:
        return conn.execute(sql, params).fetchall()


def get_showtime(showtime_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM showtimes WHERE showtime_id = ?", (showtime_id,)
        ).fetchone()


def delete_showtime(showtime_id):
    """Không cho xoá suất chiếu đã có người đặt (khoá ngoại sẽ báo lỗi)."""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM showtimes WHERE showtime_id = ?", (showtime_id,))
        return cur.rowcount == 1


def all_seat_codes():
    return [f"{r}{c}" for r in SEAT_ROWS for c in range(1, SEATS_PER_ROW + 1)]


def get_booked_seats(showtime_id):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT seat_code FROM booking_seats WHERE showtime_id = ?", (showtime_id,)
        ).fetchall()
    return {row["seat_code"] for row in rows}


def get_available_seats(showtime_id):
    booked = get_booked_seats(showtime_id)
    return [seat for seat in all_seat_codes() if seat not in booked]


# ============================== BOOKINGS ============================

def create_booking(booking_id, showtime_id, customer_name, phone, booking_date, seats):
    """
    Đặt vé cho danh sách ghế. Dùng TRANSACTION:
    nếu 1 ghế lỗi (trùng/không tồn tại) thì KHÔNG ghế nào được lưu.
    Trả về tổng tiền.
    """
    st = get_showtime(showtime_id)
    if st is None:
        raise ValueError("Showtime does not exist")
    valid = set(all_seat_codes())
    for seat in seats:
        if seat not in valid:
            raise ValueError(f"Seat {seat} does not exist")
    total = st["ticket_price"] * len(seats)

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?, 'Active')",
            (booking_id, showtime_id, customer_name, phone, booking_date, total),
        )
        for seat in seats:
            conn.execute("INSERT INTO booking_seats VALUES (?, ?, ?)",
                         (booking_id, showtime_id, seat))
        conn.commit()
        return total
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise ValueError(f"Booking failed (seat already taken or duplicate ID): {e}")
    finally:
        conn.close()


def get_booking(booking_id):
    with get_connection() as conn:
        b = conn.execute("SELECT * FROM bookings WHERE booking_id = ?", (booking_id,)).fetchone()
        if b is None:
            return None, []
        seats = [r["seat_code"] for r in conn.execute(
            "SELECT seat_code FROM booking_seats WHERE booking_id = ?", (booking_id,))]
        return b, seats


def get_all_bookings():
    with get_connection() as conn:
        return conn.execute("""
            SELECT b.*, m.title, s.show_date, s.show_time
            FROM bookings b
            JOIN showtimes s ON s.showtime_id = b.showtime_id
            JOIN movies m    ON m.movie_id = s.movie_id
            ORDER BY b.booking_id
        """).fetchall()


def change_booking_seats(booking_id, new_seats):
    """
    Đổi ghế / đổi số lượng vé của 1 booking đang Active.
    Dùng TRANSACTION: lỗi thì giữ nguyên ghế cũ. Trả về tổng tiền mới.
    """
    conn = get_connection()
    try:
        b = conn.execute("SELECT * FROM bookings WHERE booking_id = ? AND status = 'Active'",
                         (booking_id,)).fetchone()
        if b is None:
            raise ValueError("Booking not found or already cancelled")
        price = conn.execute("SELECT ticket_price FROM showtimes WHERE showtime_id = ?",
                             (b["showtime_id"],)).fetchone()["ticket_price"]
        conn.execute("DELETE FROM booking_seats WHERE booking_id = ?", (booking_id,))
        for seat in new_seats:
            conn.execute("INSERT INTO booking_seats VALUES (?, ?, ?)",
                         (booking_id, b["showtime_id"], seat))
        total = price * len(new_seats)
        conn.execute("UPDATE bookings SET total_price = ? WHERE booking_id = ?", (total, booking_id))
        conn.commit()
        return total
    except sqlite3.IntegrityError:
        conn.rollback()
        raise ValueError("Some seats are already taken by another booking")
    finally:
        conn.close()


def cancel_booking(booking_id):
    """Huỷ vé: đổi trạng thái + xoá ghế -> ghế được trả lại tự động."""
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE bookings SET status='Cancelled', total_price=0 "
            "WHERE booking_id=? AND status='Active'", (booking_id,))
        conn.execute("DELETE FROM booking_seats WHERE booking_id = ?", (booking_id,))
        return cur.rowcount == 1


# ============================= UTILS ================================

def next_id(table, column, prefix, width):
    """Sinh mã tiếp theo, vd next_id('bookings', 'booking_id', 'B', 3) -> 'B004'."""
    allowed = {("movies", "movie_id"), ("showtimes", "showtime_id"), ("bookings", "booking_id")}
    if (table, column) not in allowed:
        raise ValueError("Invalid table/column")
    with get_connection() as conn:
        rows = conn.execute(f"SELECT {column} FROM {table}").fetchall()
    numbers = [int(r[0][len(prefix):]) for r in rows
               if r[0].startswith(prefix) and r[0][len(prefix):].isdigit()]
    return f"{prefix}{max(numbers, default=0) + 1:0{width}d}"


# ============================= REPORT ===============================

def revenue_by_movie():
    """Thống kê doanh thu & số vé theo phim (điểm cộng khi demo)."""
    with get_connection() as conn:
        return conn.execute("""
            SELECT m.title,
                   COUNT(bs.seat_code)        AS tickets_sold,
                   COALESCE(SUM(CASE WHEN bs.seat_code IS NOT NULL
                                     THEN s.ticket_price END), 0) AS revenue
            FROM movies m
            LEFT JOIN showtimes s      ON s.movie_id = m.movie_id
            LEFT JOIN booking_seats bs ON bs.showtime_id = s.showtime_id
            GROUP BY m.movie_id
            ORDER BY revenue DESC
        """).fetchall()


if __name__ == "__main__":
    init_db()
    print("Database ready at:", DB_PATH)
