# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and features
model = joblib.load("hbA1c_model.pkl")
features = joblib.load("features.pkl")

# Page configuration
st.set_page_config(
    page_title="HbA1c Predictor - GlucoSense",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        margin-top: 1em;
    }
    .stMarkdown h1 {
        color: #1f77b4;
    }
    .stMarkdown h2 {
        color: #2c3e50;
    }
    .stMarkdown h3 {
        color: #34495e;
    }
    </style>
""", unsafe_allow_html=True)

# Header with logo and description
st.markdown("""
    <div style='text-align: center;'>
        <h1>🩸 GlucoSense HbA1c Predictor</h1>
        <p style='font-size: 1.2em; color: #666;'>
            Estimate your average blood glucose over the past 3 months using advanced machine learning
        </p>
    </div>
""", unsafe_allow_html=True)

# Information box
with st.expander("ℹ️ What is HbA1c?", expanded=True):
    st.markdown("""
        HbA1c (Hemoglobin A1c) is a blood test that shows your average blood sugar levels over the past 3 months.
        It's an important indicator of diabetes risk and blood sugar control.
        
        **Normal Range:** Below 5.7%  
        **Prediabetes:** 5.7% - 6.4%  
        **Diabetes:** 6.5% or higher
    """)

# Create columns for better layout
col1, col2 = st.columns(2)

# Initialize user_input with correct order
user_input = {feature: 0 for feature in features}

with col1:
    st.markdown("### 📋 Personal Information")
    user_input["gender"] = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        help="Select your gender"
    )
    
    user_input["age"] = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=30,
        help="Enter your age in years"
    )

    user_input["smoking_history"] = st.selectbox(
        "Smoking History",
        ["never", "former", "current", "not current", "ever", "No Info"],
        help="Select your smoking history"
    )

with col2:
    st.markdown("### 🏥 Health Metrics")
    user_input["bmi"] = st.number_input(
        "BMI (Body Mass Index)",
        min_value=10.0,
        max_value=60.0,
        value=25.0,
        step=0.1,
        help="Enter your BMI (weight in kg / height in meters squared)"
    )

    # Convert numerical flags to Yes/No
    hypertension_choice = st.selectbox(
        "Do you have Hypertension?",
        ["No", "Yes"],
        help="Select if you have been diagnosed with hypertension"
    )
    user_input["hypertension"] = 1 if hypertension_choice == "Yes" else 0

    heart_disease_choice = st.selectbox(
        "Do you have Heart Disease?",
        ["No", "Yes"],
        help="Select if you have been diagnosed with heart disease"
    )
    user_input["heart_disease"] = 1 if heart_disease_choice == "Yes" else 0

st.markdown("### 🔬 Blood Work")
user_input["blood_glucose_level"] = st.number_input(
    "Blood Glucose Level (mg/dL)",
    min_value=0.0,
    max_value=500.0,
    value=100.0,
    help="Enter your blood glucose level in mg/dL"
)

# Prepare input for prediction with correct feature order
input_df = pd.DataFrame([user_input])[features]

# Encode categorical data like in training
if "smoking_history" in input_df.columns:
    mapping_smoking = {"never": 0, "No Info": 1, "current": 2, "former": 3, "ever": 4, "not current": 5}
    input_df["smoking_history"] = input_df["smoking_history"].map(mapping_smoking)
if "gender" in input_df.columns:
    mapping_gender = {"Male": 1, "Female": 0, "Other": 2}
    input_df["gender"] = input_df["gender"].map(mapping_gender)

# Add a divider before prediction
st.divider()

# Center the predict button with custom styling
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    predict_button = st.button("🔍 Predict HbA1c", use_container_width=True)

if predict_button:
    hbA1c = model.predict(input_df)[0]
    
    # Create a container for results with custom styling
    result_container = st.container()
    with result_container:
        st.markdown("### 📊 Your Results")
        
        # Display HbA1c with appropriate styling
        st.markdown(f"""
            <div style='text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;'>
                <h2 style='color: #2c3e50;'>Predicted HbA1c</h2>
                <h1 style='color: #1f77b4; font-size: 3em;'>{hbA1c:.1f}%</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Interpretation with color-coded messages and better formatting
        if hbA1c < 5.7:
            st.success("""
                ### ✅ Your HbA1c is in the normal range (below 5.7%)
                **Recommendations:**
                - Continue maintaining your healthy lifestyle
                - Regular exercise and balanced diet are important
                - Schedule routine check-ups
            """)
        elif 5.7 <= hbA1c <= 6.4:
            st.warning("""
                ### ⚠️ Your HbA1c suggests prediabetes (5.7% - 6.4%)
                **Recommendations:**
                - Consider lifestyle modifications
                - Consult with a healthcare provider
                - Monitor your blood glucose regularly
                - Focus on diet and exercise
            """)
        else:
            st.error("""
                ### 🚨 Your HbA1c suggests diabetes (6.5% or higher)
                **Recommendations:**
                - Schedule an appointment with your doctor
                - This is not a diagnosis, but requires medical attention
                - Bring these results to your healthcare provider
                - Regular monitoring and medical supervision is important
            """)

# Add footer with disclaimer and additional information
st.divider()
st.markdown("""
    <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 5px;'>
        <p style='color: #666; font-size: 0.9em;'>
            <strong>Disclaimer:</strong> This tool provides estimates only and should not be used for medical diagnosis. 
            Always consult with healthcare professionals for medical advice and proper diagnosis.
        </p>
        <p style='color: #666; font-size: 0.9em;'>
            <strong>Note:</strong> The prediction is based on machine learning models and may not account for all individual factors.
            Regular medical check-ups are essential for proper health monitoring.
        </p>
    </div>
""", unsafe_allow_html=True)