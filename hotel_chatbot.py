# ✅ Updated code with booking confirmation system
import streamlit as st
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import json

# Multilingual UI text
UI_TEXT = {
    "hotel_select": {
        "en": "Select Your Hotel",
        "hi": "अपना होटल चुनें",
        "awa": "अपना होटल चुनि"
    },
    "choose_hotel": {
        "en": "Choose your hotel:",
        "hi": "होटल चुनें:",
        "awa": "होटल चुनि:"
    },
    "confirm_hotel": {
        "en": "Confirm Hotel",
        "hi": "होटल पुष्टि करें",
        "awa": "होटल पक्का करीं"
    },
    "checkin_header": {
        "en": "Select Check-in Date and Time",
        "hi": "चेक-इन की तारीख और समय चुनें",
        "awa": "चेक-इन के तारीख अउर समय चुनि"
    },
    "checkin_date": {
        "en": "Check-in Date",
        "hi": "चेक-इन की तारीख",
        "awa": "चेक-इन के तारीख"
    },
    "checkin_time": {
        "en": "Check-in Time",
        "hi": "चेक-इन का समय",
        "awa": "चेक-इन के समय"
    },
    "confirm_checkin": {
        "en": "Confirm Check-in",
        "hi": "चेक-इन पुष्टि करें",
        "awa": "चेक-इन पक्का करीं"
    },
    "checkout_header": {
        "en": "Select Check-out Date and Time",
        "hi": "चेक-आउट की तारीख और समय चुनें",
        "awa": "चेक-आउट के तारीख अउर समय चुनि"
    },
    "checkout_date": {
        "en": "Check-out Date",
        "hi": "चेक-आउट की तारीख",
        "awa": "चेक-आउट के तारीख"
    },
    "checkout_time": {
        "en": "Check-out Time",
        "hi": "चेक-आउट का समय",
        "awa": "चेक-आउट के समय"
    },
    "confirm_checkout": {
        "en": "Confirm Check-out",
        "hi": "चेक-आउट पुष्टि करें",
        "awa": "चेक-आउट पक्का करीं"
    },
    "room_type_header": {
        "en": "Select Room Type",
        "hi": "कमरे का प्रकार चुनें",
        "awa": "कमरा के किस्म चुनि"
    },
    "room_type": {
        "en": "Room Type",
        "hi": "कमरे का प्रकार",
        "awa": "कमरा के किस्म"
    },
    "confirm_room_type": {
        "en": "Confirm Room Type",
        "hi": "कमरे का प्रकार पुष्टि करें",
        "awa": "कमरा के किस्म पक्का करीं"
    },
    "guests_header": {
        "en": "Number of Guests",
        "hi": "अतिथियों की संख्या",
        "awa": "मेहमानन के गिनती"
    },
    "confirm_guests": {
        "en": "Confirm Number of Guests",
        "hi": "संख्या पुष्टि करें",
        "awa": "गिनती पक्का करीं"
    },
    "name_header": {
        "en": "Your Name",
        "hi": "आपका नाम",
        "awa": "आपके नाम"
    },
    "confirm_name": {
        "en": "Confirm Name",
        "hi": "नाम पुष्टि करें",
        "awa": "नाम पक्का करीं"
    },
    "phone_header": {
        "en": "Your Phone Number",
        "hi": "आपका फोन नंबर",
        "awa": "आपके फोन नंबर"
    },
    "confirm_phone": {
        "en": "Confirm Phone Number",
        "hi": "फोन नंबर पुष्टि करें",
        "awa": "फोन नंबर पक्का करीं"
    },
    "email_header": {
        "en": "Your Email Address",
        "hi": "आपका ईमेल पता",
        "awa": "आपके ईमेल पता"
    },
    "confirm_email": {
        "en": "Confirm Email",
        "hi": "ईमेल पुष्टि करें",
        "awa": "ईमेल पक्का करीं"
    },
    "special_requests_header": {
        "en": "Special Requests",
        "hi": "विशेष अनुरोध",
        "awa": "खास फरमाइश"
    },
    "special_requests": {
        "en": "Any special requests? (Type 'none' if not)",
        "hi": "कोई विशेष अनुरोध? (अगर नहीं तो 'none' लिखें)",
        "awa": "कोई खास फरमाइश? (नाहीं त 'none' लिखीं)"
    },
    "confirm_special_requests": {
        "en": "Confirm Special Requests",
        "hi": "अनुरोध पुष्टि करें",
        "awa": "फरमाइश पक्का करीं"
    },
    "booking_summary": {
        "en": "✅ Booking confirmed! Here's your booking summary:",
        "hi": "✅ बुकिंग पुष्टि हो गई! आपकी बुकिंग का सारांश:",
        "awa": "✅ बुकिंग पक्का भइल! बुकिंग के बिवरन:"
    },
    "thank_you": {
        "en": "Thank you for choosing our hotel! We look forward to welcoming you.",
        "hi": "हमारे होटल को चुनने के लिए धन्यवाद! हम आपका स्वागत करने के लिए उत्सुक हैं।",
        "awa": "हमार होटल चुनै खातिर धन्यवाद! हम रउरा के स्वागत करे के बाट जोहत बानी।"
    },
    "guests_label": {
        "en": "Number of Guests",
        "hi": "अतिथियों की संख्या",
        "awa": "मेहमानन के गिनती"
    },
    "name_label": {
        "en": "Full Name",
        "hi": "पूरा नाम",
        "awa": "पूरा नाम"
    },
    "phone_label": {
        "en": "Phone Number",
        "hi": "फोन नंबर",
        "awa": "फोन नंबर"
    },
    "email_label": {
        "en": "Email",
        "hi": "ईमेल",
        "awa": "ईमेल"
    }
}

