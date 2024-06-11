import streamlit as st 
import subprocess
import os
import tempfile
from io import BytesIO
import re

st.set_page_config(page_title="code2uml")
Output = "output.puml"

# Initialize session state for text_area_content if it doesn't exist
if 'text_area_content' not in st.session_state:
    st.session_state['text_area_content'] = ''


st.sidebar.markdown("""
# **UML Diagram Generator**

This application converts Java source code into UML diagrams using PlantUML.

- **Upload `.java` files**: Use the file uploader to select your Java source files. After uploading, click 'Submit' to generate the UML diagram.

- **Customize your diagram**: Use the dropdown menu to change the theme of the UML diagram. Click 'Update' to apply the theme.

- **View the output**: The UML diagram will be displayed as a `.png` image which can also be downloaded using download button below.

- **Manual input**: You can also manually input PlantUML code into the text box and click 'Update' to generate a diagram

Developed by Srijan Chaudhary ❤️


""")



uploaded_files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True, type=[".java"])

def update_action(selected_option):
    theme_line = '' if selected_option == 'none' else f'!theme {selected_option}'

    current_text = st.session_state['text_area_content']

    # If there's a theme in the current text, remove it
    current_text = re.sub(r'!theme \w+\n', '', current_text)
    current_text = current_text.replace('@startuml', '@startuml\n' + theme_line, 1)

    with open(Output, 'w') as f:
        f.write(current_text)

    command = f'java -jar plantuml-1.2024.5.jar {Output}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    # Read the output image into a BytesIO object
    with open('output.png', 'rb') as f:
        img_data = BytesIO(f.read())
    st.image(img_data)

    # Provide a download link for the image
    st.sidebar.markdown("## Download Image")
    st.sidebar.markdown("Click the button below to download the image. The image will be downloaded to your browser's default download location. To change the download location, please change your browser settings.")
    btn = st.sidebar.download_button(
        label="Download Image",
        data=img_data,
        file_name='output.png',
        mime='image/png',
        key=None
    )

    st.session_state['text_area_content'] = current_text
    text_area_placeholder.text_area("", st.session_state['text_area_content'], height=400)
with tempfile.TemporaryDirectory() as source_dir:

    # Create an empty placeholder at the start
    st.header("Output")
    text_area_placeholder = st.empty()

    # Define the update_text_area_content function
    def update_text_area_content():
        st.session_state['text_area_content'] = text_area

    # Fill the placeholder with a text_area widget
    text_area = text_area_placeholder.text_area("", st.session_state['text_area_content'], height=400, on_change=update_text_area_content)

    for uploaded_file_raw in uploaded_files:
        file_name = os.path.join(source_dir, uploaded_file_raw.name)
        with open(file_name, 'wb') as f:
            f.write(uploaded_file_raw.getvalue())

    if st.sidebar.button('Submit'):
        command = f'java -jar javaparser.jar "{source_dir}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output, error = process.communicate()
        process.wait()
        if process.returncode == 0:
            # Update the session state when the output is received
            st.session_state['text_area_content'] = output.decode('utf-8')
            text_area_placeholder.text_area("", st.session_state['text_area_content'], height=400)
        else:
            st.error("Error occurred while parsing Java files.")

    options = ['none', 'amiga', 'aws-orange', 'black-knight', 'bluegray', 'blueprint', 'carbon-gray', 'cerulean', 'cerulean-outline', 'cloudscape-design', 'crt-amber', 'crt-green', 'cyborg', 'cyborg-outline', 'hacker', 'lightgray', 'mars', 'materia', 'materia-outline', 'metal', 'mimeograph', 'minty', 'mono', 'plain', 'reddress-darkblue', 'reddress-darkgreen', 'reddress-darkorange', 'reddress-darkred', 'reddress-lightblue', 'reddress-lightgreen', 'reddress-lightorange', 'reddress-lightred', 'sandstone', 'silver', 'sketchy', 'sketchy-outline', 'spacelab', 'spacelab-white', 'sunlust', 'superhero', 'superhero-outline', 'toy', 'united', 'vibrant']
    selected_option = st.selectbox('Choose a theme', options)

    if st.button('Update'):
        # Update the session state with the current text from the text area
        st.session_state['text_area_content'] = text_area
        update_action(selected_option)
