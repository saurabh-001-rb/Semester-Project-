import streamlit as st
import pyautogui
import pyperclip
import time
import google.generativeai as genai

# ─────────────────────────────────────────────────────
# CONFIGURATION
genai.configure(api_key="YOUR_API_KEY_HERE")  # Replace with your API key
model = genai.GenerativeModel("gemini-1.5-flash")

# ─────────────────────────────────────────────────────
# STREAMLIT PAGE SETTINGS
st.set_page_config(page_title="WhatsApp Chatbot", layout="wide")
st.title("🤖💬 WhatsApp AI Chatbot")
st.caption("Auto-reply bot powered by Google Gemini + Streamlit UI")
st.markdown("---")

# ─────────────────────────────────────────────────────
# SESSION STATE INIT
if "message" not in st.session_state:
    st.session_state.message = ""
if "reply" not in st.session_state:
    st.session_state.reply = ""
if "last_sent_reply" not in st.session_state:
    st.session_state.last_sent_reply = ""

# ─────────────────────────────────────────────────────
# FUNCTION TO FETCH LATEST MESSAGE FROM WHATSAPP
def fetch_message_from_whatsapp():
    try:
        pyautogui.click(1302, 1055)  # Focus WhatsApp window (adjust coords)
        time.sleep(1.2)
        pyautogui.moveTo(757, 190)
        pyautogui.dragTo(1689, 939, duration=1.0, button='left')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        return pyperclip.paste()
    except Exception as e:
        return f"⚠️ Error fetching message: {e}"

# ─────────────────────────────────────────────────────
# FUNCTION TO GENERATE GEMINI REPLY
def generate_reply_with_gemini(message):
    prompt = f"""
Generate a natural, short, smart WhatsApp response in **Marathi, Hindi, or English**:

**Message:** {message}  

### Guidelines:
- Be friendly and casual (like real chat)
- Use only ONE language
- Keep it SHORT and NATURAL
- Use emojis/slang when needed
- Don’t repeat or explain message
"""
    try:
        response = model.generate_content(prompt)
        if hasattr(response, "text"):
            return response.text.strip().split("\n")[0]
        return "🤔 Blank reply received."
    except Exception as e:
        return f"⚠️ Error generating reply: {e}"

# ─────────────────────────────────────────────────────
# FUNCTION TO SEND MESSAGE TO WHATSAPP
def send_reply_to_whatsapp(reply):
    try:
        pyautogui.click(1185, 736)
        time.sleep(0.5)
        pyperclip.copy(reply)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.4)
        pyautogui.press('enter')
        st.session_state.last_sent_reply = reply
        return "✅ Reply sent to WhatsApp!"
    except Exception as e:
        return f"⚠️ Error sending message: {e}"

# ─────────────────────────────────────────────────────
# MAIN UI LAYOUT
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Step 1: Fetch Message")
    if st.button("Fetch Latest Message"):
        st.session_state.message = fetch_message_from_whatsapp()
        st.success("Message fetched successfully!")

    if st.session_state.message:
        st.text_area("Incoming Message", st.session_state.message, height=150)

with col2:
    st.subheader("⚡ Step 2: Generate Reply")
    if st.session_state.message and st.button("Generate AI Reply"):
        st.session_state.reply = generate_reply_with_gemini(st.session_state.message)
        st.success("Reply generated with Gemini AI")

    if st.session_state.reply:
        st.text_area("AI Reply", st.session_state.reply, height=150)

# SEND BUTTON AT BOTTOM
st.markdown("---")
if st.session_state.reply and st.button("📤 Send Reply to WhatsApp"):
    result = send_reply_to_whatsapp(st.session_state.reply)
    st.success(result)

# Show last sent reply
if st.session_state.last_sent_reply:
    st.markdown(f"🕓 **Last Sent Reply:** _{st.session_state.last_sent_reply}_")

# Optional Instructions Expander
with st.expander("ℹ️ How It Works"):
    st.markdown("""
    1. **Click "Fetch Message"**: It copies the latest message from the WhatsApp window.
    2. **Click "Generate Reply"**: It sends the message to Gemini AI and gets a smart reply.
    3. **Click "Send Reply"**: It pastes the reply into WhatsApp and presses Enter to send.

    > Make sure WhatsApp is **open** and positioned as expected (or adjust pyautogui coordinates).
    """)

