import pyautogui
import time
import pyperclip
import google.generativeai as genai  # Correct import

# Set up Gemini API
genai.configure(api_key="AIzaSyCohTBXo8rbb-An7WWMIom2hEGfy1ma6dA")  # Replace with your actual API key

# Function to generate response
def generate_reply(message):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the latest available model
    response = model.generate_content(message)
    return response.text.strip() if response else "Sorry, I couldn't understand."

# Step 1: Copy the message from WhatsApp
time.sleep(1)
pyautogui.click(1302, 1055)  # Click on WhatsApp window
time.sleep(2)
pyautogui.moveTo(757, 190)  # Move to message start
pyautogui.dragTo(1689, 939, duration=1.0, button='left')  # Select text
pyautogui.hotkey('ctrl', 'c')  # Copy text
time.sleep(1)

# Step 2: Retrieve the copied text
copied_text = pyperclip.paste()
print("Copied text:", copied_text)

copied_text = pyperclip.paste()
print("Copied text:", copied_text)

whatsapp_prompt = f"""Generate a natural Responce only in Marathi OR Hindi last or in English any one language, human-like WhatsApp response to the following message:  

Message: {copied_text}  

Your response should sound like a casual text message from a real person, using informal language, abbreviations, emojis (if needed), and natural chat expressions. Keep it short, natural, and engaging. Avoid overly formal or robotic phrasing.  

- If the message is very short (e.g., "ok", "hmm", "gn"), reply with a quick, natural acknowledgment.  
- If the message is part of a conversation, respond in a way that continues the flow.  
- If the message is a question, reply in a way a friend would, keeping it casual.  

### Examples:  

1️⃣ Message: "Bbye gn🤓
"  
   Reply: "Itkya lavkar gn😂🥲"  

2️⃣ Message: "Bghel jaude"  
   Reply: "Ho tech nn, bagh ata tine tula sangitla"  

3️⃣ Message: "Hello! How can you assist me today?"  
   Reply: "Bol na, kay help pahije?"  

4️⃣ Message: "What’s the weather like today?"  
   Reply: "Kuthay aahes? Baghto mg update deto"  

5️⃣ Message: "Tell me a joke."  
   Reply: "😂 Aai mhanti chaha ghe, me mhanto net slow ahe!"  

Maintain the same tone and style as a real WhatsApp chat between friends or acquaintances. Avoid generic AI-sounding responses—make it feel personal and engaging."""

# Step 3: Generate AI response
reply = generate_reply(whatsapp_prompt)
print("Generated Reply:", reply)

# Step 4: Send the reply back to WhatsApp
pyautogui.click(1185, 736)  # Click on chat input box
time.sleep(1)
pyperclip.copy(reply)  # Copy reply to clipboard
pyautogui.hotkey('ctrl', 'v')  # Paste reply
time.sleep(1)
pyautogui.press('enter')  # Send message

print("Reply sent successfully!")
