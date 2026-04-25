# AI Speech to Image

A terminal-based Python tool that records your voice, converts the speech to text, and generates an image based on your prompt using Google's Gemini API and Pollinations.ai.

## Features

- **Voice Recording:** Records 8 seconds of audio from your microphone using `sounddevice`.
- **Speech Recognition:** Transcribes the recorded audio into text using Google's Speech-to-Text API.
- **Image Generation:** Leverages the **Google Gemini API** (`gemini-2.5-flash`) to intelligently create prompts, and dynamically generates images through [Pollinations.ai](https://pollinations.ai).
- **Auto-Display:** Automatically downloads and opens the generated image using your system's default image viewer.

## Prerequisites

Before running the application, make sure you have Python installed. You will also need to install the following Python packages:

```bash
pip install SpeechRecognition sounddevice soundfile requests Pillow python-dotenv
```

*Note: On Windows, `sounddevice` might also require you to have a working microphone setup. No extra C++ libraries are typically required if installed via pip.*

## Configuration

The script uses a Google Gemini API key to function. 
Currently, the API key is placed directly in `si.py` as `Gemini_api_key`.

If you wish to keep your API key secure, you can set it as an environment variable or place it inside a `.env` file in the same directory:
```env
GEMINI_API_KEY=your_actual_api_key_here
```
*(You will need to update the `Gemini_api_key` variable in `si.py` to `os.getenv("GEMINI_API_KEY")` if you choose to use the `.env` approach.)*

## Usage

1. Open a terminal in the project directory.
2. Run the script:
   ```bash
   python si.py
   ```
3. When prompted `Listening... Speak now!`, speak your prompt clearly into the microphone (you have 8 seconds).
   *Example: "Give me an image of a red sports car."*
4. Wait for the script to process your speech and generate the image.
5. The image will automatically be downloaded and displayed!

## How it Works

1. `sounddevice` captures raw audio data for exactly 8 seconds.
2. `soundfile` saves the raw audio as a temporary `temp_recording.wav` file.
3. `speech_recognition` processes the `.wav` file and converts it into a text string.
4. The text is sent to the **Gemini 2.5 Flash** model, asking it to return a formatted Markdown image URL pointing to Pollinations.ai.
5. `requests` downloads the image from Pollinations.ai as `image.jpg`.
6. `Pillow (PIL)` opens the image file on your screen.

## Troubleshooting

- **Audio not recognized:** Ensure your microphone is the default recording device in your OS settings and speak clearly without background noise.
- **API Error / Invalid Key:** Make sure your Gemini API key is valid. You can get a free key from [Google AI Studio](https://aistudio.google.com/).
