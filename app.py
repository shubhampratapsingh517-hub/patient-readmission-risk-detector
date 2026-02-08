import streamlit as st
import pickle
import numpy as np

st.set_page_config(
    page_title="Patient Readmission Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    with open("readmission_model (1).pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌ Model file not found. Please check the path!")
    st.stop()

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = "Vibrant Rainbow"

# Theme configurations
themes = {
    "Vibrant Rainbow": {
        "primary": "#FF6B6B, #4ECDC4, #45B7D1, #FFA07A, #98D8C8",
        "secondary": "#667eea, #764ba2, #f093fb",
        "bg": "#ffecd2, #fcb69f, #ff9a9e, #fecfef",
        "input_bg": "#E0C3FC, #8EC5FC",
        "card_bg": "#FFFFFF"
    },
    "Ocean Breeze": {
        "primary": "#0093E9, #80D0C7, #13547A",
        "secondary": "#006BA6, #0496FF, #FFBC42",
        "bg": "#D4F1F4, #75E6DA, #189AB4",
        "input_bg": "#B8E6F0, #A0D6E8",
        "card_bg": "#FFFFFF"
    },
    "Sunset Glow": {
        "primary": "#FF6F61, #FFA500, #FFD700",
        "secondary": "#FF416C, #FF4B2B",
        "bg": "#FFF4E6, #FFDAB9, #FFB6C1",
        "input_bg": "#FFE5B4, #FFDAB9",
        "card_bg": "#FFFFFF"
    },
    "Forest Green": {
        "primary": "#2D6A4F, #52B788, #74C69D",
        "secondary": "#1B4332, #2D6A4F",
        "bg": "#D8F3DC, #B7E4C7, #95D5B2",
        "input_bg": "#C7E9C0, #A8DADC",
        "card_bg": "#FFFFFF"
    },
    "Purple Dream": {
        "primary": "#9D4EDD, #C77DFF, #E0AAFF",
        "secondary": "#7209B7, #560BAD",
        "bg": "#F3E5F5, #E1BEE7, #CE93D8",
        "input_bg": "#E1BEE7, #D1C4E9",
        "card_bg": "#FFFFFF"
    }
}

current_theme = themes[st.session_state.theme]

st.markdown(f"""
<style>
/* Global Styles */
* {{
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

/* Sidebar Styling */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {current_theme['secondary']}) !important;
    padding: 20px 10px !important;
}}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label {{
    color: white !important;
}}

[data-testid="stSidebar"] .stSelectbox label {{
    font-weight: 700 !important;
    font-size: 16px !important;
}}

/* Main Background */
.main {{
    background: linear-gradient(to bottom right, {current_theme['bg']});
    background-size: 400% 400%;
    animation: gradientShift 20s ease infinite;
    padding: 20px;
}}

@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Header Card */
.header-card {{
    background: linear-gradient(135deg, {current_theme['secondary']});
    color: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    margin-bottom: 30px;
}}

.header-card h1 {{
    font-size: 3em;
    font-weight: 900;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}}

.header-card p {{
    font-size: 1.2em;
    margin: 10px 0 0 0;
    opacity: 0.95;
}}

/* Feature Cards */
.feature-card {{
    background: {current_theme['card_bg']};
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 2px solid rgba(102, 126, 234, 0.1);
    transition: all 0.3s ease;
}}

.feature-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    border-color: rgba(102, 126, 234, 0.3);
}}

.feature-card h3 {{
    background: linear-gradient(135deg, {current_theme['secondary']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.3em;
    margin-bottom: 15px;
    font-weight: 700;
}}

/* Input Grid Layout */
.input-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}}

.input-item {{
    background: linear-gradient(135deg, {current_theme['input_bg']});
    padding: 15px;
    border-radius: 12px;
    border: 2px solid rgba(255,255,255,0.8);
    transition: all 0.3s ease;
}}

.input-item:hover {{
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.input-label {{
    font-weight: 700;
    font-size: 14px;
    color: #2c3e50;
    margin-bottom: 5px;
    display: block;
}}

.input-description {{
    font-size: 11px;
    color: #5a6c7d;
    font-style: italic;
    margin-top: 5px;
}}

/* Streamlit Inputs - Compact Design */
.stNumberInput > div > div > input,
.stSelectbox > div > div > select {{
    border-radius: 8px !important;
    border: 2px solid rgba(102, 126, 234, 0.3) !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    background: white !important;
}}

.stNumberInput > div > div > input:focus,
.stSelectbox > div > div > select:focus {{
    border-color: rgba(102, 126, 234, 0.8) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}}

/* Prediction Result Card */
.prediction-card {{
    border-radius: 20px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
    margin-top: 30px;
    border: 3px solid rgba(255,255,255,0.5);
    position: relative;
    overflow: hidden;
}}

.prediction-card::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
    transform: rotate(45deg);
    animation: shine 3s linear infinite;
}}

@keyframes shine {{
    0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
    100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
}}

.prediction-card h2 {{
    font-size: 2em;
    margin: 0 0 15px 0;
    position: relative;
    z-index: 1;
}}

.prediction-card .percentage {{
    font-size: 3.5em;
    font-weight: 900;
    margin: 20px 0;
    position: relative;
    z-index: 1;
}}

.prediction-card .risk-badge {{
    display: inline-block;
    padding: 10px 25px;
    border-radius: 25px;
    font-size: 1.1em;
    font-weight: 700;
    margin-top: 10px;
    position: relative;
    z-index: 1;
}}

.low-risk {{
    background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
    color: white;
}}

.low-risk .risk-badge {{
    background: rgba(255,255,255,0.3);
}}

.moderate-risk {{
    background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
    color: white;
}}

.moderate-risk .risk-badge {{
    background: rgba(255,255,255,0.3);
}}

.high-risk {{
    background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    color: white;
}}

.high-risk .risk-badge {{
    background: rgba(255,255,255,0.3);
}}

/* Action Button */
.stButton > button {{
    background: linear-gradient(135deg, {current_theme['primary']}) !important;
    background-size: 200% 200% !important;
    animation: gradientMove 3s ease infinite !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 18px !important;
    padding: 15px 50px !important;
    border-radius: 50px !important;
    border: none !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    margin-top: 20px !important;
}}

@keyframes gradientMove {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.stButton > button:hover {{
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6) !important;
}}

/* Progress Bar */
.stProgress > div > div > div {{
    background: linear-gradient(90deg, {current_theme['primary']}) !important;
    background-size: 200% 100% !important;
    animation: progressMove 2s linear infinite !important;
    border-radius: 10px !important;
}}

@keyframes progressMove {{
    0% {{ background-position: 0% 50%; }}
    100% {{ background-position: 200% 50%; }}
}}

/* Info Badge */
.info-badge {{
    display: inline-block;
    background: linear-gradient(135deg, {current_theme['secondary']});
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .input-grid {{
        grid-template-columns: 1fr;
    }}
    
    .header-card h1 {{
        font-size: 2em;
    }}
    
    .prediction-card .percentage {{
        font-size: 2.5em;
    }}
}}
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    theme = st.selectbox("🎨 Theme", 
                        ["Vibrant Rainbow", "Ocean Breeze", "Sunset Glow", "Forest Green", "Purple Dream"],
                        index=["Vibrant Rainbow", "Ocean Breeze", "Sunset Glow", "Forest Green", "Purple Dream"].index(st.session_state.theme))
    
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 About This Tool")
    st.markdown("""
    This AI-powered predictor helps healthcare professionals assess patient readmission risk using machine learning.
    
    **Features:**
    - Real-time predictions
    - Risk level categorization
    - Comprehensive analysis
    """)
    
    st.markdown("---")
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. Enter patient details in each category
    2. Review all inputs carefully
    3. Click 'Predict Readmission'
    4. Review the risk assessment
    """)

# Header
st.markdown("""
<div class='header-card'>
    <h1>🏥 Patient Readmission Predictor</h1>
    <p>Advanced AI-powered risk assessment for hospital readmission</p>
</div>
""", unsafe_allow_html=True)

# Data dictionaries
numeric_features = {
    "age": "Patient's age in years",
    "time_in_hospital": "Days spent in hospital during stay",
    "n_lab_procedures": "Number of laboratory tests performed",
    "n_procedures": "Number of medical procedures conducted",
    "n_medications": "Number of medications prescribed",
    "n_outpatient": "Number of outpatient visits in past year",
    "n_inpatient": "Number of inpatient visits in past year",
    "n_emergency": "Number of emergency visits in past year",
    "glucose_test": "Glucose serum test result indicator",
    "A1Ctest": "HbA1c test result indicator"
}

categorical_features = {
    "change": "Was medication changed during stay?",
    "diabetes_med": "Was diabetes medication prescribed?"
}

medical_specialty_options = ["Cardiology", "Endocrinology", "Family/General Practice", "InternalMedicine", "Other"]
diag_options = ["Circulatory", "Respiratory", "Digestive", "Diabetes", "Other"]

feature_values = []

# Create two-column layout for main content
col_left, col_right = st.columns([1, 1])

with col_left:
    # Numeric Features Card
    st.markdown("""
    <div class='feature-card'>
        <span class='info-badge'>Section 1 of 3</span>
        <h3>📊 Patient Metrics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create grid layout with columns
    for i in range(0, len(numeric_features), 2):
        cols = st.columns(2)
        features_list = list(numeric_features.items())
        
        for j, col in enumerate(cols):
            if i + j < len(features_list):
                feature, description = features_list[i + j]
                with col:
                    st.markdown(f"<div class='input-label'>{feature.replace('_', ' ').title()}</div>", unsafe_allow_html=True)
                    value = st.number_input(f"{feature}", value=0.0, step=0.1, key=feature, label_visibility="collapsed")
                    st.markdown(f"<div class='input-description'>{description}</div>", unsafe_allow_html=True)
                    feature_values.append(value)

with col_right:
    # Categorical Features Card
    st.markdown("""
    <div class='feature-card'>
        <span class='info-badge'>Section 2 of 3</span>
        <h3>🔄 Treatment Information</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for feature, description in categorical_features.items():
        st.markdown(f"<div class='input-label'>{feature.replace('_', ' ').title()}</div>", unsafe_allow_html=True)
        value = st.selectbox(f"{feature}_select", options=["No", "Yes"], key=feature, label_visibility="collapsed")
        st.markdown(f"<div class='input-description'>{description}</div>", unsafe_allow_html=True)
        feature_values.append(1 if value == "Yes" else 0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Medical Information Card
    st.markdown("""
    <div class='feature-card'>
        <span class='info-badge'>Section 3 of 3</span>
        <h3>🩺 Medical Details</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='input-label'>Medical Specialty</div>", unsafe_allow_html=True)
    medical_specialty = st.selectbox("specialty", options=medical_specialty_options, key="medical_specialty", label_visibility="collapsed")
    st.markdown("<div class='input-description'>Primary treating physician's specialty</div>", unsafe_allow_html=True)
    feature_values.append(medical_specialty_options.index(medical_specialty))
    
    st.markdown("<div class='input-label'>Primary Diagnosis</div>", unsafe_allow_html=True)
    diag_1 = st.selectbox("diag1", options=diag_options, key="diag_1", label_visibility="collapsed")
    st.markdown(f"<div class='input-description'>{diag_1} system disorder</div>", unsafe_allow_html=True)
    feature_values.append(diag_options.index(diag_1))
    
    st.markdown("<div class='input-label'>Secondary Diagnosis</div>", unsafe_allow_html=True)
    diag_2 = st.selectbox("diag2", options=diag_options, key="diag_2", label_visibility="collapsed")
    st.markdown(f"<div class='input-description'>{diag_2} system disorder</div>", unsafe_allow_html=True)
    feature_values.append(diag_options.index(diag_2))
    
    st.markdown("<div class='input-label'>Tertiary Diagnosis</div>", unsafe_allow_html=True)
    diag_3 = st.selectbox("diag3", options=diag_options, key="diag_3", label_visibility="collapsed")
    st.markdown(f"<div class='input-description'>{diag_3} system disorder</div>", unsafe_allow_html=True)
    feature_values.append(diag_options.index(diag_3))

# Prediction Button
if st.button("🔍 Predict Readmission Risk"):
    try:
        input_data = np.array([feature_values])
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] if hasattr(model, "predict_proba") else 1.0 if prediction == 1 else 0.0
        prob_percent = probability * 100

        if prob_percent < 25:
            risk_level = "Low Risk"
            css_class = "low-risk"
            emoji = "✅"
        elif prob_percent < 60:
            risk_level = "Moderate Risk"
            css_class = "moderate-risk"
            emoji = "⚠️"
        else:
            risk_level = "High Risk"
            css_class = "high-risk"
            emoji = "🚨"

        pred_text = "Likely to be Readmitted" if prediction == 1 else "Unlikely to be Readmitted"

        st.markdown(f"""
        <div class='prediction-card {css_class}'>
            <h2>{emoji} {pred_text}</h2>
            <div class='percentage'>{prob_percent:.1f}%</div>
            <div class='risk-badge'>{risk_level}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(float(probability))
        st.balloons()
        
        # Additional insights
        st.markdown("### 📈 Risk Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Probability", f"{prob_percent:.1f}%")
        with col2:
            st.metric("Risk Category", risk_level)
        with col3:
            st.metric("Prediction", "Readmit" if prediction == 1 else "No Readmit")
            
    except Exception as e:
        st.error(f"❌ Error making prediction: {e}")


















