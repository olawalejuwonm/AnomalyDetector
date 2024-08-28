import cv2
import numpy as np
import os
from sklearn.metrics import precision_score, recall_score, f1_score
from mainmodule import SurveillanceSystem  # Import the SurveillanceSystem class from mainmodule.py

# Path to the CDnet dataset
cdnet_dataset_path = "cdnet/office/input"
cdnet_groundtruth_path = "cdnet/office/groundtruth"

# Function to read frames from the CDnet dataset
def read_cdnet_frames(dataset_path):
    frames = []
    for root, _, files in os.walk(dataset_path):
        for file in sorted(files):
            if file.endswith(".jpg") or file.endswith(".png"):
                frame_path = os.path.join(root, file)
                frame = cv2.imread(frame_path)
                frames.append(frame)
    return frames

# Function to read ground truth frames from the CDnet dataset
def read_cdnet_groundtruth(dataset_path):
    groundtruths = []
    for root, _, files in os.walk(dataset_path):
        for file in sorted(files):
            if file.endswith(".jpg") or file.endswith(".png"):
                groundtruth_path = os.path.join(root, file)
                groundtruth = cv2.imread(groundtruth_path, cv2.IMREAD_GRAYSCALE)
                groundtruths.append(groundtruth)
    return groundtruths

# Function to evaluate performance
def evaluate_performance(detected_objects, ground_truth):
    y_true = []
    y_pred = []
    # Assuming ground_truth is a binary mask where 255 indicates the object
    y_true = (ground_truth == 255).astype(int).flatten()
    for class_id in detected_objects.class_id:
        y_pred.append(1 if class_id == 72 else 0)  # Assuming class_id 72 is the object of interest
    y_pred = np.array(y_pred * len(y_true))  # Repeat y_pred to match the length of y_true
    precision = precision_score(y_true, y_pred, average="macro", zero_division=0)
    recall = recall_score(y_true, y_pred, average="macro", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    return precision, recall, f1

# Read frames and ground truth from the CDnet dataset
frames = read_cdnet_frames(cdnet_dataset_path)
groundtruths = read_cdnet_groundtruth(cdnet_groundtruth_path)

print(f"Number of Frames: {len(frames)}")
print(f"Number of Ground Truths: {len(groundtruths)}")

# Instantiate the SurveillanceSystem
system = SurveillanceSystem()

# Process each frame and evaluate performance
all_precisions = []
all_recalls = []
all_f1s = []

for frame, groundtruth in zip(frames, groundtruths):
    detected_objects, processed_frame = system.callback(frame)
    print(f"Detected Objects: {detected_objects}")
    print(f"Ground Truth: {groundtruth}")
    print(processed_frame.shape)
    precision, recall, f1 = evaluate_performance(detected_objects, groundtruth)
    all_precisions.append(precision)
    print(f"Precision: {precision}")
    all_recalls.append(recall)
    print(f"Recall: {recall}")
    all_f1s.append(f1)
    print(f"F1-Score: {f1}")

# Calculate average performance metrics
if all_precisions and all_recalls and all_f1s:
    average_precision = np.mean(all_precisions)
    average_recall = np.mean(all_recalls)
    average_f1 = np.mean(all_f1s)
else:
    average_precision = average_recall = average_f1 = 0.0
    print("Warning: No valid performance metrics were calculated.")

print(f"Average Precision: {average_precision}")
print(f"Average Recall: {average_recall}")
print(f"Average F1-Score: {average_f1}")