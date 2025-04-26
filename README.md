
# 🚗 Parking Slot Detector using OpenCV

This project detects free and occupied parking slots from video footage using simple image processing techniques in OpenCV.

It includes two main scripts:
- `ParkingSpacePicker.py` → Manually mark parking spaces on a parking lot image.
- `main.py` → Detects free/occupied parking slots in real-time from a video.

---

## 📂 Project Structure
```
.
├── 2nd/
│   ├── carParkImg.png     # Static image used for parking space selection
│   ├── carPark.mp4        # Video feed for parking lot
│   └── CarParkPos         # Saved parking positions (using pickle)
├── ParkingSpacePicker.py  # Tool to manually draw/select parking slots
├── main.py                # Main detection and counting program
├── README.md              # Project documentation
```

---

## 🛠 Requirements
- Python 3.8+
- OpenCV
- cvzone
- numpy

Install dependencies with:
```bash
pip install opencv-python cvzone numpy
```

---

## ✨ How It Works

### 1. Select Parking Spaces
Run:
```bash
python ParkingSpacePicker.py
```
- Left Click: Add a parking spot rectangle.
- Right Click: Remove a rectangle.
- Press **Space** to reset all spots.
- Press **Q** to quit and save.

Parking spots are saved automatically into a `CarParkPos` file.

---

### 2. Run the Parking Slot Detector
Run:
```bash
python main.py
```
- It processes video frame-by-frame.
- Checks each marked parking space if it is occupied or free.
- Displays **"Free" vs "Occupied"** slots with a live counter.

---

## ⚙️ Configuration

You can easily adjust:
- `original_width`, `original_height`: Size of parking slot rectangles.
- `scale`: Resize factor for both the image and video to fit your screen.

Scaling ensures that rectangles drawn match exactly in both image and video.

---


## 🧠 Concepts Used
- Image Thresholding
- Contour Detection
- Gaussian Blurring
- Adaptive Thresholding
- Parking Slot Area Cropping
- Dynamic Rescaling

---

## 🚀 Future Improvements
- Automatic parking space detection using Deep Learning (YOLOv8, etc.)
- Better handling for rainy/nighttime footage.
- Flask web app for live monitoring.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

---

**Made with ❤️ using OpenCV and Python!**
