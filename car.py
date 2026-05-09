import pandas as pd

class RentalBooking:
    def __init__(self, first_name, last_name, phone, car_type, days):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.car_type = car_type
        self.days = days
        self.base_price = 150

    def calculate_total(self, insurance=0):
        return (self.base_price * self.days) + insurance

class PremiumBooking(RentalBooking):
    def __init__(self, first_name, last_name, phone, car_type, days, member_id):
        super().__init__(first_name, last_name, phone, car_type, days)
        self.member_id = member_id

    def calculate_total(self, discount=0):
        total = self.base_price * self.days
        return total - discount

def validate_phone(phone):
    return len(phone) >= 10 and phone.isdigit()

def format_receipt_name(first, last):
    return f"{first.upper()} {last.upper()}"