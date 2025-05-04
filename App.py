import streamlit as st
import tempfile
import os
from gtts import gTTS
import base64
import time
import io

def text_to_speech(text, language='en', slow=False):
    """Convert text to speech using gTTS (Google Text-to-Speech)"""
    try:
        # Create a temporary file
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        audio_file.close()
        
        # Generate speech
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(audio_file.name)
        
        return audio_file.name
    except Exception as e:
        st.error(f"Error during text-to-speech conversion: {str(e)}")
        return None

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for a file"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="{file_label}.mp3">Download {file_label}</a>'

def get_available_languages():
    """Get available languages with their friendly names"""
    languages = {
        'en': 'English', 
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh-CN': 'Chinese (Simplified)',
        'ar': 'Arabic',
        'hi': 'Hindi'
    }
    return languages

def main():
    st.set_page_config(
        page_title="Text to Audio Converter",
        page_icon="🔊",
        layout="wide"
    )
    
    st.title("Text to Audio Converter")
    st.markdown("Convert your text to speech using gTTS!")
    
    # Text input
    text_input = st.text_area("Enter the text you want to convert to audio:", 
                         height=150, 
                         placeholder="Type your text here...",
                         help="Enter the text you want to convert to speech")
    
    # Language selection
    languages = get_available_languages()
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox(
            "Select a language:",
            options=list(languages.keys()),
            format_func=lambda x: f"{languages[x]} ({x})",
            help="Choose the language for text-to-speech conversion"
        )
        
        # Speaking speed
        slow_speech = st.checkbox("Slower speech", value=False, 
                           help="Check this to slow down the speaking rate")
    
    with col2:
        # File name
        output_filename = st.text_input("Output File Name:", value="my_audio", 
                                   help="Enter the file name for the output audio")
    
    # Button to convert text to speech
    if st.button("Convert to Audio", type="primary"):
        if not text_input.strip():
            st.error("Please enter some text to convert!")
        else:
            with st.spinner("Converting text to audio..."):
                # Show progress
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Generate audio
                try:
                    audio_file = text_to_speech(text_input, language, slow_speech)
                    
                    if audio_file:
                        # Display success message
                        st.success("Audio generated successfully!")
                        
                        # Audio playback
                        st.subheader("Listen to the generated audio:")
                        st.audio(audio_file, format="audio/mp3")
                        
                        # Download link
                        st.markdown("### Download Audio File")
                        st.markdown(get_binary_file_downloader_html(audio_file, output_filename), unsafe_allow_html=True)
                    else:
                        st.error("Failed to generate audio. Please try again.")
                    
                except Exception as e:
                    st.error(f"An error occurred during conversion: {e}")
    
    # Usage instructions
    with st.expander("How to use this app"):
        st.markdown("""
        1. Enter the text you want to convert to audio in the text area
        2. Choose a language from the dropdown menu
        3. Optionally select slower speech if needed
        4. Enter a name for your output file
        5. Click the 'Convert to Audio' button
        6. Listen to the preview and download your audio file
        """)
    
    # App information footer
    st.markdown("---")
    st.markdown("### About this app")
    st.markdown("""
    This application uses the gTTS (Google Text-to-Speech) library to convert text to speech.
    The app generates MP3 audio files that you can preview and download.
    
    **Note:** This app requires an internet connection since gTTS connects to Google's servers to generate speech.
    """)

if __name__ == "__main__":
    main()