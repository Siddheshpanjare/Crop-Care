import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from utils.recommendation_dictionary import get_recommendation

CLASS_NAMES = [
    "Corn_Blight", "Corn_Common_Rust", "Corn_Gray_Leaf_Spot", "Corn_Healthy", "Corn___Northern_Leaf_Blight",
    "Pepperbell___Bacterial_spot", "Pepperbell___healthy", 
    "Potato___Early_Blight", "Potato___Healthy", "Potato___Late_Blight", 
    "Rice_Bacterial leaf blight", "Rice_Leaf_smut", "Rice___Brown_Spot", "Rice___Healthy", "Rice___Leaf_Blast", "Rice___Neck_Blast", 
    "Sugarcane_Bacterial_Blight", "Sugarcane_Healthy", "Sugarcane_Mosaic", "Sugarcane_RedRot", "Sugarcane_Rust", "Sugarcane_Yellow_Rust", 
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight", "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot", "Tomato_Spider_mites_Two_spotted_spider_mite", "Tomato__Target_Spot", "Tomato__Tomato_YellowLeaf__Curl_Virus", "Tomato__Tomato_mosaic_virus", "Tomato_healthy", 
    "Wheat___Brown_Rust", "Wheat___Healthy", "Wheat___Yellow_Rust"
]

def load_ai_model(model_path):
    """
    Load the trained ResNet50 model.
    """
    model = tf.keras.models.load_model(model_path)
    return model

