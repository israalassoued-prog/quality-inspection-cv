import cv2
import os

files = os.listdir("my_folder");
correct = 0;
total = 0;
os.makedirs("output", exist_ok=True)
for filename in files:
    full_path = os.path.join("my_folder", filename);   
    img = cv2.imread(full_path);
    
    print("Processing:", filename);
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    blur = cv2.GaussianBlur(gray, (5, 5), 0);
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY);
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);
    hull = cv2.convexHull(contours[0], returnPoints=False);
    defects = cv2.convexityDefects(contours[0], hull);
    
    THRESHOLD_MAX = 1.99;
    worst_distance = 0;
    worst_point = None
    for i in range(len(defects)):
        start_idx, end_idx, far_idx, raw_distance = defects[i][0]
        actual_distance = raw_distance / 256.0
        if actual_distance > THRESHOLD_MAX:
            if actual_distance > worst_distance:
                worst_distance = actual_distance
                worst_point = contours[0][far_idx][0]
    
    if worst_distance > 0:
        prediction = "bad"
        top_left = (worst_point[0] - 10, worst_point[1] - 10)
        bottom_right = (worst_point[0] + 10, worst_point[1] + 10)
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
    else:
        prediction = "good"
    output_path = os.path.join("output", filename)
    cv2.imwrite(output_path, img)
    print(filename, "-> prediction:", prediction)
    print(filename, "-> worst_distance:", worst_distance, "-> prediction:", prediction)
    if "bad" in filename:
        truth = "bad"
    else:
        truth = "good"
    total = total + 1
    if truth == prediction:
        correct =correct+1
print(correct, "out of", total, "correct");


