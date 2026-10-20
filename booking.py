class ticket_purchase:
    def __init__(self,
                ticket_id: str=None,
                showtime_id: str=None,
                customer_id: str=None,
                number_of_tickets: int=0,
                booking_date: str=None,
                room_number: str=None,
                price: int=0):
            self.ticket_id = ticket_id
            self.showtime_id= showtime_id
            self.customer_id = customer_id
            self.number_of_tickets = number_of_tickets
            self.booking_date = booking_date
            self.room_number = room_number
            self.price = price
    def tinh_tong_tien(self):
            return self.number_of_tickets * self.price
    def __str__(self):
            return (f"Vé ID: {self.ticket_id}|"
                    f"{self.showtime_id}|"
                    f"{self.number_of_tickets}|"
                    f"{self.customer_id}|"
                    f"{self.booking_date}|"
                    f"{self.room_number}|"
                    f"{self.price}|"
                    f"{self.tinh_tong_tien()} VNĐ"
                    )
ve= ticket_purchase()
ve.tinh_tong_tien()
print(ve)
