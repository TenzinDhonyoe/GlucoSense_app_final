# GlucoSense HbA1c Predictor

A machine learning-based web application to predict HbA1c levels using various health metrics.

## Features

- User-friendly interface for inputting health metrics
- Real-time HbA1c prediction
- Detailed recommendations based on results
- Mobile-responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GlucoSense_app_final.git
cd GlucoSense_app_final
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Model Training

Before running the app, you need to train the model:

1. Download the diabetes prediction dataset
2. Run the training script:
```bash
python train_model.py
```
This will create two files:
- `hbA1c_model.pkl`: The trained model
- `features.pkl`: The list of features used by the model

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Enter your health metrics and click "Predict HbA1c"

## Input Parameters

- Gender
- Age
- Smoking History
- BMI (Body Mass Index)
- Hypertension Status
- Heart Disease Status
- Blood Glucose Level

## Disclaimer

This tool provides estimates only and should not be used for medical diagnosis. Always consult with healthcare professionals for medical advice and proper diagnosis.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 