from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np
import torch
from ultralytics.yolo.engine.results import Boxes
import os
img_data = {}

def evaluate_img( input_image):
    name = os.path.split(input_image)[1]
    model = YOLO("bestPCB_YoloV8.pt")
    results = model.predict(source=input_image, conf=0.75)[0]
    # print(results)
    cls = results.boxes.cls.cpu().numpy()    # cls, (N, 1)
    probs = results.boxes.conf.cpu().numpy()  # confidence score, (N, 1)
    boxes = results.boxes.xyxy.cpu().numpy()   # box with xyxy format, (N, 4)
    names = results.names
    detect_res = []
    for i in range(len(cls)):
        a = {}
        id = cls[i]
        a['class'] = int(id)
        a['name'] = names.get(id)
        bbox = boxes[i]
        a['xmin'] = int(bbox[0])
        a['ymin'] = int(bbox[1])
        a['xmax'] = int(bbox[2])
        a['ymax'] = int(bbox[3])
        detect_res.append(a)
    print(detect_res)
    print("HI-------")
    img_data[name] = detect_res
    return {name: detect_res}


def plot_img( img, result):
    name = os.path.split(img)[1]
    # Define colors for each class
    colors = {
        'open_circuit': (0, 255, 0),   # green
        'short': (255, 0, 0),  # blue
        'mouse_bite': (0, 0, 255), # red
        'spur': (255, 255, 0), # cyan
        'spurious_copper': (0, 255, 255), # yellow
        'missing_hole': (155, 105, 205)
    }

    # Load the image
    image = cv2.imread(img)

    # Loop through each result and draw the bounding box on the image
    for r in result[name]:
        class_name = r['name']
        color = colors[class_name]
        xmin, ymin, xmax, ymax = map(int, [r['xmin'], r['ymin'], r['xmax'], r['ymax']])
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness=2)
        text = f"{class_name}"
        cv2.putText(image, text, (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    new_name = f'output_images/{name}'
    cv2.imwrite(new_name, image)
    return new_name





img = r'C:\Users\beono\OneDrive\Desktop\PCB_defect detector2\input_images\WhatsApp Image 2023-03-11 at 15.22.36.jpg'
name = os.path.split(img)[1]
print(name)
ann = evaluate_img(img)
print(ann)
resu = plot_img(img, ann)









# print("Masks:", masks)
# print("Names:", names)
# print("Original image shape:", orig_img.shape)
# print("Original shape:", orig_shape)
# print("Path:", path)
# print("Probs:", probs)
# print("Speed:", speed)






# # Iterate over the results and draw bounding boxes
# for res in results:
#     for box in res["boxes"]:
#         x1, y1, x2, y2, conf, cls = box.int().tolist()
#         color = (0, 255, 0)  # Green color for the boxes
#         cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

# # Display the image
# cv2.imshow("Image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
