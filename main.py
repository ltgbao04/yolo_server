from flask import Flask, request, jsonify
import torch
import cv2
import function.helper as helper
import function.utils_rotate as utils_rotate

app = Flask(__name__)

yolo_path = "yolov5"
weight_path = "model\\LP_detector_nano_61.pt"
weight2_path = "model\\LP_ocr_nano_62.pt"

# Load YOLO models
yolo_LP_detect = torch.hub.load(yolo_path, 'custom', path=weight_path, force_reload=True, source='local')
yolo_license_plate = torch.hub.load(yolo_path, 'custom', path=weight2_path, force_reload=True, source='local')
yolo_license_plate.conf = 0.60

@app.route('/detect', methods=['POST'])
def detect():
    image = request.files['image']
    if image:
        path_to_save = 'output/temp_image.png'
        print("Save = ", path_to_save)
        image.save(path_to_save)

        img = cv2.imread(path_to_save)
        
        plates = yolo_LP_detect(img, size=640)

        plates = yolo_LP_detect(img, size=640)
        list_plates = plates.pandas().xyxy[0].values.tolist()
        list_read_plates = set()
        detected_plates = "" 
    
        if len(list_plates) == 0:
            lp = helper.read_plate(yolo_license_plate, img)
            if lp != "unknown":
                cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                list_read_plates.add(lp)
                detected_plates += lp 
        else:
            for plate in list_plates:
                flag = 0
                x = int(plate[0])  # xmin
                y = int(plate[1])  # ymin
                w = int(plate[2] - plate[0])  # xmax - xmin
                h = int(plate[3] - plate[1])  # ymax - ymin
                crop_img = img[y:y + h, x:x + w]
                cv2.rectangle(img, (int(plate[0]), int(plate[1])), (int(plate[2]), int(plate[3])), color=(0, 0, 225), thickness=2)
                lp = ""
                for cc in range(0, 2):
                    for ct in range(0, 2):
                        lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                        if lp != "unknown":
                            list_read_plates.add(lp)
                            cv2.putText(img, lp, (int(plate[0]), int(plate[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                            detected_plates += lp
                            flag = 1
                            break
                    if flag == 1:
                        break
        print(detected_plates)
    return detected_plates

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
