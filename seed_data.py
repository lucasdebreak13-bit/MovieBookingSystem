"""
seed_data.py - Nạp dữ liệu mẫu để demo. Chạy 1 lần bằng F5 trong Thonny.
Chạy lại nhiều lần cũng không sao: dữ liệu đã có thì bỏ qua.
"""
from management import CinemaManager
from movie import Movie
from showtime import Showtime

manager = CinemaManager()

sample_movies = [
    Movie('M01', 'Avatar 10', 'Sci-fi', 192, 'T13', 'English', 80000.0, 2026),
    Movie('M02', 'Cyberfun 2099', 'Animation', 110, 'P', 'Vietnamese', 120000.0, 2099, 'Coming Soon'),
    Movie('M03', 'Jurassic Worldt', 'Adventure', 124, 'T18', 'English', 96000.0, 2026),
    Movie('M04', 'Interstellate', 'Sci-fi', 169, 'T16', 'English', 75000.0, 2025, 'Ended'),
    Movie('M05', 'The Conjuring1', 'Horror', 112, 'K', 'Japanese', 99000.0, 2026),
]

sample_showtimes = [
    Showtime('S01', 'M01', 'R1', '2026-10-25', '19:30', 80000),
    Showtime('S02', 'M01', 'R2', '2026-10-25', '21:00', 90000),
    Showtime('S03', 'M03', 'R1', '2026-10-26', '18:00', 96000),
    Showtime('S04', 'M05', 'R3', '2026-10-26', '22:00', 99000),
]

for m in sample_movies:
    try:
        manager.add_movie(m)
        print('Added movie   :', m)
    except ValueError as e:
        print('Skip movie    :', e)

for s in sample_showtimes:
    try:
        manager.add_showtime(s)
        print('Added showtime:', s)
    except ValueError as e:
        print('Skip showtime :', e)

print('\nSeed data done! Now run main.py')
