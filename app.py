from PIL import Image
import google.generativeai as genai # type: ignore
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load gemini pro vision
model = genai.GenerativeModel("gemini-1.5-flash")

def input_image_details(upload_file):
    if upload_file is not None:
        # read the file into bytes
        bytes_data= upload_file.getvalue()
        
        image_parts = [
            {
                "mime_type":upload_file.type,
                "data":bytes_data
            }
            
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

def get_gemni_response(prompt, image,user_input):
    response = model.generate_content([prompt, image[0], user_input])
    return response.text


#initilize our streamlite app
st.set_page_config(page_title="Multilanguage Invoice Extractor ")
st.header("MultiLanguage Invoice Extractor")
user_input = st.text_input("Input Prompt", key="input")
upload_file = st.file_uploader("choose an image of the invoice..", type=["jpg","jpeg","png"])

# to show the uploaded image
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="upload Image.", use_column_width=True)
    
    
submit = st.button("Tell me about the Invice")

prompt = """
Your are an expert in understanding invoice. We will upload a image as invoice 
and you will have to answer any questions based on the upload invoice image
"""


# if submit buttion is clicked
if submit:
    image_data = input_image_details(upload_file)
    response = get_gemni_response(prompt, image_data, user_input)
    st.subheader("The response is")
    st.write(response)