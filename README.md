# Movie Ticket Booking Management System

A console-based movie ticket booking management system developed in **Python** for the **PFP191 – Programming Fundamentals with Python** course.

> **Project status:** Completed for Week 7 – all planned features (Weeks 4–7) are implemented and tested.

## 1. Project objectives

This project helps users manage movie information, screening schedules, and ticket bookings. It also gives our team practice with:

- Object-Oriented Programming (OOP)
- Lists and dictionaries
- Input validation and exception handling
- Reading and writing text files
- Modular programming and teamwork using GitHub

## 2. Features

### Movie (Week 5)
- `Movie` class: movie ID, title, genre, age rating, duration, language, ticket price, release year, status
- Add, update and delete movies (a movie that still has showtimes cannot be deleted)
- **Search** by movie ID, title or genre
- **Sort** by title, ticket price or duration – ascending or descending
- Import movies from a text file (`movies.txt`)

### Showtime (Week 5)
- `Showtime` class: showtime ID, movie (ID + title), room, date, time, ticket price, available seats
- Add, **update** and delete showtimes (a showtime that already has bookings cannot be updated or deleted)
- Prevent schedule conflicts in the same room (movie duration + 15 minutes cleaning)
- Prevent creating showtimes in the past
- Seat map (5 rows × 10 seats) showing booked seats
- **Sort** by date & time, movie title or ticket price – ascending or descending

### Booking / Ticket purchase (Week 5)
- `Booking` class: booking ID, showtime, customer name, phone, seats, ticket price, room number, booking date
- Book tickets, prevent double-booking of a seat
- Update a booking (change seats / number of tickets) and cancel a booking (seats are released)
- **Sort** bookings by booking date, movie title, total price or customer name – ascending or descending

### Management (Weeks 6–7)
- `CinemaManager` connects all modules: add / update / delete for Movie, Showtime and Booking
- Text-based menu (`main.py`)
- **Save and load data:** SQLite database (`data/cinema.db`), export all data to text files, import movies from a text file
- Revenue report by movie

## 3. Technologies

- **Language:** Python 3
- **Code editor:** Thonny
- **Version control:** Git and GitHub
- **Interface:** Command-line interface (CLI)
- **Data storage:** SQLite (`data/cinema.db`, built into Python, no install needed); data can be exported to text files (`.txt`)

## 4. Project structure

```text
MovieBookingSystem/
├── main.py          # Text menu (input/print only)
├── management.py    # CinemaManager: business rules, connects all modules
├── movie.py         # Movie class + validation
├── showtime.py      # Showtime class + validation
├── booking.py       # Booking class + validation
├── database.py      # All SQL queries (SQLite)
├── seed_data.py     # Sample data for demo
├── data/            # Created automatically (ignored by Git)
│   ├── cinema.db
│   └── movies.txt, showtimes.txt, bookings.txt   (after export)
├── docs/
│   └── MovieBooking_UML.png
├── README.md
└── .gitignore
```

```text
main.py  ->  management.py  ->  database.py  ->  data/cinema.db
                 |
     movie.py / showtime.py / booking.py  (validate data before saving)
```

## 5. How to run

1. Install Python 3 and Thonny.
2. Clone the repository with GitHub Desktop (or download ZIP).
3. Open `seed_data.py` in Thonny and press **F5** once to load sample data.
4. Open `main.py` and press **F5 (Run)**.
5. Use the menu in the Shell to choose a function.

Each class file (`movie.py`, `showtime.py`, `booking.py`) can also be run alone to see its own tests.

## 6. Team responsibilities

| Role | Member | Module | Main responsibilities |
|---|---|---|---|
| A – Movie Data | Trần Đăng Khoa | `movie.py` | Movie class, movie information and validation |
| B – Showtime | Nguyễn Trần Nhật Anh | `showtime.py` | Showtime class, schedule, available seats |
| C – Ticket | Võ Nguyễn Khôi Nguyên | `booking.py` | Booking class, booking, change and cancellation |
| D – Management | Lê Nguyên | `management.py`, `main.py` | Module integration, menu, data management (Weeks 6–7 supported by all members) |

### Weekly plan

| Week | Goal | Result |
|---|---|---|
| 4 | UML class diagram | `docs/MovieBooking_UML.png` |
| 5 | Main classes: Movie, Showtime, Booking | `movie.py`, `showtime.py`, `booking.py` |
| 6 | `CinemaManager`: integrate modules; add / delete / update for Movie, Showtime, Booking | `management.py`, `main.py`, `database.py` |
| 7 | Search (ID, title, genre); sort (title, date, purchase) ascending / descending; save and load data | Search & sort menus, SQLite + text export/import |

## 7. How we collaborate

1. Create a GitHub **Issue** for a task.
2. Work on a separate feature **branch**.
3. Commit code with a clear message.
4. Open a **Pull Request** for review.
5. Merge tested changes into `main`.

## 8. Testing

Each class file (`movie.py`, `showtime.py`, `booking.py`) contains its own tests inside `if __name__ == "__main__":`.
Manual test cases cover valid and invalid inputs for movies, showtimes and bookings, room schedule conflicts, past showtimes, updating showtimes, seat conflicts, booking changes and cancellation, search and sort (ascending / descending), the revenue report, and exporting/importing text files.

## 9. Coding conventions

| Item | Rule | Example |
|---|---|---|
| Language | Names and messages in English; comments may be in Vietnamese | `calculate_total()` |
| Class names | PascalCase | `Movie`, `Showtime`, `Booking`, `CinemaManager` |
| Functions / variables | snake_case | `get_available_seats()`, `ticket_price` |
| Movie ID | `M` + 2 digits | `M01` |
| Showtime ID | `S` + 2 digits | `S01` |
| Booking ID | `B` + 3 digits | `B001` |
| Seat code | Row letter A–E + number 1–10 | `A1`, `E10` |
| Room | `R` + number | `R1` |
| Date | `YYYY-MM-DD` (string) | `2026-10-25` |
| Time | `HH:MM`, 24-hour | `19:30` |
| Money | VND, stored as `float`, displayed with commas | `80,000 VND` |
| Errors | Classes `raise ValueError`; only `main.py` / `management.py` use `try/except` | |
| Test code | Put inside `if __name__ == "__main__":` | |

## 10. Course information

- **Course:** PFP191 – Programming Fundamentals with Python
- **Project topic:** Topic 9 – Movie Ticket Purchase Management
- **Type:** Group assignment (4 members)

This repository is for learning and coursework. AI assistance is recorded in each member's AI Audit Log as required by the course.
