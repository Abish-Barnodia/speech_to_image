import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import requests       
from PIL import Image
import re

print("--- AI Speech to Image (Terminal Mode) ---")

# 1. Record Audio
fs = 44100
seconds = 8
print(f"Listening... Speak now! (Recording for {seconds} seconds)")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()
sf.write("temp_recording.wav", myrecording, fs)

# 2. Recognize Speech
print("Processing Speech...")
recognizer = sr.Recognizer()
with sr.AudioFile("temp_recording.wav") as Source:
    recognizer.adjust_for_ambient_noise(Source)
    audio = recognizer.record(Source)
    
try:
    text = recognizer.recognize_google(audio, language="en-US")
    print(f"I heard: '{text}'")
except sr.UnknownValueError:
    print("Error: Can't Understand. Please run the script again and speak clearly.")
    exit(1)
except sr.RequestError:
    print("Error: Speech API Error. Please check your internet connection.")
    exit(1)

# 3. Generate Image using Gemini API
print("Generating image via Gemini...")
Gemini_api_key = os.getenv("GEMINI_API_KEY")

if not Gemini_api_key:
    print("Error: GEMINI_API_KEY not found. Please set it in your .env file.")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={Gemini_api_key}"
headers = {"Content-Type": "application/json"}
data = {
    "contents": [{
        "parts": [{"text": f"Generate an image of: {text}. Return ONLY a markdown image link to pollinations.ai, like this: ![](https://image.pollinations.ai/prompt/YOUR_PROMPT_URL_ENCODED). Do not add any other text."}]
    }]
}

try:
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        try:
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            # Extract an image URL from the markdown response
            url_match = re.search(r'\((https?://[^\)]+)\)', content)
            if url_match:
                img_url = url_match.group(1)
                file_name = "image.jpg"
                img_response = requests.get(img_url)
                with open(file_name, 'wb') as file:
                    file.write(img_response.content)
                
                print("Done! Image downloaded. Opening...")
                img = Image.open(file_name)
                img.show()
            else:
                print("Error: Gemini didn't return an image URL in the response.")
                print("Raw response:", content)
        except (KeyError, IndexError) as e:
            print("Error: Unexpected response structure from Gemini API.")
            print("Raw response:", result)
    else:
        print(f"API Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")