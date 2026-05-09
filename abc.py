import streamlit as st
from datetime import date
from car_logic import RentalBooking, validate_phone, format_receipt_name

# Title Heading
st.title("DRIVE LINK CAR RENTAL SYSTEM")
st.markdown("---")

# 1. Driver Information
st.header("Driver Information")
col1, col2 = st.columns(2)
with col1:
    f_name = st.text_input("First Name")
    l_name = st.text_input("Last Name")
    phone = st.text_input("Phone Number")
with col2:
    id_card = st.file_uploader("Upload ID Card (JPG)", type=["jpg", "jpeg"])
    license = st.file_uploader("Upload License Card (JPG)", type=["jpg", "jpeg"])

st.subheader("Next of Kin (Heir)")
heir_name = st.text_input("Heir Name")
heir_phone = st.text_input("Heir Phone Number")

# 2. Booking Option
st.header("Booking Option")
start_date = st.date_input("Start Date", value=date.today())
end_date = st.date_input("End Date", value=date.today())
total_days = (end_date - start_date).days

# 3. Car Option
st.header("Car Selection")
category = st.selectbox("Category", ["Sedan", "SUV", "Sport"])

car_data = {
    "Sedan": {"Proton Saga": 100, "Toyota Vios": 150, "Honda City": 160},
    "SUV": {"Perodua Ativa": 180, "Proton X50": 200, "Honda CR-V": 250},
    "Sport": {"Ford Mustang": 500, "BMW M4": 700, "Porsche 911": 1200}
}

selected_car = st.selectbox("Select Car Type", list(car_data[category].keys()))
price_per_day = car_data[category][selected_car]
st.info(f"Price: RM {price_per_day}")

# 4. Payment Option
st.header("Payment Option")
card_no = st.text_input("Bank Card Number", type="password")
ccv = st.text_input("CCV", max_chars=3, type="password")
sec_num = st.text_input("3-Digit Security Number", max_chars=3, type="password")

# 5. Submit and Exception Handling
st.markdown("---")
col_btn1, col_btn2 = st.columns(2)

if col_btn1.button("Submit Booking"):
    try:
        if not f_name or not l_name or not phone:
            raise ValueError("Driver information is incomplete!")

        if total_days <= 0:
            raise ValueError("End date must be after start date!")

        if not validate_phone(phone):
            raise ValueError("Invalid phone number format!")

        booking = RentalBooking(f_name, l_name, phone, selected_car, total_days)
        booking.base_price = price_per_day
        final_total = booking.calculate_total()

        st.success(f"Booking Successful for {format_receipt_name(f_name, l_name)}!")
        st.write(f"Total to pay: RM {final_total}")

        st.subheader("Booking Receipt")
        receipt_data = {
            "Driver": f"{f_name} {l_name}",
            "Car": selected_car,
            "Duration": f"{total_days} Days",
            "Total": f"RM {final_total}"
        }
        st.table(receipt_data)
        st.caption("PDF Receipt Generated Successfully (Simulated)")

    except ValueError as e:
        st.error(f"Input Error: {e}")
    except Exception as e:
        st.error(f"Unexpected Error: {e}")

if col_btn2.button("Cancel Booking"):
    st.warning("Booking has been cleared.")
    st.rerun()