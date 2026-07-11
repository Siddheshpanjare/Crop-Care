import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Base Theme - Light Green & White */
        :root {
            --bg-color: #ffffff;
            --card-bg: #ffffff;
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --accent: #059669; /* Greenorizin dark green */
            --accent-light: #d1fae5;
        }

        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(10px);
        }
        [data-testid="stDeployButton"] {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden;}

        /* Main App Background */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background-image: none;
        }

        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background-color: #f8fafc;
            border-right: 1px solid #e5e7eb;
        }
        [data-testid="stSidebar"] * {
            color: var(--text-main);
        }

        /* Glassmorphism Cards -> Flat Cards */
        .glass-card {
            background: var(--card-bg);
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        /* Top Navbar */
        .top-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 30px;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid #e5e7eb;
            position: sticky;
            top: 0;
            z-index: 999;
            margin-top: -60px;
            margin-bottom: 40px;
        }

        .nav-logo {
            font-size: 24px;
            font-weight: 800;
            color: var(--accent);
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Hero Section */
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            color: #111827;
            margin-bottom: 10px;
            animation: fadeInDown 0.8s ease-out;
        }

        .hero-subtitle {
            font-size: 1.25rem;
            color: var(--text-muted);
            text-align: center;
            margin-bottom: 40px;
            font-weight: 400;
            animation: fadeInUp 0.8s ease-out;
        }

        /* Beta Badge inside Hero */
        .beta-badge {
            display: inline-block;
            background-color: #d1fae5;
            color: #047857;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 16px;
            margin-bottom: 10px;
        }

        /* Animations */
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Custom Streamlit Buttons */
        div.stButton > button {
            background-color: var(--accent);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
            width: 100%;
        }
        
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(5, 150, 105, 0.3);
            background-color: #047857;
            color: white;
        }
        
        div.stButton > button:active, div.stButton > button:focus {
            background-color: #064e3b !important;
            color: white !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Badges */
        .status-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .badge-healthy {
            background-color: #ecfdf5;
            color: #059669;
            border: 1px solid #a7f3d0;
        }
        
        .badge-diseased {
            background-color: #fef2f2;
            color: #dc2626;
            border: 1px solid #fecaca;
        }

        /* Progress Bar */
        .stProgress > div > div > div > div {
            background-color: var(--accent);
        }

        /* Metrics */
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-main);
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-main) !important;
        }

        /* Upload Card */
        .upload-card {
            background: var(--card-bg);
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 28px;
            min-height: 340px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .upload-card h3 {
            margin-top: 0;
            color: var(--text-main);
            font-weight: 600;
            font-size: 18px;
        }
        .upload-dropzone {
            border: 2px dashed #e5e7eb;
            border-radius: 12px;
            background: #ffffff;
            padding: 40px 20px;
            text-align: center;
            transition: border-color 0.2s ease, background 0.2s ease;
        }
        .upload-dropzone:hover {
            border-color: #a7f3d0;
            background: #f8fafc;
        }
        .upload-icon {
            font-size: 32px;
            margin-bottom: 16px;
            color: #059669;
            background: #d1fae5;
            display: inline-block;
            padding: 12px 14px;
            border-radius: 12px;
        }
        .upload-dropzone p {
            margin: 4px 0;
            color: var(--text-muted);
            font-size: 14px;
        }
        .upload-dropzone p.drop-title {
            color: var(--text-main);
            font-weight: 600;
            font-size: 15px;
        }
        .upload-format-badge {
            display: inline-block;
            margin-top: 12px;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
            color: var(--text-muted);
            background: #f1f5f9;
        }

        /* Analysis Results Placeholder */
        .analysis-placeholder {
            background: var(--card-bg);
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 28px;
            text-align: center;
            min-height: 340px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .analysis-leaf-icon {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: #f8fafc;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px auto;
            font-size: 28px;
            color: #94a3b8;
            border: 1px solid #e5e7eb;
        }
        .analysis-placeholder h3 {
            color: var(--text-main);
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 18px;
        }
        .analysis-placeholder p {
            color: var(--text-muted);
            font-size: 14px;
        }

        /* Tips Card */
        .tips-card {
            background: var(--card-bg);
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 24px 28px;
            margin-top: 20px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .tips-card h4 {
            margin-top: 0;
            color: var(--text-main);
            font-weight: 600;
            font-size: 16px;
        }
        .tips-card ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .tips-card ul li {
            padding: 8px 0;
            color: var(--text-muted);
            font-size: 14px;
        }
        .tips-card ul li::before {
            content: "✓";
            color: var(--accent);
            font-weight: bold;
            margin-right: 10px;
        }

        /* Markdown text colors */
        .stMarkdown p {
            color: var(--text-main);
        }

        /* Hide native Streamlit uploader and overlay it on the dropzone */
        [data-testid="stFileUploader"] {
            position: relative;
            margin-top: -210px;
            height: 210px;
            opacity: 0;
            cursor: pointer;
            z-index: 10;
        }
        [data-testid="stFileUploader"] section {
            height: 100%;
        }
        [data-testid="stFileUploader"] section > input {
            height: 100%;
            cursor: pointer;
        }
        [data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
            opacity: 1 !important;
            color: var(--text-main) !important;
        }
        
        /* Expanders styling */
        .streamlit-expanderHeader {
            color: var(--text-main) !important;
            font-weight: 600;
        }
        .streamlit-expanderContent {
            border: 1px solid #e5e7eb;
            border-top: none;
            border-radius: 0 0 8px 8px;
        }

        /* Info box */
        div[data-testid="stAlert"] {
            background-color: #f0fdf4;
            color: #166534;
            border: 1px solid #bbf7d0;
        }

        </style>
    """, unsafe_allow_html=True)

def render_glass_card(content):
    return f'<div class="glass-card">{content}</div>'

def render_badge(text, is_healthy=True):
    badge_class = "badge-healthy" if is_healthy else "badge-diseased"
    return f'<div class="status-badge {badge_class}">{text}</div>'
