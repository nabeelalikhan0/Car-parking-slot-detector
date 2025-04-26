import cv2
import pickle
import os

# Original rectangle size
original_width, original_height = 140,70

# Resize scale (adjust based on your screen size)
scale = 0.6  # 60% of original size
width, height = int(original_width * scale), int(original_height * scale)

# Path to save parking positions
pos_path = '2nd/CarParkPos'

# Load saved positions
if os.path.exists(pos_path):
    with open(pos_path, 'rb') as f:
        posList = pickle.load(f)
else:
    posList = []

def mouseClick(events, x, y, flags, params):
    global posList
    # Convert scaled coordinates back to original
    x_orig, y_orig = int(x / scale), int(y / scale)

    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x_orig, y_orig))
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x_orig < x1 + original_width and y1 < y_orig < y1 + original_height:
                posList.pop(i)
                break

    with open(pos_path, 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('2nd/carParkImg.png')
    if img is None:
        print("Image not found. Check the path.")
        break

    # Resize image
    img_resized = cv2.resize(img, (0, 0), fx=scale, fy=scale)

    # Draw scaled rectangles
    for pos in posList:
        x, y = int(pos[0] * scale), int(pos[1] * scale)
        cv2.rectangle(img_resized, (x, y), (x + width, y + height), (255, 0, 255), 2)

    cv2.imshow("Image", img_resized)
    cv2.setMouseCallback("Image", mouseClick)

    key = cv2.waitKey(1)

    if key == 32:  # Spacebar clears all rectangles
        posList = []
        with open(pos_path, 'wb') as f:
            pickle.dump(posList, f)
        print("All rectangles cleared.")

    elif key == ord('q'):  # Q to quit
        break

cv2.destroyAllWindows()
