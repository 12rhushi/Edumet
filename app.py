import streamlit as st
from PIL import Image
import tempfile
import os
import google.generativeai as genai
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
from gtts import gTTS

# Configure the generative AI model
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_gemini_response(input, prompt, image=None):
    if image is not None:
        response = model.generate_content([input, image[0], prompt])
    else:
        response = model.generate_content([input, prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        return None

def recognize_speech(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
    
    try:
        speech_text = r.recognize_google(audio_data)
        return speech_text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def text_to_speech(text):
    tts = gTTS(text=text, lang='en', slow=False)
    audio_fp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    tts.save(audio_fp.name)
    audio_fp.close()
    return audio_fp.name

# Set page configuration
st.set_page_config(page_title="Chat Interface")

# Define layout columns
left_column, right_column = st.columns([2, 1])

# Define paths to local GIFs
default_gif_path = "C:/Users/rhushi/Desktop/New folder/idel.gif"
speak_gif_path = "C:/Users/rhushi/Desktop/New folder/talking.gif"

# Add sidebar
with st.sidebar:
    st.subheader('Model')
    
    # Display idle GIF initially
    if os.path.exists(default_gif_path):
        gif_placeholder = st.empty()
        gif_placeholder.image(default_gif_path, caption="Idle GIF", use_column_width=True)
    else:
        st.warning("Default GIF not found")

# Left column: Input and upload
left_column.header("Input and Upload")

# Record audio
record_audio = left_column.button("Record Audio")
audio_file = None
if record_audio:
    with st.spinner("Recording..."):
        duration = 5  # Adjust the recording duration as needed
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_file.close()
        audio_data = sd.rec(int(duration * 44100), samplerate=44100, channels=2, dtype="int16")
        sd.wait()
        sf.write(audio_file.name, audio_data, samplerate=44100)
        st.success("Recording completed!")

# Recognize speech from recorded audio
speech_text = None
if audio_file is not None:
    speech_text = recognize_speech(audio_file.name)

# Input text prompt
input_prompt = left_column.text_area("Input Prompt: ", key="input", value=speech_text if speech_text else "")

# Button to upload image
uploaded_file = left_column.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    left_column.image(image, caption="Uploaded Image.", use_column_width=True)

submit = left_column.button("Send")

# Right column: Model response
right_column.header("")
input_prompt_text = """You are a professional teacher name Fern and your work is to explain concepts in the way of an informal conversation but explain it in a decisive way
and in a single paragraph just give the output in plain text format no need to give output in quotations"""

if submit:
    # Check if an image is uploaded
    image_data = input_image_setup(uploaded_file)
    
    # Generate response based on whether image is uploaded or not
    response = get_gemini_response(input_prompt_text, input_prompt, image_data)
    
    # Convert text to speech
    audio_file_path = text_to_speech(response)
    
    # Switch to speaking GIF, play TTS, and revert to idle GIF
    if os.path.exists(speak_gif_path):
        gif_placeholder.image(speak_gif_path, caption="Speaking GIF", use_column_width=True)

    # Right column response shown when TTS starts
    right_column.subheader("The Response is")
    right_column.write(response)

    # Play TTS audio
    with st.spinner("Playing TTS..."):
        data, fs = sf.read(audio_file_path, dtype='float32')
        sd.play(data, fs)
        sd.wait()

    # Revert to idle GIF after TTS playback finishes
    if os.path.exists(default_gif_path):
        gif_placeholder.image(default_gif_path, caption="Idle GIF", use_column_width=True)
    
    # Remove temporary audio file
    os.unlink(audio_file_path)
