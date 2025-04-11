import streamlit as st
import hashlib
import json
import os
from cryptography.fernet import Fernet, InvalidToken

# ------------------ Configurations ------------------
st.set_page_config(page_title="🔐 Secure Vault App", layout="centered")

# ------------------ Custom UI Styling ------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #000000, #434343);
        color: white;
        border-right: 3px solid #6c63ff;
        padding-top: 20px;
    }
  
            


    section[data-testid="stSidebar"] .block-container {
        padding-top: 40px;
        padding-bottom: 20px;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .st-radio,
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stButton {
        color: white !important;
    }

    .stButton > button {
        background: linear-gradient(to right, #ff512f, #dd2476);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease-in-out;
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #00b09b, #96c93d);
        transform: scale(1.05);
    }

    .stTextInput > div > input,
    .stTextArea textarea {
        background-color: #ffffffcc;
        border: 2px solid #6c63ff;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-weight: 500;
        color: #222;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .stTextInput > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #00b09b;
        outline: none;
        box-shadow: 0px 0px 5px rgba(0,176,155,0.5);
    }

    .stCode {
        background-color: #f0fff0 !important;
        border: 1px solid #c8e6c9 !important;
        border-radius: 10px;
        padding: 1rem;
        font-size: 14px;
    }

    .stAlert {
        border-radius: 10px;
        padding: 1rem;
    }
                .custom-subtitle {
        font-size: 20px !important;
        color: black !important;
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 20px;
    }
            .custom-subtitle {
            font-size: 20px;
            color: black;
            font-weight: 500;
            margin-bottom: 15px;
        }
          
   
            
    </style>
 <p class="custom-subtitle">🔒🌫 "Smart Security for Your Sensitive Information"</p>
""", unsafe_allow_html=True)

# ------------------ File Paths ------------------
USERS_FILE = "users.json"
VAULT_FILE = "vault.json"

# ------------------ Helpers ------------------
def load_file(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_file(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_cipher(key):
    return Fernet(key.encode())

# ------------------ Session States ------------------
if "username" not in st.session_state:
    st.session_state.username = None

users = load_file(USERS_FILE)
vault = load_file(VAULT_FILE)

# ------------------ App Title ------------------
st.title("🧠 AI Secure Vault")
st.caption("🔒🦠 Trusted Partner Encrypt and Decrypt Data with Confidence " )


# ------------------ Navigation Sidebar ------------------
st.sidebar.markdown("## 🔐 Vault Menu")
choice = st.sidebar.radio("📁 Select an option:", [
    "📝  Register",

    "🔐  Login",

    "🧳   My Vault",

    "📜  All Users"
])

# ------------------ Register ------------------
if choice.startswith("📝"):
    st.subheader("📝 Create a New Account")
    new_user = st.text_input("👤 Enter Username")
    new_email = st.text_input("📧 Enter Email")
    new_pass = st.text_input("🔑 Enter Password", type="password")

    if new_user and new_email and new_pass:
        if "@" not in new_email:
            st.error("❌ Please enter a valid email address.")
        elif len(new_pass) < 6:
            st.error("❌ Password must be at least 6 characters long.")
        elif new_user in users:
            st.error("❌ Username already exists. Try a new one.")
        else:
            if st.button("🚀 Register"):
                key = Fernet.generate_key().decode()
                users[new_user] = {
                    "email": new_email,
                    "password": hash_password(new_pass),
                    "key": key
                }
                save_file(USERS_FILE, users)
                st.success("✅ Account created successfully!")
    elif st.button("🚀 Register"):
        st.warning("⚠️ All fields are required to register.")

# ------------------ Login ------------------
elif choice.startswith("🔐"):
    st.subheader("🔓 Login to Your Vault")
    email = st.text_input("📧 Enter Email")
    password = st.text_input("🔑 Enter Password", type="password")

    if email and password:
        if "@" not in email:
            st.error("❌ Please enter a valid email address.")
        else:
            if st.button("🔐 Login"):
                user = None
                for username, data in users.items():
                    if "email" in data and data["email"] == email:
                        user = username
                        break
                if user and users[user]["password"] == hash_password(password):
                    st.session_state.username = user
                    st.success(f"🚀 Good to see you, Asia🎈🎉! Time to safeguard your secrets.")
                    st.balloons()
                else:
                    st.error("❌ Invalid email or password.")
    elif st.button("🔐 Login"):
        st.warning("⚠️ Please enter both email and password.")

# ------------------ My Vault ------------------
elif choice.startswith("🧳"):
    if st.session_state.username:
        st.subheader(f"🧳 Vault for {st.session_state.username}")
        user_key = users[st.session_state.username]["key"]
        cipher = get_cipher(user_key)

        tab1, tab2 = st.tabs(["📥 Store Data", "🔍 Retrieve Data"])

        with tab1:
            data = st.text_area("🗝️ Enter your secret data:")
            if st.button("💾 Encrypt & Save"):
                if data:
                    encrypted = cipher.encrypt(data.encode()).decode()
                    vault[st.session_state.username] = encrypted
                    save_file(VAULT_FILE, vault)
                    st.success("🔒 Your data has been securely locked away!")
                    st.code(encrypted, language="text")
                else:
                    st.warning("⚠️ Please enter some data to encrypt.")

        with tab2:
            if st.button("🔓 Decrypt My Data"):
                encrypted = vault.get(st.session_state.username)
                if encrypted:
                    try:
                        decrypted = cipher.decrypt(encrypted.encode()).decode()
                        st.success("🔓 Here's your unlocked secret message:")
                        st.code(decrypted)
                    except InvalidToken:
                        st.error("❌ Unable to decrypt. Data might be corrupted.")
                else:
                    st.info("ℹ️ No data found for this user.")
    else:
        st.warning("🔐 Please login first to access your vault.")

    st.markdown("---")
    st.subheader("⚙️ Account Options")

    logout_label = f"🚪 Log out {st.session_state.username} & 🗑️ Delete My Data"
    if st.button(logout_label, use_container_width=True):
        username = st.session_state.username
        if username in vault:
            del vault[username]
            save_file(VAULT_FILE, vault)
        st.session_state.username = None
        st.success("👋 You've been logged out. Your vault has been cleared!")
        st.balloons()

# ------------------ All Users ------------------
elif choice.startswith("📜"):
    st.subheader("👥 Registered Users")
    if users:
        for username, data in users.items():
            email = data.get('email', 'No email provided')
            st.markdown(f"✅ **{email}**")
    else:
        st.info("🚫 No users registered yet.")




# import streamlit as st
# import hashlib
# import json
# import os
# from cryptography.fernet import Fernet, InvalidToken

# # ------------------ Configurations ------------------
# st.set_page_config(page_title="🔐 Secure Vault App", layout="centered")

# # ------------------ Custom UI Styling ------------------
# st.markdown("""
#     <style>
#     body {
#         background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
#         background-attachment: fixed;
#         font-family: 'Segoe UI', sans-serif;
#     }

#     section[data-testid="stSidebar"] {
#         background: linear-gradient(to bottom, #000000, #434343);
#         color: white;
#         border-right: 3px solid #6c63ff;
#         padding-top: 20px;
#     }

#     .stButton > button {
#         background: linear-gradient(to right, #ff512f, #dd2476);
#         color: white;
#         font-weight: 600;
#         border: none;
#         border-radius: 12px;
#         padding: 0.6rem 1.2rem;
#         transition: all 0.3s ease-in-out;
#     }

#     .stButton > button:hover {
#         background: linear-gradient(to right, #00b09b, #96c93d);
#         transform: scale(1.05);
#     }

#     .stTextInput > div > input,
#     .stTextArea textarea {
#         background-color: #ffffffcc;
#         border: 2px solid #6c63ff;
#         border-radius: 12px;
#         padding: 0.75rem 1rem;
#         font-weight: 500;
#         color: #222;
#         box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
#         transition: all 0.3s ease;
#     }

#     .stTextInput > div > input:focus,
#     .stTextArea textarea:focus {
#         border-color: #00b09b;
#         outline: none;
#         box-shadow: 0px 0px 5px rgba(0,176,155,0.5);
#     }

#     .stCode {
#         background-color: #f0fff0 !important;
#         border: 1px solid #c8e6c9 !important;
#         border-radius: 10px;
#         padding: 1rem;
#         font-size: 14px;
#     }

#     .stAlert {
#         border-radius: 10px;
#         padding: 1rem;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ------------------ File Paths ------------------
# USERS_FILE = "users.json"
# VAULT_FILE = "vault.json"

# # ------------------ Helpers ------------------
# def load_file(filename):
#     if os.path.exists(filename):
#         with open(filename, "r") as f:
#             return json.load(f)
#     return {}

# def save_file(filename, data):
#     with open(filename, "w") as f:
#         json.dump(data, f, indent=4)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def get_cipher(key):
#     return Fernet(key.encode())

# # ------------------ Session States ------------------
# if "username" not in st.session_state:
#     st.session_state.username = None

# users = load_file(USERS_FILE)
# vault = load_file(VAULT_FILE)

# # ------------------ App Title ------------------
# st.title("🧠 AI Secure Vault")
# st.caption("🔒 Encrypt and Decrypt Data with Confidence")

# # ------------------ Navigation Sidebar ------------------
# st.sidebar.markdown("## 🔐 Vault Menu")
# choice = st.sidebar.radio("📁 Select an option:", [
#     "📝 Register",
#     "🔐 Login",
#     "🧳 My Vault",
#     "📜 All Users"
# ])

# # ------------------ Register ------------------
# if choice.startswith("📝"):
#     st.subheader("📝 Create a New Account")
#     new_user = st.text_input("👤 Enter Username")
#     new_email = st.text_input("📧 Enter Email")
#     new_pass = st.text_input("🔑 Enter Password", type="password")

#     if new_user and new_email and new_pass:
#         if "@" not in new_email:
#             st.error("❌ Please enter a valid email address.")
#         elif len(new_pass) < 6:
#             st.error("❌ Password must be at least 6 characters long.")
#         elif new_user in users:
#             st.error("❌ Username already exists. Try a new one.")
#         else:
#             if st.button("🚀 Register"):
#                 key = Fernet.generate_key().decode()
#                 users[new_user] = {
#                     "email": new_email,
#                     "password": hash_password(new_pass),
#                     "key": key
#                 }
#                 save_file(USERS_FILE, users)
#                 st.success("✅ Account created successfully!")
#     elif st.button("🚀 Register"):
#         st.warning("⚠️ All fields are required to register.")

# # ------------------ Login ------------------
# elif choice.startswith("🔐"):
#     st.subheader("🔓 Login to Your Vault")
#     email = st.text_input("📧 Enter Email")
#     password = st.text_input("🔑 Enter Password", type="password")

#     if email and password:
#         if "@" not in email:
#             st.error("❌ Please enter a valid email address.")
#         else:
#             if st.button("🔐 Login"):
#                 user = None
#                 for username, data in users.items():
#                     if "email" in data and data["email"] == email:
#                         user = username
#                         break
#                 if user and users[user]["password"] == hash_password(password):
#                     st.session_state.username = user
#                     st.success(f"🚀 Welcome back, {username}! Ready to vault your secrets?")
#                 else:
#                     st.error("❌ Invalid email or password.")
#     elif st.button("🔐 Login"):
#         st.warning("⚠️ Please enter both email and password.")

# # ------------------ My Vault ------------------
# elif choice.startswith("🧳"):
#     if st.session_state.username:
#         st.subheader(f"🧳 Vault for {st.session_state.username}")
#         user_key = users[st.session_state.username]["key"]
#         cipher = get_cipher(user_key)

#         tab1, tab2 = st.tabs(["📥 Store Data", "🔍 Retrieve Data"])

#         with tab1:
#             data = st.text_area("🗝️ Enter your secret data:")
#             if st.button("💾 Encrypt & Save"):
#                 if data:
#                     encrypted = cipher.encrypt(data.encode()).decode()
#                     vault[st.session_state.username] = encrypted
#                     save_file(VAULT_FILE, vault)
#                     st.success("🔒 Your data has been securely locked away!")
#                     st.code(encrypted, language="text")
#                 else:
#                     st.warning("⚠️ Please enter some data to encrypt.")

#         with tab2:
#             if st.button("🔓 Decrypt My Data"):
#                 encrypted = vault.get(st.session_state.username)
#                 if encrypted:
#                     try:
#                         decrypted = cipher.decrypt(encrypted.encode()).decode()
#                         st.success("🔓 Here's your unlocked secret message:")
#                         st.code(decrypted)
#                     except InvalidToken:
#                         st.error("❌ Unable to decrypt. Data might be corrupted.")
#                 else:
#                     st.info("ℹ️ No data found for this user.")
#     else:
#         st.warning("🔐 Please login first to access your vault.")

#     st.markdown("---")
#     st.subheader("⚙️ Account Options")

#     if st.button("🚪 Logout & 🗑️ Delete My Data", use_container_width=True):
#         username = st.session_state.username
#         if username in vault:
#             del vault[username]
#             save_file(VAULT_FILE, vault)
#         st.session_state.username = None
#         st.success("👋 You've been logged out. Your vault has been cleared!")
#         st.balloons()

# # ------------------ All Users ------------------
# elif choice.startswith("📜"):
#     st.subheader("👥 Registered Users")
#     if users:
#         for username, data in users.items():
#             email = data.get('email', 'No email provided')
#             st.markdown(f"✅ **{email}**")
#     else:
#         st.info("🚫 No users registered yet.")




# import streamlit as st
# import hashlib
# import json
# import os
# from cryptography.fernet import Fernet, InvalidToken

# # ------------------ Configurations ------------------
# st.set_page_config(page_title="🔐 Secure Vault App", layout="centered")

# # ------------------ Custom UI Styling ------------------
# st.markdown("""
#     <style>
#     body {
#         background: linear-gradient(135deg, #e0c3fc, #8ec5fc);
#         background-attachment: fixed;
#         font-family: 'Segoe UI', sans-serif;
#     }

#     section[data-testid="stSidebar"] {
#         background: linear-gradient(to bottom, #000000, #434343);
#         color: white;
#         border-right: 3px solid #6c63ff;
#         padding-top: 20px;
#     }

#     .stButton > button {
#         background: linear-gradient(to right, #ff512f, #dd2476);
#         color: white;
#         font-weight: 600;
#         border: none;
#         border-radius: 12px;
#         padding: 0.6rem 1.2rem;
#         transition: all 0.3s ease-in-out;
#     }

#     .stButton > button:hover {
#         background: linear-gradient(to right, #00b09b, #96c93d);
#         transform: scale(1.05);
#     }

#     .stTextInput > div > input,
#     .stTextArea textarea {
#         background-color: #ffffffdd;
#         border: 2px solid #6c63ff;
#         border-radius: 10px;
#         padding: 10px;
#         font-weight: 500;
#         color: #333;
#     }

#     .stCode {
#         background-color: #f0fff0 !important;
#         border: 1px solid #c8e6c9 !important;
#         border-radius: 10px;
#         padding: 1rem;
#         font-size: 14px;
#     }

#     .stAlert {
#         border-radius: 10px;
#         padding: 1rem;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ------------------ File Paths ------------------
# USERS_FILE = "users.json"
# VAULT_FILE = "vault.json"

# # ------------------ Helpers ------------------
# def load_file(filename):
#     if os.path.exists(filename):
#         with open(filename, "r") as f:
#             return json.load(f)
#     return {}

# def save_file(filename, data):
#     with open(filename, "w") as f:
#         json.dump(data, f, indent=4)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def get_cipher(key):
#     return Fernet(key.encode())

# # ------------------ Session States ------------------
# if "username" not in st.session_state:
#     st.session_state.username = None

# users = load_file(USERS_FILE)
# vault = load_file(VAULT_FILE)

# # ------------------ App Title ------------------
# st.title("🧠 AI Secure Vault")
# st.caption("🔒 Encrypt and Decrypt Data with Confidence")

# # ------------------ Navigation ------------------
# menu = ["Register", "Login", "My Vault", "All Users"]
# choice = st.sidebar.selectbox("🌈 Navigation", menu)

# # ------------------ Register ------------------
# if choice == "Register":
#     st.subheader("📝 Create a New Account")
#     new_user = st.text_input("👤 Username")
#     new_email = st.text_input("📧 Email")
#     new_pass = st.text_input("🔑 Password", type="password")

#     if new_user and new_email and new_pass:
#         if "@" not in new_email:
#             st.error("❌ Please enter a valid email address.")
#         elif len(new_pass) < 6:
#             st.error("❌ Password must be at least 6 characters long.")
#         elif new_user in users:
#             st.error("❌ Username already exists. Try a new one.")
#         else:
#             if st.button("🚀 Register"):
#                 key = Fernet.generate_key().decode()
#                 users[new_user] = {
#                     "email": new_email,
#                     "password": hash_password(new_pass),
#                     "key": key
#                 }
#                 save_file(USERS_FILE, users)
#                 st.success("✅ Account created successfully!")
#     elif st.button("🚀 Register"):
#         st.warning("⚠️ All fields are required to register.")

# # ------------------ Login ------------------
# elif choice == "Login":
#     st.subheader("🔓 Login to Your Vault")
#     email = st.text_input("📧 Email")
#     password = st.text_input("🔑 Password", type="password")

#     if email and password:
#         if "@" not in email:
#             st.error("❌ Please enter a valid email address.")
#         else:
#             if st.button("🔐 Login"):
#                 user = None
#                 for username, data in users.items():
#                     if "email" in data and data["email"] == email:
#                         user = username
#                         break
#                 if user and users[user]["password"] == hash_password(password):
#                     st.session_state.username = user
#                     st.success(f"🚀 Welcome aboard, {username}! Ready to vault your secrets?")
#                 else:
#                     st.error("❌ Invalid email or password.")
#     elif st.button("🔐 Login"):
#         st.warning("⚠️ Please enter both email and password.")

# # ------------------ My Vault ------------------
# elif choice == "My Vault":
#     if st.session_state.username:
#         st.subheader(f"🧳 Vault for {st.session_state.username}")
#         user_key = users[st.session_state.username]["key"]
#         cipher = get_cipher(user_key)

#         tab1, tab2 = st.tabs(["🗂️ Store Data", "🔍 Retrieve Data"])

#         with tab1:
#             data = st.text_area("📥 Enter your secret data:")
#             if st.button("💾 Encrypt & Save"):
#                 if data:
#                     encrypted = cipher.encrypt(data.encode()).decode()
#                     vault[st.session_state.username] = encrypted
#                     save_file(VAULT_FILE, vault)
#                     st.success("📦 Your data has been securely locked away!")
#                     st.code(encrypted, language="text")
#                 else:
#                     st.warning("⚠️ Please enter some data to encrypt.")

#         with tab2:
#             if st.button("🔓 Decrypt My Data"):
#                 encrypted = vault.get(st.session_state.username)
#                 if encrypted:
#                     try:
#                         decrypted = cipher.decrypt(encrypted.encode()).decode()
#                         st.success("🔓 Here's your unlocked secret message:")
#                         st.code(decrypted)
#                     except InvalidToken:
#                         st.error("❌ Unable to decrypt. Data might be corrupted.")
#                 else:
#                     st.info("ℹ️ No data found for this user.")
#     else:
#         st.warning("🔐 Please login first to access your vault.")

#     st.markdown("---")
#     st.subheader("⚙️ Account Options")

#     if st.button("🚪 Logout & 🗑️ Delete My Data", use_container_width=True):
#         username = st.session_state.username
#         if username in vault:
#             del vault[username]
#             save_file(VAULT_FILE, vault)
#         st.session_state.username = None
#         st.success("👋 You've been logged out. Your vault has been cleared!")
#         st.balloons()

# # ------------------ All Users ------------------
# elif choice == "All Users":
#     st.subheader("👥 Registered Users")
#     if users:
#         for username, data in users.items():
#             email = data.get('email', 'No email provided')
#             st.markdown(f"✅ **{email}**")
#     else:
#         st.info("🚫 No users registered yet.")






# import streamlit as st
# import hashlib
# import json
# import os
# from cryptography.fernet import Fernet, InvalidToken



# # ------------------ Configurations ------------------
# st.set_page_config(page_title="🔐 Secure Vault App", layout="centered")

# # ------------------ File Paths ------------------
# USERS_FILE = "users.json"
# VAULT_FILE = "vault.json"

# # ------------------ Helpers ------------------
# def load_file(filename):
#     if os.path.exists(filename):
#         with open(filename, "r") as f:
#             return json.load(f)
#     return {}

# def save_file(filename, data):
#     with open(filename, "w") as f:
#         json.dump(data, f, indent=4)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def get_cipher(key):
#     return Fernet(key.encode())

# # ------------------ Session States ------------------
# if "username" not in st.session_state:
#     st.session_state.username = None

# users = load_file(USERS_FILE)
# vault = load_file(VAULT_FILE)

# # ------------------ App Title ------------------
# st.title("🧠 AI Secure Vault")
# st.caption("🔒 Encrypt and Decrypt Data with Confidence")

# # ------------------ Navigation ------------------
# menu = ["Register", "Login", "My Vault", "All Users"]
# choice = st.sidebar.selectbox("🌈 Navigation", menu)

# # ------------------ Register ------------------
# if choice == "Register":
#     st.subheader("📝 Create a New Account")
#     new_user = st.text_input("👤 Username")
#     new_email = st.text_input("📧 Email")
#     new_pass = st.text_input("🔑 Password", type="password")

#     # Validation
#     if new_user and new_email and new_pass:
#         if "@" not in new_email:
#             st.error("❌ Please enter a valid email address.")
#         elif len(new_pass) < 6:
#             st.error("❌ Password must be at least 6 characters long.")
#         elif new_user in users:
#             st.error("❌ Username already exists. Try a new one.")
#         else:
#             if st.button("🚀 Register"):
#                 key = Fernet.generate_key().decode()
#                 users[new_user] = {
#                     "email": new_email,
#                     "password": hash_password(new_pass),
#                     "key": key
#                 }
#                 save_file(USERS_FILE, users)
#                 st.success("✅ Account created successfully!")
#     elif st.button("🚀 Register"):
#         st.warning("⚠️ All fields are required to register.")

# # ------------------ Login ------------------
# elif choice == "Login":
#     st.subheader("🔓 Login to Your Vault")
#     email = st.text_input("📧 Email")
#     password = st.text_input("🔑 Password", type="password")

#     # Validation
#     if email and password:
#         if "@" not in email:
#             st.error("❌ Please enter a valid email address.")
#         else:
#             if st.button("🔐 Login"):
#                 user = None
#                 # Search for user by email
#                 for username, data in users.items():
#                     if "email" in data and data["email"] == email:
#                         user = username
#                         break
#                 if user and users[user]["password"] == hash_password(password):
#                     st.session_state.username = user
#                     st.success(f"🚀 Welcome, {username}! Your journey to secure vaults begins now!")
#                 else:
#                     st.error("❌ Invalid email or password.")
#     elif st.button("🔐 Login"):
#         st.warning("⚠️ Please enter both email and password.")

# # ------------------ My Vault ------------------
# elif choice == "My Vault":
#     if st.session_state.username:
#         st.subheader(f"🧳 Vault for {st.session_state.username}")
#         user_key = users[st.session_state.username]["key"]
#         cipher = get_cipher(user_key)

#         tab1, tab2 = st.tabs(["🗂️ Store Data", "🔍 Retrieve Data"])

#         with tab1:
#             data = st.text_area("📥 Enter your secret data:")
#             if st.button("💾 Encrypt & Save"):
#                 if data:
#                     encrypted = cipher.encrypt(data.encode()).decode()
#                     vault[st.session_state.username] = encrypted
#                     save_file(VAULT_FILE, vault)
#                     st.success("✅ Success!  Your data is now encrypted and stored securely.")
#                     st.code(encrypted, language="text")
#                 else:
#                     st.warning("⚠️ Please enter some data to encrypt.")

#         with tab2:
#             if st.button("🔓 Decrypt My Data"):
#                 encrypted = vault.get(st.session_state.username)
#                 if encrypted:
#                     try:
#                         decrypted = cipher.decrypt(encrypted.encode()).decode()
#                         st.success("🔓 Here's your unlocked secret message!")
#                         st.code(decrypted)
#                     except InvalidToken:
#                         st.error("❌ Unable to decrypt. Data might be corrupted.")
#                 else:
#                     st.info("ℹ️ No data found for this user.")
#     else:
#         st.warning("🔐 Please login first to access your vault.")

#         st.markdown("---")
# st.subheader("⚙️ Account Options")

# if st.button("🚪 Logout & 🗑️ Delete My Data", use_container_width=True):
#     username = st.session_state.username
#     if username in vault:
#         del vault[username]
#         save_file(VAULT_FILE, vault)
#     st.session_state.username = None

#     st.success("👋 You have been logged out successfully, and your vault data has been securely deleted!")
#     st.balloons()


# # ------------------ All Users ------------------
# # ------------------ All Users ------------------
# elif choice == "All Users":
#     st.subheader("👥 Registered Users")
#     if users:
#         for username, data in users.items():
#             # Check if 'email' key exists in the user data
#             email = data.get('email', 'No email provided')  # Default message if email is missing
#             st.markdown(f"✅ **{email}**")
#     else:
#         st.info("🚫 No users registered yet.")













