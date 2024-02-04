import streamlit as st


def home():
    st.balloons()
    st.image("/logo/TingleLogo.png", width=200)
    st.subheader("** Personalized Search Engine at Your Fingertip**")
    st.success(
        """ Empower your search with personalized results using LLAMA-powered engine. """
    )
    st.write(
        """
        This app allows you to upload an audio file and generate its meaning using a large language model (LLM).

        ### How it works:
        1. **Upload Audio:** Upload your audio file (MP3 or WAV format).
        2. **Generate Meaning:** After uploading, the app will convert the audio to text and then generate its meaning using an LLM.
        3. **View Result:** The generated meaning will be displayed to you.

        Enjoy exploring the app!
        """
    )
