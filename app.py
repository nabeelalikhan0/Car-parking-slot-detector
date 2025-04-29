import streamlit as st
import pickle
import cv2
import cvzone
import numpy as np

# Set up Streamlit page
st.title("Car Slot Detector")

# Choose video
video_option = st.selectbox("Choose video to run", ["Select", "First video", "Second video"])

# Load correct file
if video_option != "Select":
    if video_option == "First video":
        video_path = '1st/carPark.mp4'
        pos_file = '1st/CarParkPos'
        width, height = 107, 48
    else:
        video_path = '2nd/carPark.mp4'
        pos_file = '2nd/CarParkPos'
        width, height = 140, 75

    # Load parking positions
    with open(pos_file, 'rb') as f:
        posList = pickle.load(f)

    # Load video
    cap = cv2.VideoCapture(video_path)

    # Display frame in a Streamlit image placeholder
    frame_placeholder = st.empty()

    def checkParkingSpace(imgPro, img):
        spaceCounter = 0
        for pos in posList:
            x, y = pos
            imgCrop = imgPro[y:y + height, x:x + width]
            count = cv2.countNonZero(imgCrop)

            # Use higher and dynamic threshold for better accuracy
            # You can test values between 1200 to 1800 for best result
            threshold = 500 if video_option == "Second video" else 900

            if count > threshold:  # now checking for more white pixels = car present
                color = (0, 0, 255)  # Red for occupied
                thickness = 3
            else:
                color = (0, 255, 0)  # Green for free
                thickness = 2
                spaceCounter += 1

            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                            thickness=2, offset=0, colorR=color)

        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                        thickness=5, offset=20, colorR=(0, 200, 0))
        return img



    run = st.checkbox("Start Video")

    while run:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        if not success:
            st.write("Video load failed.")
            break

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        result_img = checkParkingSpace(imgDilate, img)

        # Convert image to RGB and update streamlit
        frame_placeholder.image(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB), channels="RGB")
        cv2.waitKey(10)
