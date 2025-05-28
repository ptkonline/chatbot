# ✅ Updated code with booking confirmation system
import streamlit as st
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import json

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

# Initialize session state for bookings
if "bookings" not in st.session_state:
    st.session_state.bookings = []

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

# Language selection UI
lang = st.selectbox(
    "Choose your language:",
    ["en", "hi", "awa"],
    format_func=lambda l: {"en": "English", "hi": "Hindi", "awa": "Awadhi"}[l]
)

# Initialize chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input box
if prompt := st.chat_input("Type your message here..."):
    timestamp = datetime.now().strftime('%I:%M %p')
    user_msg = f"🕒 {timestamp} — {prompt}"
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.write(user_msg)

    response = ask_deepseek(prompt, lang)
    assistant_msg = f"🕒 {timestamp} — {response}"
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
    with st.chat_message("assistant"):
        st.write(assistant_msg)
        
        # If the response indicates a booking confirmation, show booking form
        if "booking" in prompt.lower() or "book" in prompt.lower():
            with st.form("booking_form"):
                st.subheader("📝 Booking Form")
                hotel = st.selectbox("Select Hotel", ["Golden Tulip Lucknow", "Saraca Hotel Lucknow"])
                check_in = st.date_input("Check-in Date", min_value=datetime.now())
                check_out = st.date_input("Check-out Date", min_value=check_in + timedelta(days=1))
                room_type = st.selectbox("Room Type", ["Single", "Double", "Suite", "Family Suite"])
                guests = st.number_input("Number of Guests", min_value=1, max_value=4)
                name = st.text_input("Full Name")
                phone = st.text_input("Phone Number")
                email = st.text_input("Email")
                special_requests = st.text_area("Special Requests")
                
                if st.form_submit_button("Confirm Booking"):
                    booking_data = {
                        "hotel": hotel,
                        "check_in": check_in.strftime("%Y-%m-%d"),
                        "check_out": check_out.strftime("%Y-%m-%d"),
                        "room_type": room_type,
                        "guests": guests,
                        "name": name,
                        "phone": phone,
                        "email": email,
                        "special_requests": special_requests
                    }
                    
                    booking_ref = save_booking(booking_data)
                    st.success(f"✅ Booking confirmed! Your booking reference is: {booking_ref}")
                    st.balloons()

