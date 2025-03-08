import streamlit as st
import random
import string
import re
import sqlite3

# Function to check password strength
def check_password_strength(password):
    strength = 0
    feedback = []
    
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("🔴 Password should be at least 8 characters long.")
    
    if re.search(r'[A-Z]', password):
        strength += 1
    else:
        feedback.append("🔴 Add at least one uppercase letter (A-Z).")
    
    if re.search(r'[a-z]', password):
        strength += 1
    else:
        feedback.append("🔴 Add at least one lowercase letter (a-z).")
    
    if re.search(r'\d', password):
        strength += 1
    else:
        feedback.append("🔴 Add at least one number (0-9).")
    
    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        strength += 1
    else:
        feedback.append("🔴 Add at least one special character (!@#$%^&* etc.).")
    
    return strength, feedback

# Function to generate a random password
def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    if length < 6:
        return "❌ Password length should be at least 6 characters!"
    
    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*(),.?\":{}|<>"
    
    if not characters:
        return "❌ Please select at least one character type!"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Database setup
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        site_name TEXT,
                        username TEXT,
                        password TEXT
                      )''')
    conn.commit()
    conn.close()

def save_password(site, username, password):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (site_name, username, password) VALUES (?, ?, ?)", 
                   (site, username, password))
    conn.commit()
    conn.close()

def get_saved_passwords():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT site_name, username, password FROM passwords")
    data = cursor.fetchall()
    conn.close()
    return data

# Initialize database
init_db()

# Streamlit UI
st.title("🔐 Password Manager & Strength Checker")

# Sidebar for Developer Info
st.sidebar.title("👨‍💻 About the Developer")
st.sidebar.write("**Name:** Fahad Khakwani")
st.sidebar.write("[GitHub](https://github.com/yourgithub)")
st.sidebar.write("[Vercel](https://vercel.com/yourvercel)")
st.sidebar.write("[LinkedIn](https://www.linkedin.com/in/fahad-khakwani-3aa655265/)")
st.sidebar.write("📞 Contact: +1234567890")
st.sidebar.write("✉ Email: fahad@example.com")
st.sidebar.write("🛠 Version: 1.0.1")

# Password Strength Checker
st.subheader("📏 Check Password Strength")
password = st.text_input("Enter your password:", type="password")

if password:
    strength, feedback = check_password_strength(password)
    
    if strength == 5:
        st.success("✅ Strong Password 💪")
    elif strength >= 3:
        st.warning("⚠ Medium Password 🟡")
    else:
        st.error("❌ Weak Password 🔴")

    if feedback:
        st.subheader("❗ Tips to Improve Password Strength:")
        for tip in feedback:
            st.write(tip)

# Password Generator
st.subheader("🔑 Generate a Secure Password")
password_length = st.slider("Select password length:", min_value=6, max_value=16, value=12)
use_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
use_lower = st.checkbox("Include Lowercase Letters (a-z)", value=True)
use_digits = st.checkbox("Include Numbers (0-9)", value=True)
use_special = st.checkbox("Include Special Characters (!@#$%^&*)", value=True)

if st.button("Generate Password"):
    new_password = generate_password(password_length, use_upper, use_lower, use_digits, use_special)
    st.success(f"🔐 Generated Password: `{new_password}`")
    st.code(new_password, language="")

# Save Password
st.subheader("💾 Save a Password")
site_name = st.text_input("Website/App Name")
username = st.text_input("Username")
password_to_save = st.text_input("Password", type="password")

if st.button("Save Password"):
    if site_name and username and password_to_save:
        save_password(site_name, username, password_to_save)
        st.success("✅ Password saved successfully!")
    else:
        st.warning("⚠ Please fill in all fields.")

# Display Saved Passwords
st.subheader("🔍 View Saved Passwords")

if "show_passwords" not in st.session_state:
    st.session_state.show_passwords = False

if st.button("Show Saved Passwords"):
    st.session_state.show_passwords = not st.session_state.show_passwords

if st.session_state.show_passwords:
    saved_passwords = get_saved_passwords()
    if saved_passwords:
        for site, username, password in saved_passwords:
            st.write(f"**Site:** {site}")
            st.write(f"**Username:** {username}")
            st.write(f"**Password:** `{password}`")
            st.markdown("---")
    else:
        st.info("No saved passwords found.")

st.markdown("🔒 **Always use a strong and unique password to stay safe online!**")
