import pyautogui
import pyperclip
import google.generativeai as genai
import time

# === Gemini Setup ===
genai.configure(api_key="AIzaSyCohTBXo8rbb-An7WWMIom2hEGfy1ma6dA")
your_name = "Saurabh"

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[
    {"role": "user", "parts": [
        f"""You are Saurabh chatting on WhatsApp.

Rules:
- Only reply if the last message is from the other person.
- Keep replies short, smart, and mature.
- Use just one language (Marathi, Hindi, or English).
- Don't exaggerate or repeat user messages.
"""
    ]},
    {"role": "model", "parts": ["Understood. Will only reply to valid messages from others."]}
])

# === Memory Tracking ===
last_full_chat = ""
last_reply = ""

# === WhatsApp focus once ===
print("📲 Focusing WhatsApp window...")
pyautogui.click(1252, 1053)  # Replace with WhatsApp window position
time.sleep(1)

# ✅ Replace this with your safe neutral coordinate found from step 1
NEUTRAL_CLICK_POINT = (1100, 400)

# === Function to get chat text ===
def get_chat_text():
    pyautogui.moveTo(784, 205)
    pyautogui.dragTo(1780, 971, duration=1.0, button='left')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    pyautogui.click(NEUTRAL_CLICK_POINT)  # ✅ Deselect selection safely
    time.sleep(0.2)
    return pyperclip.paste().strip()

# === Function to generate reply ===
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

# === Main Monitoring Loop ===
print("🤖 WhatsApp bot is running...")

while True:
    try:
        current_chat = get_chat_text()

        if current_chat != last_full_chat:
            old_lines = last_full_chat.splitlines()
            new_lines = current_chat.splitlines()

            new_msgs = [line for line in new_lines if line not in old_lines]

            if new_msgs:
                last_line = new_msgs[-1]

                if not last_line.startswith(your_name + ":"):
                    reply = generate_reply(last_line)

                    if reply:
                        pyautogui.click(842, 971)  # Input box
                        time.sleep(0.3)
                        pyperclip.copy(reply)
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(0.3)
                        pyautogui.press('enter')
                        print(f"✅ Replied: {reply}")
                    else:
                        print("🛑 No valid reply generated.")
                else:
                    print("🛑 Last message is from you. Skipping reply.")

            last_full_chat = current_chat
        else:
            print("⏳ No new messages.")

        time.sleep(10)

    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(5)