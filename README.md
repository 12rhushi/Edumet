
# Chat Interface with Text-to-Speech and Generative AI

This Streamlit-based web application allows users to interact with a generative AI model (Google's Gemini) and receive conversational responses. Users can input prompts via text or voice, and the AI provides responses based on the input. The application features text-to-speech (TTS) functionality with animated GIFs that switch between idle and speaking states during the TTS playback.

## Features
- **Text and Audio Input**: Enter prompts via text or record voice input. The recorded audio is transcribed into text using Google's speech recognition.
- **Generative AI Responses**: The app uses Google's Gemini model to generate conversational responses based on the input.
- **Text-to-Speech (TTS)**: The generated response is converted to speech using `gTTS` and played back to the user.
- **Dynamic GIF Switching**: The application switches between an idle GIF and a speaking GIF when TTS is playing and switches back when TTS stops.

## Technologies Used
- **Streamlit**: For building the web interface.
- **Google Gemini AI**: For generating responses.
- **Google Text-to-Speech (gTTS)**: For converting text to speech.
- **SpeechRecognition**: For recognizing spoken prompts from recorded audio.
- **SoundDevice & SoundFile**: For recording and playing audio.
- **PIL (Python Imaging Library)**: For handling image uploads.

## Requirements

- Python 3.8+
- The following Python libraries:
  - `streamlit`
  - `PIL`
  - `google-generativeai`
  - `gTTS`
  - `speech_recognition`
  - `sounddevice`
  - `soundfile`

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Install dependencies:**

   You can install the required dependencies using `pip`:

   ```bash
   pip install streamlit pillow google-generativeai gtts SpeechRecognition sounddevice soundfile
   ```

3. **API Key Setup:**

   Obtain your API key from [Google's Gemini API](https://developers.generativeai.google.com/) and update the key in the script where `genai.configure` is called:

   ```python
   genai.configure(api_key="YOUR_API_KEY")
   ```

4. **Run the application:**

   To start the Streamlit app, run:

   ```bash
   streamlit run app.py
   ```

5. **Directory Setup for GIFs:**

   Ensure the GIFs you want to use for idle and speaking states are stored locally, and the paths are updated in the code:

   ```python
   default_gif_path = "path/to/your/idle.gif"
   speak_gif_path = "path/to/your/speaking.gif"
   ```

## Usage

1. **Input a Prompt**: You can type a text prompt into the text area or record your voice by clicking the "Record Audio" button.
2. **Submit**: After providing your input, click "Send". The app will process the input and generate a response using the generative AI model.
3. **GIFs and TTS**: The idle GIF is displayed initially. When TTS starts, the GIF will switch to a speaking state. Once TTS playback finishes, the app will revert to the idle GIF.
4. **Image Upload (Optional)**: You can also upload an image to get a response generated based on both the text and the image.

## Example

1. Run the app using `streamlit run app.py`.
2. Enter a prompt or record an audio message.
3. Watch as the app responds, plays the generated speech, and switches between GIFs.

## Future Improvements
- Add support for more complex interactions with multiple AI models.
- Implement real-time speech recognition.
- Expand the range of GIF animations to enhance user interaction.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
