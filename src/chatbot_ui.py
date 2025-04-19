import streamlit as st
import pyautogui
import time
import pyperclip
import google.generativeai as genai

# Set your actual Gemini API key
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-1.5-flash")

# Session states to store data
if "message" not in st.session_state:
    st.session_state.message = ""
if "reply" not in st.session_state:
    st.session_state.reply = ""
if "last_sent_reply" not in st.session_state:
    st.session_state.last_sent_reply = ""

# Function to fetch the latest WhatsApp message
def fetch_message_from_whatsapp():
    try:
        pyautogui.click(1302, 1055)  # Click on WhatsApp
        time.sleep(1.5)
        pyautogui.moveTo(757, 190)
        pyautogui.dragTo(1689, 939, duration=1.0, button='left')  # Select chat
        pyautogui.hotkey('ctrl', 'c')  # Copy
        time.sleep(0.5)
        return pyperclip.paste()
    except Exception as e:
        return f"Error fetching message: {e}"

# Function to generate reply using Gemini
def generate_reply_with_gemini(user_message):
    prompt = f"""
Generate a natural, short, smart WhatsApp response in **only one language** (Marathi, Hindi, or English) based on the following message:

**Message:** {user_message}  

### **Guidelines:**
- Keep it short, natural, and engaging.
- **DO NOT** repeat the user's message in the response.
- **DO NOT** add unnecessary details or explanations.
- **DO NOT** sound robotic; keep it casual, like a real WhatsApp chat.
- Use natural abbreviations, emojis (if needed), and friendly tones.
- If it's a **question**, answer briefly but **smartly**.
- If it's a **casual message**, respond in a natural, engaging way.
"""
    try:
        response = model.generate_content(prompt)
        if hasattr(response, "text"):
            return response.text.strip().split("\n")[0]
        else:
            return "🤔 Kai tari problem ahe reply madhe..."
    except Exception as e:
        return f"Error generating reply: {e}"

# Function to send reply back to WhatsApp
def send_reply_to_whatsapp(reply):
    try:
        pyautogui.click(1185, 736)  # Click message input
        time.sleep(0.5)
        pyperclip.copy(reply)
        pyautogui.hotkey('ctrl', 'v')  # Paste
        time.sleep(0.5)
        pyautogui.press('enter')  # Send
        st.session_state.last_sent_reply = reply
        return "✅ Reply sent!"
    except Exception as e:
        return f"Error sending reply: {e}"

# Streamlit UI
st.title("💬 WhatsApp Chatbot Dashboard")

st.markdown("This tool lets you fetch, respond, and send replies to WhatsApp chats using Google Gemini AI.")

# Step 1: Fetch message
if st.button("📥 Fetch Message"):
    st.session_state.message = fetch_message_from_whatsapp()
    st.success("Fetched latest WhatsApp message.")

# Display fetched message
if st.session_state.message:
    st.text_area("📨 Latest Message", st.session_state.message, height=100)

# Step 2: Generate reply
if st.session_state.message and st.button("⚡ Generate AI Reply"):
    st.session_state.reply = generate_reply_with_gemini(st.session_state.message)
    st.success("Generated reply using Gemini.")

# Display AI reply
if st.session_state.reply:
    st.text_area("🤖 AI Reply", st.session_state.reply, height=100)

# Step 3: Send reply
if st.session_state.reply and st.button("📤 Send Reply to WhatsApp"):
    result = send_reply_to_whatsapp(st.session_state.reply)
    st.success(result)

# Last sent reply
if st.session_state.last_sent_reply:
    st.markdown(f"🕓 **Last Sent Reply:** _{st.session_state.last_sent_reply}_")