try:
    import requests
except ModuleNotFoundError:
    st.warning("⚠️ The 'requests' module is not installed. Please run `pip install requests`.")

# Load environment variables
load_dotenv()

# Configure DeepSeek API
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    st.error("❌ DeepSeek API key not found. Please check your .env file.")

# Initialize all session state variables at the start
if "messages" not in st.session_state:
    st.session_state.messages = []
if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "current_step" not in st.session_state:
    st.session_state.current_step = "start"
if "booking_data" not in st.session_state:
    st.session_state.booking_data = {}

# Define DeepSeek API function
def ask_deepseek(user_query, lang='en'):
    if not api_key:
        return {
            "en": "DeepSeek API key not found. Please check your .env file.",
            "hi": "DeepSeek API कुंजी नहीं मिली। कृपया अपनी .env फ़ाइल की जाँच करें।",
            "awa": "DeepSeek API कुंजी नाहीं मिलल। कृपया .env फ़ाइल देखीं।"
        }[lang]

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": f"""You are a helpful hotel receptionist in Lucknow, India. Answer in {lang}. You have knowledge about two main hotels:

1. Golden Tulip Lucknow:
- 4-star business hotel
- Check-in: 2:00 PM, Check-out: 11:00 AM
- Features: Free Wi-Fi, AC, rooftop swimming pool, secure parking, airport shuttle
- Restaurant 'Branche': Open 7:00 AM - 11:00 PM, serves buffet breakfast
- Nearby attractions: Bara Imambara, Rumi Darwaza (10-15 min drive), Hazratganj Market (3 km)
- Simple Booking Process:
  * Check-in: 2:00 PM onwards
  * Check-out: By 11:00 AM
  * Room Types: Single, Double, Suite
  * Special Requests: Early check-in, late check-out, extra bed, airport pickup

2. Saraca Hotel Lucknow:
- Heritage hotel with art-modern architecture
- 41 beautiful rooms
- Features: Free Wi-Fi, outdoor swimming pool, 24-hour gym
- Restaurant 'Azrak': Serves Indian cuisine, open all day
- Check-in: 2:00 PM, Check-out: 12:00 PM
- Simple Booking Process:
  * Check-in: 2:00 PM onwards
  * Check-out: By 12:00 PM
  * Room Types: Single, Double, Family Suite
  * Special Requests: Early check-in, late check-out, extra bed, airport pickup

Quick Booking Guide:
1. Choose your dates
2. Select room type
3. Add any special requests
4. Provide contact details
5. Confirm booking

