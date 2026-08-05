# 🌱 Crop Care: AI-Powered Plant Health Intelligence

[![Crop Care Demo](https://img.youtube.com/vi/SncdPAki4b0/maxresdefault.jpg)](https://youtu.be/SncdPAki4b0)
*(Click the image above to watch the project demo)*

Crop Care is a Deep Learning-Based Crop Disease Detection and Rule Based Recommendation System. It empowers farmers with AI-driven early detection, severity level assignment, and actionable disease remedies. 

Globally, annual crop yield loss due to diseases is ~20–40%. Traditional manual inspection is subjective and error-prone, while lab-based PCR testing is economically unviable for smallholder farmers and has a slow turnaround time. Crop Care provides a proactive solution to identify and treat diseases before irreversible crop damage occurs.

## ✨ Key Features

* **End-to-End Pipeline:** Provides a seamless pipeline from image upload to actionable recommendation in seconds.
* **Crop Classification:** Automatically identifies the crop type from an uploaded leaf image using a CNN classifier.
* **High Accuracy Detection:** Detects specific crop diseases with high accuracy using ResNet50 transfer learning.
* **Severity Analysis:** Quantifies infection spread using Grad-CAM heatmaps to categorize disease stages for precise intervention.
* **Actionable Remedies:** Provides disease-wise treatment recommendations via a dictionary recommendation engine based on class and severity.
* **Accessible Interface:** Features a bilingual web system (English and Hindi) designed for farmer use.
* **Offline Capabilities:** Designed as a lightweight model deployable on mobile devices for rural accessibility.

## 🔄 System Workflow

**Image Upload** ➔ **Crop Detection** ➔ **Disease Detection** ➔ **Severity Detection (GradCam)** ➔ **Rule Based Recommendation**

## 🛠️ Tech Stack

* **Programming Language:** Python
* **Machine Learning & Deep Learning:** Tensorflow, CNN, ResNet, Transfer Learning
* **Frontend Web Framework:** Streamlit

## 📊 Dataset & Preprocessing

The model utilizes the PlantVillage dataset alongside custom collected data for regional accuracy. 
* **Total Images:** 44,658 images after data augmentation.
* **Supported Crops:** Tomato, Wheat, Corn, Potato, Rice, Pepperbell, and Sugarcane.
* **Preprocessing Pipeline:** Images are resized to 224x224 pixels and normalized to a [0,1] scale.
* **Data Augmentation:** The dataset diversity is increased using random rotations, zoom, flips, brightness shifts, shear, and shifts.

## 🧠 Model Performance

Two primary architectures were evaluated for disease classification:

### 1. ResNet 50 (Best Performance Model)
ResNet 50 achieved the highest performance due to its deep residual learning capability and superior feature extraction for complex plant disease patterns.
* **Accuracy:** 93.60%
* **Precision:** 93%
* **Recall:** 93%
* **F1-Score:** 94%

<img width="1612" height="577" alt="Epochs" src="https://github.com/user-attachments/assets/6b008ae3-0ccb-411e-a819-4e5472b1c14f" />

### 2. MobileNet V2
* **Accuracy:** 88.36%
* **Precision:** 90%
* **Recall:** 92%
* **F1-Score:** 91%

## 🔍 Visual Diagnostics

### Grad-CAM Severity Detection
The system uses Grad-CAM heatmaps to visualize the severity of the infection, outputting a precise severity percentage (e.g., 49.27% for Early Blight). 

<img width="1625" height="645" alt="Heatmap" src="https://github.com/user-attachments/assets/730b4d6f-f6c4-4c7c-a379-e3e60ecebf75" />

### Confusion Matrix Analysis
Most diseases were correctly identified in the test set, with low misclassification. Most confusion occurs between visually similar diseases.

<img width="1638" height="818" alt="Confusion matrix" src="https://github.com/user-attachments/assets/5f297832-3f87-4560-8d55-070e9538e60f" />

## 🚀 Limitations & Future Scope

* **Multi-Label Classification:** Currently, the model predicts exactly one dominant disease per leaf image; future updates will replace the softmax layer with a sigmoid activation layer to support multiple simultaneous diseases.
* **Dynamic Recommendations:** The current rule-based dictionary will be integrated with a cloud-based API Expert System to deliver region-specific, dynamically updating treatment recommendations.
* **Automated Cropping:** Future pipelines will implement an upstream YOLO object detection layer to automatically isolate and crop the leaf from background clutter (like soil and weeds) before classification.
* **High-Resolution Support:** We aim to adopt patch-based cropping or advanced architectures to support larger inputs (e.g., 512x512) to detect early-stage microscopic spots that are currently lost during 224x224 compression.
