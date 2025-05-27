import streamlit as st

# Set page config first, before any other Streamlit commands
st.set_page_config(
    page_title="Hotel Receptionist AI",
    page_icon="🏨",
    layout="wide"
)

import sqlite3
from datetime import datetime, timedelta
from difflib import get_close_matches
import re
import pandas as pd

# --- Setup SQLite ---
@st.cache_resource
def init_db():
    conn = sqlite3.connect("hotel_bookings.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_count INTEGER,
            room_type TEXT,
            checkin_date TEXT,
            checkout_date TEXT,
            language TEXT,
            status TEXT DEFAULT 'confirmed',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

# --- Hotel Profile ---
hotel_profile = {
    "name": "Golden Tulip Lucknow",
    "check_in": "2:00 PM",
    "check_out": "11:00 AM",
    "room_types": {
        "single": {"price": 3000, "capacity": 1},
        "double": {"price": 5000, "capacity": 2},
        "deluxe": {"price": 8000, "capacity": 3}
    }
}

# --- Language Responses ---
responses = {
    "greeting": {
        "en": f"Welcome to {hotel_profile['name']}! How can I assist you today?",
        "hi": f"{hotel_profile['name']} में आपका स्वागत है! मैं आपकी कैसे सहायता कर सकता हूं?",
        "awa": f"{hotel_profile['name']} में आपका स्वागत बा! हमरा कइसे मदद कर सकत बानी?"
    },
    "checkin_info": {
        "en": f"Check-in time is {hotel_profile['check_in']}, and check-out is by {hotel_profile['check_out']}.",
        "hi": f"चेक-इन का समय {hotel_profile['check_in']} है, और चेक-आउट {hotel_profile['check_out']} तक है।",
        "awa": f"चेक-इन {hotel_profile['check_in']} से होई, और चेक-आउट {hotel_profile['check_out']} तक होई।"
    },
    "booking_confirmation": {
        "en": "Your booking has been confirmed! Here are the details:",
        "hi": "आपका बुकिंग कन्फर्म हो गया है! यहाँ विवरण है:",
        "awa": "आपका बुकिंग हो गईल बा! यहाँ सब जानकारी बा:"
    },
    "invalid_dates": {
        "en": "Please provide valid check-in and check-out dates.",
        "hi": "कृपया वैध चेक-इन और चेक-आउट तिथियां दें।",
        "awa": "कृपया सही चेक-इन और चेक-आउट तारीख बताईए।"
    },
    "unknown": {
        "en": "I'm sorry, I didn't understand that. Could you please rephrase?",
        "hi": "क्षमा करें, मैं नहीं समझ पाया। क्या आप दोबारा बता सकते हैं?",
        "awa": "कृपया करो, मैं ना बुझा पाएं। फिर से बताईए?"
    }
}

# --- Intent Keywords ---
intent_keywords = {
    "greeting": ["hello", "hi", "namaste", "राम राम", "नमस्ते"],
    "checkin_info": ["check-in", "check out", "चेक-इन", "चेकआउट", "समय"],
    "booking": ["room", "guests", "book", "सिंगल", "डबल", "room", "guest", "जन", "बुक"]
}
intent_map = {k: v for v, keys in intent_keywords.items() for k in keys}

# --- Extractors ---
def identify_intent(text):
    text = text.lower().strip()
    for word in text.split():
        match = get_close_matches(word, intent_map.keys(), n=1, cutoff=0.8)
        if match:
            return intent_map[match[0]]
    return "unknown"

def extract_guest_count(text):
    m = re.search(r"\b(\d{1,2})\b", text)
    if m:
        count = int(m.group(1))
        return count if 1 <= count <= 4 else None
    return None

def extract_dates(text):
    # Try multiple date formats
    date_patterns = [
        r"\b(\d{1,2})[\/\-. ](\d{1,2})[\/\-. ](\d{4})\b",  # DD/MM/YYYY
        r"\b(\d{1,2})[\/\-. ](\d{1,2})\b",  # DD/MM
        r"\b(\d{4})[\/\-. ](\d{1,2})[\/\-. ](\d{1,2})\b"   # YYYY/MM/DD
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        if len(matches) >= 2:
            try:
                if len(matches[0]) == 3:  # Full date format
                    ci = datetime.strptime("/".join(matches[0]), "%d/%m/%Y")
                    co = datetime.strptime("/".join(matches[1]), "%d/%m/%Y")
                else:  # Short date format
                    ci = datetime.strptime("/".join(matches[0]), "%d/%m")
                    co = datetime.strptime("/".join(matches[1]), "%d/%m")
                    ci = ci.replace(year=datetime.now().year)
                    co = co.replace(year=datetime.now().year)
                
                # Validate dates
                if ci < datetime.now() or co <= ci:
                    return None, None
                return ci.strftime("%Y-%m-%d"), co.strftime("%Y-%m-%d")
            except ValueError:
                continue
    return None, None

def extract_room_type(text):
    text = text.lower()
    for rt in hotel_profile["room_types"].keys():
        if rt in text:
            return rt
    return "double"  # Default room type

def calculate_price(room_type, checkin, checkout):
    checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
    checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
    nights = (checkout_date - checkin_date).days
    return hotel_profile["room_types"][room_type]["price"] * nights

# --- Chatbot Logic ---
def handle_query(text, lang):
    intent = identify_intent(text)
    
    if intent == "greeting":
        return responses["greeting"][lang]
    elif intent == "checkin_info":
        return responses["checkin_info"][lang]
    elif intent == "booking":
        guests = extract_guest_count(text)
        checkin, checkout = extract_dates(text)
        room_type = extract_room_type(text)
        
        if not guests or not checkin or not checkout:
            return {
                "en": "Please provide: number of guests (1-4), room type, and valid check-in/check-out dates.",
                "hi": "कृपया दें: अतिथियों की संख्या (1-4), रूम टाइप, और वैध चेक-इन/चेक-आउट तिथियां।",
                "awa": "कृपया बताईए: जन की संख्या (1-4), रूम टाइप, और सही चेक-इन/चेक-आउट तारीख।"
            }[lang]
        
        # Validate room capacity
        if guests > hotel_profile["room_types"][room_type]["capacity"]:
            return {
                "en": f"Sorry, {room_type} room can only accommodate {hotel_profile['room_types'][room_type]['capacity']} guests.",
                "hi": f"क्षमा करें, {room_type} रूम में केवल {hotel_profile['room_types'][room_type]['capacity']} अतिथि रह सकते हैं।",
                "awa": f"माफ़ करीं, {room_type} रूम में {hotel_profile['room_types'][room_type]['capacity']} जन के लेला जगह बा।"
            }[lang]
        
        # Calculate price
        total_price = calculate_price(room_type, checkin, checkout)
        
        # Store booking
        cursor.execute("""
            INSERT INTO bookings (guest_count, room_type, checkin_date, checkout_date, language)
            VALUES (?, ?, ?, ?, ?)
        """, (guests, room_type, checkin, checkout, lang))
        conn.commit()
        
        # Return confirmation with details
        return f"{responses['booking_confirmation'][lang]}\n" + {
            "en": f"• Guests: {guests}\n• Room: {room_type}\n• Check-in: {checkin}\n• Check-out: {checkout}\n• Total: ₹{total_price}",
            "hi": f"• अतिथि: {guests}\n• रूम: {room_type}\n• चेक-इन: {checkin}\n• चेक-आउट: {checkout}\n• कुल: ₹{total_price}",
            "awa": f"• जन: {guests}\n• रूम: {room_type}\n• चेक-इन: {checkin}\n• चेक-आउट: {checkout}\n• कुल: ₹{total_price}"
        }[lang]
    
    return responses["unknown"][lang]

# --- Streamlit UI ---

# Sidebar
with st.sidebar:
    st.title("🏨 Hotel Info")
    st.write(f"**Hotel:** {hotel_profile['name']}")
    st.write(f"**Check-in:** {hotel_profile['check_in']}")
    st.write(f"**Check-out:** {hotel_profile['check_out']}")
    
    st.markdown("---")
    st.subheader("Room Types & Prices")
    for rt, info in hotel_profile["room_types"].items():
        st.write(f"**{rt.title()}:** ₹{info['price']}/night (max {info['capacity']} guests)")

# Main content
st.title("🏨 Hotel Receptionist Chatbot")

# Language selection
lang = st.selectbox(
    "Choose your language:",
    ["en", "hi", "awa"],
    format_func=lambda l: {"en": "English", "hi": "Hindi", "awa": "Awadhi"}[l]
)

# Chat interface
st.markdown("---")
st.subheader("💬 Chat with Receptionist")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get and display assistant response
    response = handle_query(prompt, lang)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)

# Booking records
st.markdown("---")
st.subheader("📋 Recent Bookings")
if st.checkbox("Show booking records"):
    bookings = cursor.execute("""
        SELECT guest_count, room_type, checkin_date, checkout_date, language, timestamp 
        FROM bookings 
        ORDER BY timestamp DESC 
        LIMIT 10
    """).fetchall()
    
    if bookings:
        df = pd.DataFrame(bookings, columns=["Guests", "Room Type", "Check-in", "Check-out", "Language", "Timestamp"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No bookings found.") 