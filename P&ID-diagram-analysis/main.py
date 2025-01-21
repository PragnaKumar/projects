# Python In-built packages
from pathlib import Path
import PIL
import cv2
import numpy as np

# External packages
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Local Modules
import settings
import helper

def main():
    with st.sidebar:
        if st.sidebar.button("Start Detection"):
            switch_page("detect")

# Setting page layout
if __name__ == "__main__":
    st.set_page_config(
        page_title="P&ID Diagram Analysis",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Main page heading
    st.title("P&ID Diagram Analysis")

    col1, col2 = st.columns(2)

    with col1:
            image = r'original.jpg'
            default_image = PIL.Image.open(image)
            st.image(default_image, caption="Image without Detection",
                            use_column_width=True)
            
    with col2:
            image2 = r'result.jpg'
            default_detected_image = PIL.Image.open(image2)
            st.image(default_detected_image, caption='Detected image',
                            use_column_width=True)
        

main()


