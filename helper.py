from ultralytics import YOLO
import time
import streamlit as st
import cv2
# from pytube import YouTube
import settings
import PIL
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page



def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def display_tracker_options():
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None


def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None, classes=0):
    """
    Display the detected objects on a video frame using the YOLOv8 model.

    Args:
    - conf (float): Confidence threshold for object detection.
    - model (YoloV8): A YOLOv8 object detection model.
    - st_frame (Streamlit object): A Streamlit object to display the detected video.
    - image (numpy array): A numpy array representing the video frame.
    - is_display_tracking (bool): A flag indicating whether to display object tracking (default=None).

    Returns:
    None
    """

    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))
    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:

        # Define a class mapping dictionary
        class_mapping = { 0 : 'Normal', 1 : 'Pneumonia' }

        # Perform object detection on the image
        res = model(image, conf=conf)

        # Replace class names with custom labels in the results
        for result in res:
            for cls_id, custom_label in class_mapping.items():
                if cls_id in result.names: # check if the class id is in the results
                    result.names[cls_id] = custom_label # replace the class name with the custom label

    # Perform object detection on the image
    res = model.predict(image, conf=conf)

    # # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )


def main():

    confidence = float(st.sidebar.slider(
        "Select Model Confidence", 25, 100, 40)) / 100

    model_path = Path(settings.DETECTION_MODEL)

    try:
        model = load_model(model_path)
    except Exception as ex:
            st.error(f"Unable to load model. Check the specified path: {model_path}")
            st.error(ex)

    st.sidebar.header("Image Config")

    source_img = None
    # If image is selected
    
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
                if source_img is None:
                   st.warning("Please upload your image!") 
                else:
                    uploaded_image = PIL.Image.open(source_img)
                    st.image(source_img, caption="Uploaded Image",
                            use_container_width=True)
        except Exception as ex:
                st.error("Error occurred while opening the image.")
                st.error(ex)

    with col2:
        if source_img is None:
                return
        else:
                if st.sidebar.button('Detect Objects'):
                    res = model.predict(uploaded_image,
                                        conf=confidence
                                        )
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image',
                            use_container_width=True)
                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        # st.write(ex)
                        st.write("No image is uploaded yet!")

    if st.sidebar.button("Back"):
            switch_page("Main")

if __name__ == "__main__":
    main()
