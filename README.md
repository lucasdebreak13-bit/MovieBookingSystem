# Movie Ticket Booking Management System

A console-based movie ticket booking management system developed in **Python** for the **PFP191 – Programming Fundamentals with Python** course.

> **Project status:** In development. The features and project structure below describe our team's planned work; not all modules are finished yet.

## 1. Project objectives

This project helps users manage movie information, screening schedules, and ticket bookings. It also gives our team practice with:

- Object-Oriented Programming (OOP)
- Lists and dictionaries
- Input validation and exception handling
- Reading and writing text files
- Modular programming and teamwork using GitHub

## 2. Planned features

### Movie
- Create and display movie objects
- Add, update, and delete movies
- Search movies by title and genre
- Sort movies by ticket price and duration
- Validate movie information

The required movie fields are `movie_id`, `title`, `genre`, `duration`, and `ticket_price`. Our team may also include extra fields such as `age_rating`, `language`, `release_year`, and `status`.

### Showtime
- Create and manage showtimes for movies
- Store screening date, time, ticket price, and available seats
- Search and sort showtimes

### Booking
- Book tickets for a selected showtime
- Change the number of tickets in a booking
- Cancel a booking and restore the available seats
- View booking information

### Management
- Provide a text-based menu
- Connect Movie, Showtime, and Booking modules
- Save and load data from text files

## 3. Technologies

- **Language:** Python 3
- **Code editor:** Thonny
- **Version control:** Git and GitHub
- **Interface:** Command-line interface (CLI)
- **Data storage:** Text files (`.txt`)

## 4. Planned project structure

```text
MovieBookingSystem/
├── movie.py
├── showtime.py
├── booking.py
├── management.py
├── main.py
├── data/
│   ├── movies.txt
│   ├── showtimes.txt
│   └── bookings.txt
├── tests/
│   └── test_movie.py
├── README.md
└── .gitignore
```

*This structure may change as the team integrates the modules.*

## 5. How to run (when integration is complete)

1. Install Python 3 and Thonny.
2. Download the repository or clone it from GitHub.
3. Open the project folder and open `main.py` in Thonny.
4. Press **F5 (Run)**.
5. Use the menu in the Shell to choose a function.

> While `main.py` is not available, individual modules can be tested separately in Thonny.

## 6. Team responsibilities

| Member | Module | Main responsibilities |
|---|---|---|
| Member 1 | Movie | Movie class, movie information and validation |
| Member 2 | Showtime | Screening schedules and available seats |
| Member 3 | Booking | Booking, changes and cancellation |
| Member 4 | Management | Main menu, module integration and overall data management |

The team will agree on how to divide shared features such as movie search, sorting, and file handling before implementing them.

## 7. How we collaborate

1. Create a GitHub **Issue** for a task.
2. Work on a separate feature **branch**.
3. Commit code with a clear message.
4. Open a **Pull Request** for review.
5. Merge tested changes into `main`.

## 8. Testing

The team plans to test valid and invalid inputs, movie and showtime data, booking seat counts, and file saving/loading. Integration testing will be completed before submission.

## 9. Course information

- **Course:** PFP191 – Programming Fundamentals with Python
- **Project topic:** Movie Ticket Booking Management System
- **Type:** Group assignment (4 members)

This repository is for learning and coursework. AI assistance, if used, should be recorded in the course's AI Audit Log as required.
