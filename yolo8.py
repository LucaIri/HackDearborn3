import random
import cv2 
import numpy as np
from ultralytics import YOLO
import pyttsx3
import os
import langChange



confidences_level = 0.6 # Confidence Detection Level
box_overlap_level = 0.2 # Box overlap value
object_name = "" # Name of object detected

# Function for Non-Max Suppression (Box overlapping)
def non_max_suppression(boxes, confidences, iou_threshold):
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.0, nms_threshold=iou_threshold)
    # return [i[0] for i in indices]
    
    # Debug print to check the content of indices
    # print(f"NMS indices: {indices}")

    # Handle case where indices might be a different type than expected
    # if len(indices) > 0 and isinstance(indices[0], list): # indices is not empty and contains list
    #     return [i[0] for i in indices] 
    # elif len(indices) > 0:
    #     return indices.flatten().tolist()
    # else:
    #     return []
    return indices.flatten().tolist()

# Masking the frame and only providing a rectangle mask
def frame_masking(frame, frame_wid, frame_hyt):
    rect_wid = 240
    rect_hyt = 150
    top_left_x = int((frame_wid/2) - (rect_wid/2))
    top_left_y = int((frame_hyt/2) - (rect_hyt/2)) - 80
    top_right_x = int((frame_wid/2) + (rect_wid/2)) 
    top_right_y = int((frame_hyt/2) + (rect_hyt/2)) + 80
    
    mask = np.zeros(frame.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (top_left_x,top_left_y), (top_right_x, top_right_y), 255, -1) #top left corner and bottom right corner
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    return masked
    

# opening the file in read mode
my_file = open("utils/coco.txt", "r")
# reading the file
data = my_file.read()
# replacing end splitting the text | when newline ('\n') is seen.
class_list = data.split("\n")
my_file.close()

# print(class_list)

# Generate random colors for class list
detection_colors = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_colors.append((b, g, r))

# load a pretrained YOLOv8n model
model = YOLO(model="weights/yolov8n.pt", task="v8", verbose=False) #verbose outputs shape of the frame (batch_size, color, height, width)

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 200) # Speed percent (can go over 100)
engine.setProperty('volume', 1.0)


# Vals to resize video frames | small frame optimise the run
frame_wid = 640
frame_hyt = 480


# Prompts user to select language of choice
while True:
    lang_abb = langChange.voice_input()
    if (lang_abb != "Not recognized"):
        break



cap = cv2.VideoCapture(0) # live camera
# cap = cv2.VideoCapture("inference/videos/v2.MP4") # Pre loaded video

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = frame_masking(frame, frame_wid, frame_hyt)

    #  resize the frame | small frame optimise the run
    frame = cv2.resize(frame, (frame_wid, frame_hyt))

    # Predict on image
    detect_params = model.predict(source=[frame], conf=confidences_level, save=False) 

    # Convert tensor array to numpy
    DP = detect_params[0].numpy()
    # print(DP)

    if len(DP) != 0:
        boxes, confidences, classIDs = [], [], [] # List of boxes, confidence score and classification Ids
        
        # Extracting boxes, confidences, and classIds
        for i in range(len(detect_params[0].boxes)):
            # print(i)

            box = detect_params[0].boxes[i]  # returns one box
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]
            
            # Used for NMS
            boxes.append([int(bb[0]), int(bb[1]), int(bb[2]-bb[0]), int(bb[3]-bb[1])])  # Convert to (x, y, w, h) format
            confidences.append(float(conf))
            classIDs.append(int(clsID))
        
        # Apply Non-Maximum Suppression (NMS)   
        nms_indices = non_max_suppression(boxes, confidences, iou_threshold = box_overlap_level) 
        print(f"NMS Indices: {nms_indices}")
        clsID_val = ''
        
        if len(nms_indices) > 0:
            for i in nms_indices:
                x, y, w, h = boxes[i] # boundaires per item
                clsID_val = classIDs[i]
                conf_val = confidences[i]            
                
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h), # from x add w for width, etc.
                    detection_colors[clsID_val], # random color based on clasID_val
                    3,
                )

                # Display class name and confidence
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(
                    img = frame,
                    text = class_list[clsID_val] + " " + str(round(100 * round(conf_val, 3), 1)) + "%", # Name of object and confidence %
                    org = (x, y - 10),
                    fontFace= font,
                    fontScale = 0.5, #font size
                    color = (255, 255, 255),
                    thickness= 1,
                )
                
            print(f"Object Detected: {class_list[clsID_val]}")
            # Speak the detected object in real time
            object_name = class_list[clsID_val] #name of object pulled from list using id
            my_text = f"There is a {object_name}"
            #engine.say(my_text)
            #engine.runAndWait()
            langChange.speak_text(lang_abb, my_text)
                
    else:
        print("No Object Detected!")
            
    # print(clsID_val)
    
    #for i in range(len(classIDs)):
               # print(f"objectname: {classIDs[i]}")
    
    # Display the resulting frame
    cv2.imshow("ObjectDetection", frame)

    # Terminate run when "Q" pressed
    if cv2.waitKey(1) == ord("q"):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()