When a guest wants to make a booking, ask for:
- Hotel preference (Golden Tulip or Saraca)
- Check-in date
- Check-out date
- Room type
- Number of guests
- Contact details (name, phone, email)
- Any special requests

Be friendly and helpful. If asked about specific hotels, provide accurate information. For general queries, you can mention both hotels' features. Always maintain a professional yet warm tone."""
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            st.error(error_msg)
            return {
                "en": f"Sorry, I couldn't get a response right now. {error_msg}",
                "hi": f"क्षमा करें, अभी जवाब नहीं मिल पाया। {error_msg}",
                "awa": f"माफ करिए, जवाब नाहीं मिल पाइल बा। {error_msg}"
            }[lang]

    except Exception as e:
        error_msg = str(e)
        print("DeepSeek Error:", error_msg)
        st.error(f"API Error: {error_msg}")
        return {
            "en": f"Sorry, I couldn't get a response right now. Error: {error_msg}",
            "hi": f"क्षमा करें, अभी जवाब नहीं मिल पाया। त्रुटि: {error_msg}",
            "awa": f"माफ करिए, जवाब नाहीं मिल पाइल बा। त्रुटि: {error_msg}"
        }[lang]

# Function to generate booking reference
def generate_booking_ref():
    return f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"

# Function to save booking
def save_booking(booking_data):
    booking_data["booking_ref"] = generate_booking_ref()
    booking_data["status"] = "confirmed"
    booking_data["booking_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.bookings.append(booking_data)
    return booking_data["booking_ref"]

# Function to display welcome message
def display_welcome_message():
    return """👋 Welcome to our Hotel Booking Chatbot!

I can help you book a room at either:
1. Golden Tulip Lucknow (4-star business hotel)
2. Saraca Hotel Lucknow (Heritage hotel)

To start booking, type 'book'
To see available commands, type 'help'
To view hotel details, type 'info'
To cancel booking, type 'cancel'

How can I assist you today?"""

# Function to display help message
def display_help_message():
    return """📋 Available Commands:

1. 'book' - Start a new booking
2. 'help' - Show this help message
3. 'info' - View hotel information
4. 'cancel' - Cancel current booking
5. 'history' - View booking history

Booking Process:
1. Select hotel
2. Choose dates
3. Select room type
4. Enter guest details
5. Add special requests

Need more help? Just ask!"""

# Function to display hotel information
def display_hotel_info():
    return """🏨 Hotel Information:

1. Golden Tulip Lucknow:
   - 4-star business hotel
   - Check-in: 2:00 PM, Check-out: 11:00 AM
   - Features: Free Wi-Fi, AC, rooftop pool, secure parking
   - Restaurant 'Branche': 7:00 AM - 11:00 PM
   - Room Types: Single, Double, Suite

2. Saraca Hotel Lucknow:
   - Heritage hotel with modern architecture
   - 41 beautiful rooms
   - Features: Free Wi-Fi, outdoor pool, 24-hour gym
   - Restaurant 'Azrak': All-day Indian cuisine
   - Check-in: 2:00 PM, Check-out: 12:00 PM
   - Room Types: Single, Double, Family Suite"""

# Language selection UI
lang = st.selectbox(
    "Choose your language:",
    ["en", "hi", "awa"],
    format_func=lambda l: {"en": "English", "hi": "Hindi", "awa": "Awadhi"}[l]
)

# Sidebar: Current time display
with st.sidebar:
    now = datetime.now()
    st.markdown(f"🕒 **Time:** {now.strftime('%A, %d %B %Y — %I:%M %p')}")
    
    # Display booking history
    if st.session_state.bookings:
        st.markdown("### 📋 Recent Bookings")
        for booking in st.session_state.bookings[-5:]:  # Show last 5 bookings
            st.markdown(f"""
            **Booking Ref:** {booking['booking_ref']}  
            **Hotel:** {booking['hotel']}  
            **Check-in:** {booking['check_in']}  
            **Check-out:** {booking['check_out']}  
            **Status:** {booking['status']}  
            ---
            """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- MAIN APP FLOW ---
show_form_message = None

if st.session_state.current_step == "hotel_selection":
    with st.form("hotel_select_form"):
        st.subheader(UI_TEXT["hotel_select"][lang])
        hotel = st.radio(UI_TEXT["choose_hotel"][lang], ["Golden Tulip Lucknow", "Saraca Hotel Lucknow"])
        submitted = st.form_submit_button(UI_TEXT["confirm_hotel"][lang])
        if submitted:
            st.session_state.booking_data["hotel"] = hotel
            st.session_state.current_step = "check_in"
            st.rerun()

elif st.session_state.current_step == "check_in":
    with st.form("check_in_form"):
        st.subheader(UI_TEXT["checkin_header"][lang])
        check_in_date = st.date_input(
            UI_TEXT["checkin_date"][lang],
            min_value=datetime.now().date(),
            help="Select your check-in date"
        )
        check_in_time = st.time_input(
            UI_TEXT["checkin_time"][lang],
            value=datetime.strptime("14:00", "%H:%M").time(),
            help="Check-in time (24 hours allowed)"
        )
        submitted = st.form_submit_button(UI_TEXT["confirm_checkin"][lang])
        if submitted:
            check_in_datetime = datetime.combine(check_in_date, check_in_time)
            st.session_state.booking_data["check_in"] = check_in_datetime.strftime("%Y-%m-%d %H:%M")
            st.session_state.current_step = "check_out"
            st.rerun()

elif st.session_state.current_step == "check_out":
    with st.form("check_out_form"):
        st.subheader(UI_TEXT["checkout_header"][lang])
        check_in_datetime = datetime.strptime(st.session_state.booking_data["check_in"], "%Y-%m-%d %H:%M")
        min_check_out = check_in_datetime + timedelta(hours=1)  # Minimum 1 hour stay
        check_out_date = st.date_input(
            UI_TEXT["checkout_date"][lang],
            min_value=min_check_out.date(),
            help="Select your check-out date"
        )
        check_out_time = st.time_input(
            UI_TEXT["checkout_time"][lang],
            value=datetime.strptime("11:00", "%H:%M").time(),
            help="Check-out time (24 hours allowed)"
        )
        submitted = st.form_submit_button(UI_TEXT["confirm_checkout"][lang])
        if submitted:
            check_out_datetime = datetime.combine(check_out_date, check_out_time)
            if check_out_datetime <= check_in_datetime:
                st.error("Check-out time must be after check-in time. Please select a valid time.")
            else:
                st.session_state.booking_data["check_out"] = check_out_datetime.strftime("%Y-%m-%d %H:%M")
                st.session_state.current_step = "room_type"
                st.rerun()

elif st.session_state.current_step == "room_type":
    with st.form("room_type_form"):
        st.subheader(UI_TEXT["room_type_header"][lang])
        room_type = st.selectbox(UI_TEXT["room_type"][lang], ["Single", "Double", "Suite", "Family Suite"])
        submitted = st.form_submit_button(UI_TEXT["confirm_room_type"][lang])
        if submitted:
            st.session_state.booking_data["room_type"] = room_type
            st.session_state.current_step = "guests"
            st.rerun()

elif st.session_state.current_step == "guests":
    with st.form("guests_form"):
        st.subheader(UI_TEXT["guests_header"][lang])
        guests = st.number_input("Number of Guests", min_value=1, max_value=4, value=1)
        submitted = st.form_submit_button(UI_TEXT["confirm_guests"][lang])
        if submitted:
            st.session_state.booking_data["guests"] = guests
            st.session_state.current_step = "name"
            st.rerun()

elif st.session_state.current_step == "name":
    with st.form("name_form"):
        st.subheader(UI_TEXT["name_header"][lang])
        name = st.text_input("Full Name")
        submitted = st.form_submit_button(UI_TEXT["confirm_name"][lang])
        if submitted:
            if len(name.strip()) > 0:
                st.session_state.booking_data["name"] = name
                st.session_state.current_step = "phone"
                st.rerun()
            else:
                st.error("Please enter a valid name.")

elif st.session_state.current_step == "phone":
    with st.form("phone_form"):
        st.subheader(UI_TEXT["phone_header"][lang])
        phone = st.text_input("Phone Number")
        submitted = st.form_submit_button(UI_TEXT["confirm_phone"][lang])
        if submitted:
            if len(phone.strip()) >= 10:
                st.session_state.booking_data["phone"] = phone
                st.session_state.current_step = "email"
                st.rerun()
            else:
                st.error("Please enter a valid phone number (minimum 10 digits).")

elif st.session_state.current_step == "email":
    with st.form("email_form"):
        st.subheader(UI_TEXT["email_header"][lang])
        email = st.text_input("Email")
        submitted = st.form_submit_button(UI_TEXT["confirm_email"][lang])
        if submitted:
            if "@" in email and "." in email:
                st.session_state.booking_data["email"] = email
                st.session_state.current_step = "special_requests"
                st.rerun()
            else:
                st.error("Please enter a valid email address.")

elif st.session_state.current_step == "special_requests":
    with st.form("special_requests_form"):
        st.subheader(UI_TEXT["special_requests_header"][lang])
        special_requests = st.text_area("Any special requests? (Type 'none' if not)")
        submitted = st.form_submit_button(UI_TEXT["confirm_special_requests"][lang])
        if submitted:
            st.session_state.booking_data["special_requests"] = special_requests if special_requests.lower() != "none" else ""
            booking_ref = save_booking(st.session_state.booking_data)
            st.session_state.current_step = "summary"
            st.rerun()

elif st.session_state.current_step == "summary":
    st.success(UI_TEXT["booking_summary"][lang] + "\n\n"
               + f"🏨 Hotel: {st.session_state.booking_data['hotel']}\n"
               + f"📅 Check-in: {st.session_state.booking_data['check_in']}\n"
               + f"📅 Check-out: {st.session_state.booking_data['check_out']}\n"
               + f"🛏️ Room Type: {st.session_state.booking_data['room_type']}\n"
               + f"👥 Guests: {st.session_state.booking_data['guests']}\n"
               + f"👤 Name: {st.session_state.booking_data['name']}\n"
               + f"📱 Phone: {st.session_state.booking_data['phone']}\n"
               + f"📧 Email: {st.session_state.booking_data['email']}\n"
               + f"📝 Special Requests: {st.session_state.booking_data['special_requests']}\n"
               + f"\n🔖 Your booking reference is: {st.session_state.booking_data['booking_ref']}\n\n"
               + UI_TEXT["thank_you"][lang])
    st.balloons()
    # Reset for next booking
    st.session_state.current_step = "start"
    st.session_state.booking_data = {}

# Only show chat input if not in a form step
if st.session_state.current_step not in [
    "hotel_selection", "check_in", "check_out", "room_type", "guests", "name", "phone", "email", "special_requests", "summary"
]:
    if prompt := st.chat_input("Type your message here..."):
        timestamp = datetime.now().strftime('%I:%M %p')
        user_msg = f"🕒 {timestamp} — {prompt}"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.write(user_msg)

        # Handle special commands
        if prompt.lower() == "help":
            response = display_help_message()
        elif prompt.lower() == "info":
            response = display_hotel_info()
        elif prompt.lower() == "cancel":
            if st.session_state.current_step != "start":
                st.session_state.current_step = "start"
                st.session_state.booking_data = {}
                response = "Booking cancelled. Type 'book' to start a new booking."
            else:
                response = "No active booking to cancel."
        elif prompt.lower() == "history":
            if st.session_state.bookings:
                response = "📋 Recent Bookings:\n\n" + "\n\n".join([
                    f"Booking Ref: {b['booking_ref']}\nHotel: {b['hotel']}\nCheck-in: {b['check_in']}\nStatus: {b['status']}"
                    for b in st.session_state.bookings[-5:]
                ])
            else:
                response = "No booking history available."
        elif prompt.lower() == "book":
            st.session_state.current_step = "hotel_selection"
            response = "Let's start your booking! Please use the form below."
        else:
            response = ask_deepseek(prompt, lang)

        assistant_msg = f"🕒 {timestamp} — {response}"
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
        with st.chat_message("assistant"):
            st.write(assistant_msg)

# Display welcome message if no messages yet
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(display_welcome_message())
    st.session_state.messages.append({"role": "assistant", "content": display_welcome_message()})

