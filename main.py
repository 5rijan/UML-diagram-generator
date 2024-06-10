import streamlit as st 
import subprocess
import os
import tempfile
import shutil

@st.cache_data
def setup_java():
    os.system("wget -q https://download.oracle.com/otn/java/jdk/8u291-b10/d7fc238d0cbf4b0dac67be84580cfb4b/jdk-8u291-linux-x64.tar.gz")
    os.system("tar xvf jdk-8u291-linux-x64.tar.gz")
    os.environ["JAVA_HOME"] = os.getcwd() + "/jdk1.8.0_291"
    os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]
# Call the function to setup Java
setup_java()
# Define the output and reset files
Output = "output.puml"
OutputImage = "output.png"

st.sidebar.markdown("""
# **UML Diagram Generator**

This application converts Java source code into UML diagrams using PlantUML.

- **Upload `.java` files**: Use the file uploader to select your Java source files. After uploading, click 'Submit' to generate the UML diagram.

- **Customize your diagram**: Use the dropdown menu to change the theme of the UML diagram. Click 'Update' to apply the theme.

- **View the output**: The UML diagram will be displayed as a `.png` image which can also be downloaded using download button below.

- **Manual input**: You can also manually input PlantUML code into the text box and click 'Update' to generate a diagram.


                    """)
uploaded_files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True, type=[".java"])

source_dir = 'source'
if os.path.exists(source_dir):
    shutil.rmtree(source_dir)
os.makedirs(source_dir, exist_ok=True)

# Create an empty placeholder at the start
st.header("Output")
text_area_placeholder = st.empty()

# Fill the placeholder with a text_area widget
# Initially, the text area is filled with the contents of 'output.puml'
with open(Output, 'r') as f:
    initial_text = f.read()

text_area = text_area_placeholder.text_area("", initial_text, height=400)

for uploaded_file_raw in uploaded_files:
    file_name = os.path.join(source_dir, uploaded_file_raw.name)
    with open(file_name, 'wb') as f:
        f.write(uploaded_file_raw.getvalue())

if st.sidebar.button('Submit'):
    command = f'java -jar java2plantuml.jar "{source_dir}"'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

    with open(Output, 'r') as f:
        body = f.read()


options = ['none', 'amiga', 'aws-orange', 'black-knight', 'bluegray', 'blueprint', 'carbon-gray', 'cerulean', 'cerulean-outline', 'cloudscape-design', 'crt-amber', 'crt-green', 'cyborg', 'cyborg-outline', 'hacker', 'lightgray', 'mars', 'materia', 'materia-outline', 'metal', 'mimeograph', 'minty', 'mono', 'plain', 'reddress-darkblue', 'reddress-darkgreen', 'reddress-darkorange', 'reddress-darkred', 'reddress-lightblue', 'reddress-lightgreen', 'reddress-lightorange', 'reddress-lightred', 'sandstone', 'silver', 'sketchy', 'sketchy-outline', 'spacelab', 'spacelab-white', 'sunlust', 'superhero', 'superhero-outline', 'toy', 'united', 'vibrant']
selected_option = st.selectbox('Choose a theme', options)

import re

left_column, middle_column = st.columns(2)
if left_column.button('Update'):
    # Get the current value of the text area
    current_text = text_area

    # Prepare the theme line
    theme_line = f'!theme {selected_option}\n' if selected_option != 'none' else ''

    # Remove the existing theme line from the current text
    current_text = re.sub(r'!theme [^\n]*\n', '', current_text)

    # Remove the @startuml and @enduml tags from the current text
    current_text = re.sub(r'@startuml\n', '', current_text)
    current_text = re.sub(r'@enduml\n', '', current_text)

    # Remove the existing skinparam line from the current text
    current_text = re.sub(r'skinparam classAttributeIconSize 0\n', '', current_text)

    # Update 'output.puml' with the current text and the selected theme
    with open(Output, 'w') as f:
        f.write('@startuml\n' + theme_line + 'skinparam classAttributeIconSize 0\n' + current_text + '\n@enduml')

    command = f'java -jar plantuml-1.2024.5.jar {Output}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    st.image('output.png')

with open('output.png', 'rb') as f:
    st.sidebar.markdown("## Download Image")
    st.sidebar.markdown("Click the button below to download the image. The image will be downloaded to your browser's default download location. To change the download location, please change your browser settings.")
    btn = st.sidebar.download_button(
        label="Download Image",
        data=f,
        file_name='output.png',
        mime='image/png',
        key=None
    )