import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from PIL import Image
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import cv2

from utils.translations import get_translations, translate
from utils.styles import apply_custom_styles, render_glass_card, render_badge
from utils.real_ai import load_ai_model, run_real_inference
from utils.recommendation_dictionary import get_recommendation

# Page Config
st.set_page_config(
    page_title="CropCare",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'language' not in st.session_state:
    st.session_state.language = 'English'

@st.cache_resource
def load_cached_model():
    return load_ai_model(r"utils\ResNet50\final_resnet50_model.h5")

ai_model = load_cached_model()

translations_dict = get_translations()

def t(text):
    lang = st.session_state.get('language', 'English')
    return translate(text, lang, translations_dict)

def toggle_language():
    if st.session_state.get('language', 'English') == 'English':
        st.session_state.language = 'Hindi'
    else:
        st.session_state.language = 'English'

# Apply Styles
apply_custom_styles()

# SECTION 1: TOP NAVBAR
# Using columns to create a navbar layout
nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
with nav_col1:
    st.markdown(f'<div class="nav-logo">🌿 {t("CropCare")}</div>', unsafe_allow_html=True)
with nav_col3:
    st.button(f"🌐 {t('EN | हिंदी')}", on_click=toggle_language, use_container_width=True)

st.markdown("---")

# SECTION 3: SIDEBAR
with st.sidebar:
    st.title(f"🛠️ {t('Project Details')}")
    st.markdown(f"**{t('Selected model:')}** ResNet50")
    
    with st.expander(f"📖 {t('App instructions')}", expanded=True):
        st.write(t("1. Upload a clear image of a plant leaf.\n2. Click 'Run AI Diagnosis'.\n3. Review the AI prediction, severity, and Grad-CAM heatmap.\n4. Check the treatment recommendations."))
        
    with st.expander(f"🌱 {t('Supported crops')}", expanded=False):
        st.write(t("Apple, Cherry, Corn, Grape, Peach, Pepper, Potato, Strawberry, Tomato"))
        
    with st.expander(f"📊 {t('Dataset info')}", expanded=False):
        st.write(t("Trained on PlantVillage dataset containing 54,305 images across 38 class labels."))
        
    with st.expander(f"ℹ️ {t('About project')}", expanded=False):
        st.write(t("Developed for precise agricultural disease detection."))

# SECTION 2: HERO SECTION
st.markdown(f'<div class="hero-title">{t("CropCare")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-subtitle">{t("Explainable Multi-Crop Plant Disease Detection")}</div>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; color: #6b7280; margin-top: -10px; margin-bottom: 30px;">{t("Upload a leaf image to instantly diagnose diseases and get AI-powered treatment recommendations.")}</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# SECTION 4: IMAGE UPLOAD + PREVIEW
upload_col, preview_col = st.columns([1, 1], gap="medium")

with upload_col:
    # Upload Image Card with integrated uploader
    st.markdown(f"""
    <div class="upload-card">
        <h3>📥 {t('Upload Image')}</h3>
        <div class="upload-dropzone">
            <div class="upload-icon">⬆️</div>
            <p class="drop-title">{t('Drop your image here')}</p>
            <p>{t('or click to browse')}</p>
            <span class="upload-format-badge">🖼️ {t('JPG, PNG  Max 10MB')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # The native uploader is visually hidden via CSS and overlaid on the dropzone
    uploaded_file = st.file_uploader("upload", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="leaf_uploader")
    if not uploaded_file:
        st.session_state.show_results = False

with preview_col:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Convert image to base64 to embed inside the card HTML
        buf = BytesIO()
        image.save(buf, format="PNG")
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        st.markdown(f"""
        <div class="upload-card" style="min-height: 340px;">
            <h3 style="margin-bottom: 12px;">🖼️ {t('Image Preview')}</h3>
            <img src="data:image/png;base64,{img_b64}" style="width: 100%; border-radius: 10px; object-fit: contain; max-height: 260px;" />
        </div>
        """, unsafe_allow_html=True)
    else:
        # Analysis Results Placeholder (same height as upload card)
        st.markdown(f"""
        <div class="upload-card" style="text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <div class="analysis-leaf-icon">🌿</div>
            <h3>{t('Analysis Results')}</h3>
            <p style="color: #6b7280; font-size: 14px;">{t('Upload an image to see disease analysis results')}</p>
        </div>
        """, unsafe_allow_html=True)
        # with st.expander(t("Results will appear here")):
        #     st.write("")

# Tips for Best Results
st.markdown(f"""
<div class="tips-card">
    <h4>{t('Tips for Best Results')}</h4>
    <ul>
        <li>{t('Take a clear, close-up photo of the affected leaf')}</li>
        <li>{t('Ensure good lighting — natural daylight works best')}</li>
        <li>{t('Include visible symptoms (spots, discoloration, etc.)')}</li>
        <li>{t('Avoid blurry or out-of-focus images')}</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# SECTION 5: RUN MODEL SECTION
if uploaded_file is not None:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        run_inference = st.button(t("Run AI Diagnosis"), use_container_width=True)
        
    if run_inference:
        # Progress Simulation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Reset file pointer since Image.open read it previously
        uploaded_file.seek(0)
        # Use cv2.imdecode to match Jupyter Notebook's cv2.imread exactly
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_cv2 = cv2.imdecode(file_bytes, 1)
        img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img_cv2) # For Streamlit display
        
        status_text.text(t("Running ResNet50 Inference & Grad-CAM..."))
        progress_bar.progress(30)
        
        try:
            result = run_real_inference(image, ai_model, st.session_state.language)
            progress_bar.progress(80)
            
            status_text.text(t("Estimating Severity..."))
            progress_bar.progress(100)
            time.sleep(0.5)
            status_text.success(t("Diagnosis Complete!"))
            
            st.session_state.inference_result = result
            st.session_state.heatmap = result['heatmap']
            st.session_state.overlay = result['overlay']
            st.session_state.show_results = True
        except Exception as e:
            status_text.error(f"Error running inference: {e}")

# SECTION 6: OUTPUT DASHBOARD
if st.session_state.get('show_results', False):
    result = st.session_state.inference_result
    st.markdown(f"## {t('AI Prediction Dashboard')}")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.markdown(f"### {t('Prediction')}")
        st.markdown(f"<h4 style='color:#6b7280;'>{t('Crop Name')}</h4><h2 style='color:#059669;'>{t(result['crop'])}</h2>", unsafe_allow_html=True)
        st.markdown(f"<br><h4 style='color:#6b7280;'>{t('Disease Name')}</h4><h2 style='color:#059669;'>{t(result['disease'])}</h2>", unsafe_allow_html=True)
        #st.markdown(f"<br><h4 style='color:#6b7280;'>{t('Confidence')}</h4><h2 style='color:#1f2937;'>{result['confidence']:.2f}%</h2>", unsafe_allow_html=True)
        
        is_healthy = result["status"] == "Healthy"
        st.markdown(render_badge(t(result["status"]), is_healthy), unsafe_allow_html=True)
        
    with res_col2:
        st.markdown(f"### {t('Severity Analysis')}")
        sev_level = result['severity_level']
            
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = result['severity'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': t("Severity Level") + f" ({t(sev_level)})"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#059669" if is_healthy else "#dc2626"},
                'steps' : [
                    {'range': [0, 10], 'color': "rgba(16, 185, 129, 0.1)"},
                    {'range': [10, 25], 'color': "rgba(245, 158, 11, 0.1)"},
                    {'range': [25, 100], 'color': "rgba(239, 68, 68, 0.1)"}
                ]
            }
        ))
        fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#1f2937"})
        st.plotly_chart(fig, use_container_width=True)

    # Grad-CAM Heatmap
    st.markdown(f"### 🔍 {t('Grad-CAM Heatmap Analysis')}")
    cam_c1, cam_c2, cam_c3 = st.columns(3)
    with cam_c1:
        st.image(image, caption=t('Original Image'), use_container_width=True)
    with cam_c2:
        st.image(st.session_state.heatmap, caption=t('Heatmap'), use_container_width=True)
    with cam_c3:
        st.image(st.session_state.overlay, caption=t('Overlay'), use_container_width=True)
        
    # AI Explanation Panel
    st.info(f"""
    **{t('Why did the model predict this?')}**  
    {t('The model identified abnormal pigmentation and lesions in the highlighted regions (red/yellow areas in the heatmap). These visual patterns strongly correlate with the visual symptoms of ')} **{t(result['disease'])}**.  
    {t('Infected region is distributed primarily across the leaf veins and edges.')}
    """)

