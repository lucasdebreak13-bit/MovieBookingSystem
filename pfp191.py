class Showtime:
    def __init__(self, show_code, title, time, date, ticket_price):
        self.show_code = show_code
        self.title = title
        self.time = time
        self.date = date
        self.ticket_price = ticket_price
        self.seats = {}
        for row in "ABCDE":
            for column in range(1, 11):
                seat_code = f"{row}{column}"
                self.seats[seat_code] = True
    def Showtime_information(self):
        print(f"Show code: {self.show_code} | Title: {self.title} | Date: {self.date} | "
              f"Time: {self.time} | Price: {self.ticket_price} dollar")
    def get_available_seats(self):
        empty_seats = []
        for seat_name, is_available in self.seats.items():
            if is_available:
                empty_seats.append(seat_name)
        return empty_seats
    def book_ticket(self, seat_name):
        if seat_name in self.seats:
            if self.seats[seat_name]:
                self.seats[seat_name] = False
                print(f"Success: Seat '{seat_name}' has been successfully booked!")
                return True
            else:
                print(f"Denied: Seat '{seat_name}' is already booked!")
                return False
        else:
            print(f"Error: Seat '{seat_name}' does not exist!")
            return False