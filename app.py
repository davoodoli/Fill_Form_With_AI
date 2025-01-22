import streamlit as st
#from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
from st_audiorec import st_audiorec
import openai
import os
import io
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

mytext = ""






def generate_chat_response(prompt): 
    response = openai.ChatCompletion.create( model="gpt-4", messages=[ {"role": "system",\
             "content": "You are supposed to extract just name and last name and address\
                  and phone and city and province and postal code from the input,\
                  if the user spoke in Farsi language, fill the form with English Equivalent and make the response in English\
                      so just focus on these things."}, {"role": "user", "content": prompt} ] )
    return response.choices[0].message['content'].strip()
    
    
# Streamlit UI
st.title("Audio Recorder")

wav_audio_data = st_audiorec()
if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')
    audio_file = io.BytesIO(wav_audio_data) # Transcribe the audio 
    audio_file.name = "audio.wav" # Set a name for the BytesIO object
    transcription = openai.Audio.transcribe( model="whisper-1", file=audio_file, response_format="text" )
    response = generate_chat_response(transcription+"what is their name?their last name?\
                                    their phone? address? city? province? postal-code?\
                                      give me the output in a format that each property separate from the next property by * symbol\
                                      I mean Name of the person then put *, then last name and * etc.\
                                    ")
    name, last_name, address, phone, city, province, code = response.split('*')
    st.session_state.name = name
    st.session_state.last = last_name
    st.session_state.phone = phone
    st.session_state.address = address
    st.session_state.province = province
    st.session_state.city = city
    st.session_state.code = code







if "name" not in st.session_state:
    st.session_state.name = ""
if "last" not in st.session_state:
    st.session_state.last = ""
if "phone" not in st.session_state:
    st.session_state.phone = ""
if "address" not in st.session_state:
    st.session_state.address = ""
if "code" not in st.session_state:
    st.session_state.code = ""
if "province" not in st.session_state:
    st.session_state.province = ""
if "city" not in st.session_state:
    st.session_state.city = ""

st.text_input("First Name",key="name")

st.text_input("Last Name",key="last")

st.text_input("Phone",key="phone")

st.text_input("Address",key="address")

st.text_input("Province",key="province")

st.text_input("City",key="city")

st.text_input("Postal Code",key="code")

