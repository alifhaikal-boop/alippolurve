import streamlit as st
import pandas as pd
from datetime import date

# ========== CLASS DEFINITION ==========
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

# ========== FUNCTIONS ==========
def validate_phone(phone):
    return len(phone) >= 10 and phone.isdigit()

def format_receipt_name(first, last):
    return f"{first.upper()} {last.upper()}"

# ========== STREAMLIT UI ==========
st.title("🚗 DRIVE LINK CAR RENTAL SYSTEM")
st.markdown("---")

# Driver Information
st.header("Driver Information")
col1, col2 = st.columns(2)

with col1:
    f_name = st.text_input("First Name")
    l_name = st.text_input("Last Name")
    phone = st.text_input("Phone Number")

with col2:
    id_card = st.file_uploader("Upload ID Card (JPG)", type=["jpg", "jpeg"])
    license = st.file_uploader("Upload License Card (JPG)", type=["jpg", "jpeg"])

# Booking Option
st.header("Booking Option")
start_date = st.date_input("Start Date", value=date.today())
end_date = st.date_input("End Date", value=date.today())
total_days = (end_date - start_date).days

if total_days < 0:
    st.error("End date must be after start date!")
    total_days = 0

# Car Selection
st.header("Car Selection")
car_data = {
    "Proton Saga": 100,
    "Perodua Myvi": 120,
    "Toyota Vios": 150,
    "Honda Civic": 180
}

selected_car = st.selectbox("Select Car", list(car_data.keys()))
price_per_day = car_data[selected_car]
st.info(f"Price per day: RM{price_per_day}")

# Submit Button
if st.button("Confirm Booking"):
    if not f_name or not l_name:
        st.error("Please enter full name")
    elif not validate_phone(phone):
        st.error("Invalid phone number (min 10 digits)")
    elif total_days <= 0:
        st.error("Please select valid dates")
    else:
        # Create object from class
        booking = RentalBooking(f_name, l_name, phone, selected_car, total_days)
        booking.base_price = price_per_day
        total_price = booking.calculate_total()
        
        st.success(f"✅ Booking Successful for {format_receipt_name(f_name, l_name)}!")
        st.write(f"**Total to pay: RM{total_price}**")
        
        # Receipt using Pandas DataFrame
        st.subheader("📄 Booking Receipt")
        receipt_df = pd.DataFrame({
            "Item": ["Driver", "Car", "Duration", "Total"],
            "Details": [f"{f_name} {l_name}", selected_car, f"{total_days} days", f"RM{total_price}"]
        })
        st.table(receipt_df)
        st.balloons()