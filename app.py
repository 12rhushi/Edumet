import streamlit as st
from PIL import Image
import tempfile
import os
import google.generativeai as genai
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
from gtts import gTTS


# Set page configuration
st.set_page_config(page_title="Chat Interface")

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


# Define layout columns
left_column, right_column = st.columns([2, 1])

# Define paths to local GIFs
default_gif_path = "C:/Users/rhushi/Desktop/EDUmet/Edumet/idel.gif"
speak_gif_path = "C:/Users/rhushi/Desktop/EDUmet/Edumet/speaking.gif"

# Initialize session state for TTS and GIF switching
if "tts_active" not in st.session_state:
    st.session_state.tts_active = False
if "current_gif" not in st.session_state:
    st.session_state.current_gif = default_gif_path  # Default to idle GIF

# Add sidebar
with st.sidebar:
    st.subheader('Model')
    
    # Display the current GIF based on the session state
    gif_placeholder = st.empty()
    gif_placeholder.image(st.session_state.current_gif, caption="Current", use_column_width=True)

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
input_prompt_text = """You are a professional teacher named Fern. Respond to questions in a concise manner, limiting your answers to 2-3 lines.
Provide detailed explanations only when explicitly requested. Avoid using any emojis in your responses."""

# Stop TTS playback if session is rerun
if "tts_active" in st.session_state and st.session_state.tts_active:
    sd.stop()  # Stop any ongoing playback
    st.session_state.tts_active = False
    st.session_state.current_gif = default_gif_path
    gif_placeholder.image(st.session_state.current_gif, caption="Idle", use_column_width=True)

# Stop TTS button logic
stop_tts = st.button("Stop")

if submit:
    # Check if an image is uploaded
    image_data = input_image_setup(uploaded_file)
    
    # Generate response based on whether image is uploaded or not
    response = get_gemini_response(input_prompt_text, input_prompt, image_data)
    
    # Convert text to speech
    audio_file_path = text_to_speech(response)
    
    # Switch to speaking GIF
    st.session_state.current_gif = speak_gif_path
    gif_placeholder.image(st.session_state.current_gif, caption="Speaking", use_column_width=True)

    # Right column response shown when TTS starts
    right_column.subheader("The Response is")
    right_column.write(response)

    # Play TTS audio and set session state
    with st.spinner("Playing TTS..."):
        data, fs = sf.read(audio_file_path, dtype='float32')
        sd.play(data, fs)
        st.session_state.tts_active = True

        # Poll for stopping TTS
        if stop_tts:
            sd.stop()
            st.session_state.tts_active = False
            st.warning("TTS Stopped")
        else:
            sd.wait()  # Wait for playback to finish

    # Revert to idle GIF after TTS playback finishes
    st.session_state.tts_active = False  # Ensure this is set before switching back
    st.session_state.current_gif = default_gif_path
    gif_placeholder.image(st.session_state.current_gif, caption="Idle", use_column_width=True)  # Force update

    # Remove temporary audio file
    os.unlink(audio_file_path)
