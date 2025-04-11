import pyautogui
import time
import pyperclip
import google.generativeai as genai  # type: ignore # Correct import

# Set up Gemini API (Replace with your actual API key)
genai.configure(api_key="AIzaSyCohTBXo8rbb-An7WWMIom2hEGfy1ma6dA")

# Global variable to track last message
last_message = ""

# Function to generate response
def generate_reply(message):
    global last_message
    model = genai.GenerativeModel("gemini-1.5-flash")  # Using the latest available model
    response = model.generate_content(message)
    
    if response and hasattr(response, "text"):
        reply_text = response.text.strip().split("\n")[0]  # Take only the first meaningful line

        # Prevent repeating the same message
        if reply_text == last_message:
            return "🤔 Kai tari navin bol na!"
        
        last_message = reply_text  # Store last message
        return reply_text
    else:
        return "🤔 Nusta blank msg pathavlas ka?"

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

# Step 3: Define the WhatsApp-style prompt
whatsapp_prompt = f"""
Generate a natural, short, smart WhatsApp response in **only one language** (Marathi, Hindi, or English) based on the following message:

**Message:** {copied_text}  

### **Guidelines:**
- Keep it short, natural, and engaging.
- **DO NOT** repeat the user's message in the response.
- **DO NOT** add unnecessary details or explanations.
- **DO NOT** sound robotic; keep it casual, like a real WhatsApp chat.
- Use natural abbreviations, emojis (if needed), and friendly tones.
- If it's a **question**, answer briefly but **smartly**.
- If it's a **casual message**, respond in a natural, engaging way.

### **Examples:**
1️⃣ **Message:** "Bbye gn🤓"  
   ✅ **Reply:** "Itkya lavkar gn😂🥲"  

2️⃣ **Message:** "What’s the weather like today?"  
   ✅ **Reply:** "Kuthay aahes? Baghto mg update deto"  

3️⃣ **Message:** "Aaj ka plan kya hai?"  
   ✅ **Reply:** "Kalach fix nahi zhala re, boltu mg"  

4️⃣ **Message:** "Tell me a joke."  
   ✅ **Reply:** "😂 Aai mhanti chaha ghe, me mhanto net slow ahe!"  

Generate a **single, short, natural** reply that fits the message context.
"""

# Step 4: Generate AI response
reply = generate_reply(whatsapp_prompt)
print("Generated Reply:", reply)

# Step 5: Send the reply back to WhatsApp
pyautogui.click(1185, 736)  # Click on chat input box
time.sleep(1)
pyperclip.copy(reply)  # Copy reply to clipboard
pyautogui.hotkey('ctrl', 'v')  # Paste reply
time.sleep(1)
pyautogui.press('enter')  # Send message

print("Reply sent successfully!")
