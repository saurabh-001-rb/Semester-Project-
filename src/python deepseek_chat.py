from dotenv import load_dotenv
import os
import requests

# Step 1: Load the .env file
load_dotenv()

# Step 1: Set your API key as an environment variable
# Run this in your terminal before executing the script:
# export DEEPSEEK_API_KEY="your-new-api-key"

# Step 2: Load the API key from the environment variable
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("Please set the DEEPSEEK_API_KEY environment variable.")

# Step 3: Define the API endpoint and headers
api_url = "https://api.deepseek.com/v1/chat/completions"  
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Step 4: Define the request payload
payload = {
    "model": "deepseek-1.0",  # Replace with the correct DeepSeek model name
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"question": "user", "content": "Write a haiku about AI."}
    ]
}

# Step 5: Make the API request
try:
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for bad status codes
    completion = response.json()

    # Step 6: Print the response
    print(completion['choices'][0]['message']['content'])

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


    