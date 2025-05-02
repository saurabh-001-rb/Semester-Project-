import streamlit as st
import pyautogui
import pyperclip
import google.generativeai as genai
import time
import threading

# === Gemini Setup ===
genai.configure(api_key="AIzaSyCohTBXo8rbb-An7WWMIom2hEGfy1ma6dA")  # Replace with your real API key
your_name = "Saurabh"

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[
    {"role": "user", "parts": [f"""
You are Saurabh chatting on WhatsApp.

Rules:
- Only reply if the last message is from the other person.
- Keep replies short, smart, and mature.
- Use just one language (Marathi, Hindi, or English).
- Don't exaggerate or repeat user messages.
"""]},
    {"role": "model", "parts": ["Understood. Will only reply to valid messages from others."]}
])

# === Global State ===
last_full_chat = ""
last_reply = ""
bot_stop_event = threading.Event()
bot_thread = None

# === Thread-safe log storage ===
log_history = []
log_lock = threading.Lock()

def update_log(message):
    timestamped = f"{time.strftime('%H:%M:%S')} - {message}"
    with log_lock:
        log_history.append(timestamped)
        if len(log_history) > 100:
            log_history.pop(0)

# === Coordinates ===
WHATSAPP_CLICK_POINT = (1252, 1053)
NEUTRAL_CLICK_POINT = (1100, 400)
INPUT_BOX_COORDINATE = (842, 971)

# === Function to get chat text ===
def get_chat_text():
    try:
        print("📲 Focusing WhatsApp window...")
        pyautogui.click(WHATSAPP_CLICK_POINT)
        time.sleep(2)

        pyautogui.moveTo(784, 205)
        time.sleep(0.3)
        pyautogui.mouseDown()
        time.sleep(0.2)
        pyautogui.moveTo(1780, 971, duration=1.5)
        pyautogui.mouseUp()

        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.7)

        pyautogui.click(NEUTRAL_CLICK_POINT)
        time.sleep(0.2)

        chat_text = pyperclip.paste().strip()
        print("📋 Copied chat length:", len(chat_text))
        return chat_text

    except Exception as e:
        print("❌ Error in get_chat_text():", e)
        return ""

# === Gemini response ===
def generate_reply(message):
    global last_reply
    response = chat.send_message(message)
    if response and hasattr(response, "text"):
        reply = response.text.strip().split("\n")[0]
        if reply == last_reply or "no response" in reply.lower():
            return None
        last_reply = reply
        return reply
    return None

# === Bot Loop Thread ===
def bot_loop(log_callback):
    global last_full_chat
    log_callback("📡 Bot is monitoring WhatsApp...")

    while not bot_stop_event.is_set():
        try:
            current_chat = get_chat_text()
            log_callback("📋 Sample of chat: " + current_chat[:50])

            if current_chat != last_full_chat:
                old_lines = last_full_chat.splitlines()
                new_lines = current_chat.splitlines()
                new_msgs = [line for line in new_lines if line not in old_lines]

                if new_msgs:
                    last_line = new_msgs[-1]
                    if not last_line.startswith(your_name + ":"):
                        reply = generate_reply(last_line)
                        if reply:
                            pyautogui.click(INPUT_BOX_COORDINATE)
                            time.sleep(0.3)
                            pyperclip.copy(reply)
                            pyautogui.hotkey('ctrl', 'v')
                            time.sleep(0.3)
                            pyautogui.press('enter')
                            log_callback(f"✅ Replied: {reply}")
                        else:
                            log_callback("🛑 No valid reply generated.")
                    else:
                        log_callback("🛑 Last message is from you. Skipping.")
                last_full_chat = current_chat
            else:
                log_callback("⏳ No new messages.")
            time.sleep(5)

        except Exception as e:
            log_callback(f"⚠️ Error: {e}")
            time.sleep(5)

    log_callback("✅ Bot loop stopped.")

# === Streamlit UI ===
st.set_page_config(page_title="WhatsApp Bot", layout="centered")
st.title("🤖 WhatsApp ChatBot Controller")

if "status" not in st.session_state:
    st.session_state.status = "Stopped"

# === Buttons ===
if st.button("▶️ Start Bot"):
    if st.session_state.status == "Stopped":
        bot_stop_event.clear()
        bot_thread = threading.Thread(target=bot_loop, args=(update_log,))
        bot_thread.start()
        st.session_state.status = "Running"
        update_log("🚀 Bot started.")

if st.button("⏹ Stop Bot"):
    if st.session_state.status == "Running":
        bot_stop_event.set()
        st.session_state.status = "Stopped"
        update_log("🛑 Stop requested. Bot will shut down shortly.")

# === Status and Logs ===
st.write(f"**Bot Status**: {st.session_state.status}")
with log_lock:
    st.write("**Latest Logs:**")
    st.code("\n".join(log_history[-10:]), language="text")