# SECTION 9: TREATMENT RECOMMENDATIONS
if st.session_state.get('show_results', False):
    st.markdown("---")
    st.markdown(f"## 🩺 {t('Treatment Recommendations')}")
    
    if result['status'] == "Diseased":
        with st.expander(f"📝 {t('Recommended Treatment')} - {t(result['severity_level'])}", expanded=True):
            st.write(f"**{t('Disease Name')}:** {t(result['disease'])}")
            current_lang = st.session_state.get('language', 'English')
            dynamic_rec = get_recommendation(result['pred_class'], result['severity_level'], current_lang)
            st.write(f"**{t('Action')}:** {dynamic_rec}")
    else:
        st.success(t("The plant appears healthy! Continue regular maintenance and monitoring."))

# SECTION 11: FOOTER
st.markdown("<br><hr>", unsafe_allow_html=True)
foot_c1, foot_c2, foot_c3 = st.columns([1, 2, 1])
with foot_c2:
    st.markdown(f"<p style='text-align: center; color: #94a3b8;'>{t('Developed for crop care and Agricultural AI Innovation.')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 12px;'>{t('Disclaimer: This AI tool is for informational purposes. Always consult an agricultural expert.')}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 12px;'>{t('© 2026 CropCare. All rights reserved.')}</p>", unsafe_allow_html=True)