def get_gradcam_heatmap_robust(img_array, model):
    """
    Generates the Grad-CAM heatmap by manually passing data through the layers
    to avoid Keras nested-model KeyErrors.
    """
    # 1. Find the ResNet50 base model
    base_model_layer = None
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model):
            base_model_layer = layer
            break
            
    if base_model_layer is None:
        # Fallback if the model isn't nested
        base_model_layer = model
        pre_layers = []
        post_layers = []
        
        # Try to find the last conv layer
        last_conv_layer = None
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer = layer
                break
        
        if last_conv_layer is None:
            raise ValueError("Could not find a Conv2D layer to generate Grad-CAM.")
            
        base_idx = model.layers.index(last_conv_layer)
        pre_layers = [l for l in model.layers[:base_idx+1] if not isinstance(l, tf.keras.layers.InputLayer)]
        post_layers = model.layers[base_idx+1:]
        
        with tf.GradientTape() as tape:
            x = tf.cast(img_array, tf.float32)
            for layer in pre_layers:
                x = layer(x)
            conv_outputs = x
            tape.watch(conv_outputs)
            
            out = conv_outputs
            for layer in post_layers:
                out = layer(out, training=False)
            predictions = out
            pred_index = tf.argmax(predictions[0])
            class_channel = predictions[:, pred_index]

        grads = tape.gradient(class_channel, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        return heatmap.numpy()

    # 2. Split model into layers before, during, and after ResNet50
    base_idx = model.layers.index(base_model_layer)
    pre_model = tf.keras.models.Model(inputs=model.inputs, outputs=model.layers[base_idx - 1].output)
    post_layers = model.layers[base_idx+1:]

    # 3. Manual Forward Pass inside GradientTape
    with tf.GradientTape() as tape:
        x = pre_model(img_array)
            
        tape.watch(x)
        conv_outputs = base_model_layer(x, training=False)
        tape.watch(conv_outputs)
        
        out = conv_outputs
        for layer in post_layers:
            out = layer(out, training=False)
            
        predictions = out
        pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    # 4. Calculate Gradients
    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # 5. Generate Heatmap
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def format_class_name(class_name):
    """
    Format class name for display (e.g., 'Tomato___Late_Blight' -> Crop: 'Tomato', Disease: 'Late Blight').
    """
    if "___" in class_name:
        parts = class_name.split("___")
        crop = parts[0].replace("_", " ")
        disease = parts[1].replace("_", " ")
    elif "__" in class_name:
        parts = class_name.split("__")
        crop = parts[0].replace("_", " ")
        disease = parts[1].replace("_", " ")
    elif "_" in class_name:
        parts = class_name.split("_", 1)
        crop = parts[0].replace("_", " ")
        disease = parts[1].replace("_", " ")
    else:
        crop = class_name
        disease = class_name
    
    if "healthy" in disease.lower():
        disease = "Healthy"
    
    return crop, disease

def run_real_inference(image_pil, model, language="en", heatmap_threshold=0.35):
    """
    Runs the real inference pipeline: preprocessing, prediction, Grad-CAM, and severity calculation.
    """
    # 1. Convert PIL image to cv2 format (RGB) exactly like cv2.imread would
    # To match Jupyter notebook cv2.imread exactly, we should ideally read bytes.
    # But since we have PIL, we will convert it to BGR then back to RGB, or just use the numpy array.
    # Actually, the difference in confidence (95.48% vs 97.33%) is likely due to PIL vs OpenCV JPEG decoding.
    img = np.array(image_pil)
    if img.shape[-1] == 4: # Handle RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    
    # Ensure it's exactly the BGR->RGB conversion if needed, but np.array from PIL is already RGB.
    # Let's just pass it to OpenCV.
    
    # Preprocess
    img_resized = cv2.resize(img, (224, 224))
    img_array = np.expand_dims(img_resized, axis=0).astype(np.float32) 
    
    # 2. Get Prediction
    preds = model.predict(img_array)
    pred_idx = np.argmax(preds[0])
    pred_class = CLASS_NAMES[pred_idx]
    confidence = np.max(preds[0]) * 100
    
    crop, disease = format_class_name(pred_class)
    status = "Healthy" if "healthy" in disease.lower() else "Diseased"
    
    # 3. Get Grad-CAM Heatmap
    heatmap = get_gradcam_heatmap_robust(img_array, model)
    
    # Resize heatmap back to the original image dimensions
    heatmap_resized = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap_8u = np.uint8(255 * heatmap_resized)
    
    # 4. Background Removal & True Severity Calculation
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    s_channel = hsv[:, :, 1]
    _, leaf_mask = cv2.threshold(s_channel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    threshold_value = int(255 * heatmap_threshold) 
    _, disease_mask_raw = cv2.threshold(heatmap_8u, threshold_value, 255, cv2.THRESH_BINARY)
    
    disease_mask = cv2.bitwise_and(disease_mask_raw, disease_mask_raw, mask=leaf_mask)
    
    leaf_pixels = cv2.countNonZero(leaf_mask)
    disease_pixels = cv2.countNonZero(disease_mask)
    
    if leaf_pixels == 0:
        severity_percentage = 0.0
    else:
        severity_percentage = (disease_pixels / leaf_pixels) * 100
        
    # Cap at 100% just in case
    severity_percentage = min(severity_percentage, 100.0)
    
    # Assign Severity Level
    if status == "Healthy":
        severity_level = "Mild" # For healthy, fetch Mild or default
        severity_percentage = 0.0
    else:
        if severity_percentage <= 10.0:
            severity_level = "Mild"
        elif severity_percentage <= 25.0:
            severity_level = "Moderate"
        else:
            severity_level = "Severe"
            
    # Get Recommendation
    recommendation = get_recommendation(pred_class, severity_level, language)
            
    # 5. Create superimposed visualization
    heatmap_color = cv2.applyColorMap(heatmap_8u, cv2.COLORMAP_JET)
    superimposed_img = cv2.addWeighted(img, 0.6, heatmap_color, 0.4, 0)
    
    # Convert heatmap and overlay to PIL for Streamlit display
    heatmap_pil = Image.fromarray(cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB))
    overlay_pil = Image.fromarray(superimposed_img)
    
    return {
        "pred_class": pred_class,
        "crop": crop,
        "disease": disease,
        "confidence": confidence,
        "severity": severity_percentage,
        "severity_level": severity_level,
        "status": status,
        "heatmap": heatmap_pil,
        "overlay": overlay_pil,
        "recommendation": recommendation
    }
