#Import Necessary Libraries

import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv() #To load all Environemntal Variable
from pathlib import Path

#from api_key import api_key

#config GENAI with API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
generation_config = {
  "temperature": 0.8,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

# Apply Safety Settings
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_prompt="""

As a highly skilled medical practionioner specializing in medical image analysis, your are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases or health issues that may be present in the images.

Your Responsibilities:

1. Detailed Analysis: Thoroughly Analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in the structured form.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps , including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of the images: Incase where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'

3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions"

4. Your insights are invaluable in guiding clinical decisions. Please proceed with the Analysis, adhering to the structured approach as mentioned above.

Request to provide me an ouput response with these 4 headings Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions.
"""

#model configuration
model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Designing the front end
st.set_page_config(page_title="Medical Image Analytics", page_icon=":robot:")

#set the logo
#st.image=("ABCDEF.jpg", width=200)

#set the title
st.title("Medical Image Analytics")

#Set the sub-title
st.subheader("An Application that can help users to identify medical images")

#Uploading image
uploaded_file = st.file_uploader("Upload the Medical Image to Perform Analysis", type=["png","jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, width=300, caption="Uploaded Medical Image")
submit_button = st.button("Generate the Analysis")

if submit_button:
    #Process the uploaded image
    image_data=uploaded_file.getvalue()
    
    # making our image ready
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]
    # making our prompt ready
    prompt_parts = [

        image_parts[0],
        system_prompt,
    ]
    # Generate a response based on prompt and image
    #st.image(image_data, width=300)
    st.title("Here is the analysis based on your input image...")
    response = model.generate_content(prompt_parts)

    st.write(response.text)

