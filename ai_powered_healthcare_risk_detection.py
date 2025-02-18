# -*- coding: utf-8 -*-
"""AI_Powered_Healthcare_Risk_Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/chhavi007-bit/Healthcare-Follw-Up/blob/main/AI_Powered_Healthcare_Risk_Detection.ipynb
"""

import numpy as np
import pandas as pd
import io
import seaborn as sns
import gspread

"""Loading and Reading Data"""

from google.colab import auth
# Authenticate and authorize Google Sheets access
auth.authenticate_user()
from google.auth import default
creds, _ = default()


gc = gspread.authorize(creds)

# Replace 'Your spreadsheet name' with the actual name of your spreadsheet
# Replace 'Sheet1' with the name of the sheet you want to access
# Replace 'NewDataSet' with the correct name of your spreadsheet
worksheet = gc.open('gpt-4').worksheet('gpt-4')
 # Load data into a pandas DataFrame
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])
df.shape

print(df)

"""Sampling"""

sample_df = df.sample(n=1000, random_state=42)
print(sample_df)

"""clean data
- These characters can introduce noise and ambiguity to your data, and may not be relevant for your NLP task.
"""

import re
def clean_text(text):

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

sample_df['text_column'] = sample_df['data'] + ' ' + sample_df['conversation'
]
sample_df['text_column'] = sample_df['text_column'].apply(clean_text)
print(sample_df['text_column'])
sample_df['text_column'].describe()

"""Text Preprocessing"""

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())
    # Remove stopwords
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    # Lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)


sample_df['processed_text'] = sample_df['text_column'].apply(preprocess_text)

print(sample_df['processed_text'])

"""Exploratory Data Analysis"""

from collections import Counter
word_counts = Counter(" ".join(sample_df['processed_text']).split())
print(word_counts.most_common(100))

import re
def extract_age(text):
  match = re.search(r'(\d{1,3})\s*(?:years?|yrs?|y/o|yo|age|aged)', text, re.IGNORECASE)
  return int(match.group(1)) if match else None

sample_df['age'] = sample_df['processed_text'].apply(extract_age)
print(sample_df[['age', 'processed_text']].head(10))

def extract_gender(text):
    text = text.lower()
    if re.search(r'\b(male|man|boy|gentleman|he|him)\b', text):
        return 'Male'
    elif re.search(r'\b(female|woman|girl|lady|she|her)\b', text):
        return 'Female'
    return 'Unknown'

sample_df['gender'] = sample_df['processed_text'].apply(extract_gender)
print(sample_df[['gender', 'processed_text']].head(10))

import re
import pandas as pd


# Define a regex pattern for common medical terms (expand this list)
medical_terms = [
    # Common diseases
    "diabetes", "hypertension", "stroke", "cancer", "asthma", "tuberculosis",
    "heart attack", "lung infection", "pneumonia", "arthritis", "osteoporosis",
    "kidney disease", "liver failure", "migraine", "epilepsy", "Alzheimer", "Parkinson",

    # Symptoms
    "fever", "cough", "sore throat", "chest pain", "shortness of breath",
    "dizziness", "fatigue", "nausea", "vomiting", "headache", "muscle pain",
    "skin rash", "irregular heartbeat", "vision loss", "weight loss", "obesity",

    # Treatments
    "aspirin", "insulin", "inhaler", "antibiotics", "chemotherapy", "radiation therapy",
    "physical therapy", "painkillers", "antidepressants", "antihistamines", "surgery",
    "dialysis", "vaccine", "blood transfusion",

    # Medical tests
    "MRI scan", "CT scan", "X-ray", "ECG", "blood test", "urine test", "biopsy",
    "endoscopy", "ultrasound", "PET scan", "colonoscopy",

    "asthma", "bronchitis", "COPD", "emphysema", "pneumonia",

    "lung infection", "pulmonary fibrosis", "cystic fibrosis", "tuberculosis", "lung cancer",
    "pulmonary embolism", "ARDS", "interstitial lung disease", "sarcoidosis",
    "pleurisy", "pulmonary hypertension", "pneumothorax", "dyspnea", "wheezing",
    "chronic cough", "respiratory failure", "sleep apnea", "obstructive sleep apnea",
    "central sleep apnea", "hyperventilation", "hypoxia", "asphyxia",
    "acute bronchitis", "chronic bronchitis", "RSV", "influenza", "Legionnaires' disease",
    "Hantavirus pulmonary syndrome", "COVID-19", "SARS", "MERS"

    "ARDS",
"COVID-19",
"Breathing exercises",
"Clinical notes",
"Cough",
"Deep breath",
"Deoxygenation",
"Diagnosis",
"Dyspnea",
"Infection",
"Lungs",
"Oxygen desaturation",
"Oxygen saturation",
"Physical therapy",
"Prone position",
"Pulmonary",
"Rehabilitation",
"Respiratory",
"Respiratory failure",
"Symptoms",
"Therapy",
"Treatment",
"Ventilation",
]

# Create a regex pattern
medical_pattern = r"\b(" + "|".join(medical_terms) + r")\b"

# Function to extract medical terms using regex
def extract_medical_terms(text):
    return re.findall(medical_pattern, text, re.IGNORECASE)

# Apply regex extraction to DataFrame
sample_df['extracted_medical_terms'] = sample_df['processed_text'].apply(extract_medical_terms)

# Print extracted terms
print(sample_df['processed_text'], sample_df['extracted_medical_terms'])

print(sample_df[['processed_text', 'age', 'gender','extracted_medical_terms']])

sample_df['extracted_medical_terms_str'] = sample_df['extracted_medical_terms'].apply(' '.join)
(sample_df['extracted_medical_terms_str'].head(17))

categories = {
    "diseases": [
        "diabetes", "hypertension", "stroke", "cancer", "asthma", "tuberculosis",
        "heart attack", "lung infection", "pneumonia", "arthritis", "osteoporosis",
        "kidney disease", "liver failure", "migraine", "epilepsy", "Alzheimer", "Parkinson",
        "bronchitis", "COPD", "emphysema", "pulmonary fibrosis", "cystic fibrosis",
        "pulmonary embolism", "ARDS", "interstitial lung disease", "sarcoidosis",
        "pleurisy", "pulmonary hypertension", "pneumothorax", "respiratory failure",
        "RSV", "influenza", "Legionnaires' disease", "Hantavirus pulmonary syndrome",
        "COVID-19", "SARS", "MERS"
    ],

    "symptoms": [
        "fever", "cough", "sore throat", "chest pain", "shortness of breath",
        "dizziness", "fatigue", "nausea", "vomiting", "headache", "muscle pain",
        "skin rash", "irregular heartbeat", "vision loss", "weight loss", "obesity",
        "dyspnea", "wheezing", "chronic cough", "sleep apnea", "obstructive sleep apnea",
        "central sleep apnea", "hyperventilation", "hypoxia", "asphyxia",
        "oxygen desaturation", "oxygen saturation", "deoxygenation"
    ],

    "treatments": [
        "aspirin", "insulin", "inhaler", "antibiotics", "chemotherapy", "radiation therapy",
        "physical therapy", "painkillers", "antidepressants", "antihistamines", "surgery",
        "dialysis", "vaccine", "blood transfusion", "breathing exercises", "rehabilitation",
        "therapy", "ventilation", "prone position", "treatment"
    ],

    "medical_tests": [
        "MRI scan", "CT scan", "X-ray", "ECG", "blood test", "urine test", "biopsy",
        "endoscopy", "ultrasound", "PET scan", "colonoscopy"
    ],

    "general_medical_terms": [
        "infection", "lungs", "pulmonary", "respiratory", "clinical notes", "diagnosis",
        "symptoms"
    ]
}

# Print categorized terms
for category, terms in categories.items():
    print(f"\n{category.upper()} ({len(terms)} terms):")
    print(", ".join(terms))

# Create regex patterns for each category
patterns = {category: r"\b(" + "|".join(terms) + r")\b" for category, terms in categories.items()}


def classify_medical_terms(text):
    extracted = {"diseases": [], "symptoms": [], "treatments": [], "medical_tests": []}
    for category, pattern in patterns.items():
        extracted[category] = re.findall(pattern, text, re.IGNORECASE)
    return extracted


# Apply classification function
sample_df['classified_medical_terms'] = sample_df['extracted_medical_terms_str'].apply(classify_medical_terms)

# Print results
print(sample_df[['classified_medical_terms']].head(10))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import RandomOverSampler

# Ensure 'sample_df' exists
if 'sample_df' not in locals():
    raise ValueError("Dataset 'sample_df' is not defined!")

# Remove 'Unknown' diseases
filtered_df = sample_df[sample_df['classified_medical_terms'].apply(lambda x: x['diseases'][0] if x['diseases'] else None).notna()]

# Randomly sample up to 1000 records (optional)
sampled_df = filtered_df.sample(n=1000, random_state=42) if len(filtered_df) > 1000 else filtered_df

# Prepare Text Features (TF-IDF)
vectorizer = TfidfVectorizer(
    max_df=0.9,
    min_df=5,
    ngram_range=(1,2),
    stop_words='english'
)
X = vectorizer.fit_transform(sampled_df['classified_medical_terms'].apply(lambda x: ' '.join(x['symptoms'])))
y = sampled_df['classified_medical_terms'].apply(lambda x: x['diseases'][0])

# Apply Random Over-Sampling to Balance Classes
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Model Training
model = MultinomialNB()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Function for Predicting Diseases
def predict_disease(symptoms):
    cleaned_symptoms = " ".join(symptoms.split(", "))  # Simple text cleaning
    vectorized_input = vectorizer.transform([cleaned_symptoms])
    prediction = model.predict(vectorized_input)
    return prediction[0]

# Example Prediction
new_symptoms = "fever, cold, fatigue"
predicted_disease = predict_disease(new_symptoms)
print("Predicted Disease:", predicted_disease)

# Symptom Binarization for Visualization
mlb_symptoms = MultiLabelBinarizer()
X_binarized = mlb_symptoms.fit_transform(sampled_df['classified_medical_terms'].apply(lambda x: x['symptoms']))

# Visualization: Disease Counts After Oversampling
plt.figure(figsize=(12, 6))
sns.countplot(y=y_resampled, order=y_resampled.value_counts().index, palette='Set2')
plt.title('Disease Distribution in Oversampled Dataset')
plt.xlabel('Disease')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

import joblib

# Save the trained model and vectorizer
joblib.dump(model, "predict_disease.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

"""age:**bold text**"""

def determine_high_risk(row):

    severe_symptoms = [
        "shortness of breath", "chest pain", "irregular heartbeat",
        "Loss of consciousness", "Seizures", "Sudden confusion",
        "Severe headache", "High fever", "Uncontrolled bleeding",
        "Severe allergic reaction", "Persistent vomiting", "Severe abdominal pain",
        "Weakness or numbness", "Rapid or irregular heartbeat", "Severe burns",
        "Inability to urinate", "Bluish lips or nails", "Severe back pain",
        "Mental status changes", "Persistent dizziness", "Extreme fatigue","dyspnea"
        "wheezing", "chronic cough", "sleep apnea", "obstructive sleep apnea",
        "central sleep apnea", "hyperventilation", "hypoxia", "asphyxia",
        "oxygen desaturation", "oxygen saturation", "deoxygenation",
        "sore throat", "dizziness", "fatigue", "nausea", "vomiting", "headache", "muscle pain",
        "skin rash", "irregular heartbeat", "vision loss", "weight loss", "obesity"
    ]

    # Ensure keys exist before accessing them
    symptoms = row.get('classified_medical_terms', {}).get('symptoms', [])
    age = row.get('age', None)


    # Check if the person has multiple severe symptoms
    if sum(symptom in symptoms for symptom in severe_symptoms) >= 2:
        return 1

    # Check if age is above 65 (elderly risk factor)
    if age is not None and age >= 65:
        return 1

    return 0

# Apply function to DataFrame
sample_df['high_risk'] = sample_df.apply(determine_high_risk, axis=1)

# Print high-risk cases
print(sample_df[['processed_text', 'age', 'classified_medical_terms', 'high_risk']].head(25))

# Create a new column called symptoms
sample_df['symptoms'] = sample_df['classified_medical_terms'].apply(lambda x: x['symptoms'])
print(sample_df[['processed_text', 'age', 'symptoms', 'high_risk']].head(25))

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Prepare features (X) and target (y)
X = mlb_symptoms.fit_transform(sample_df['classified_medical_terms'].apply(lambda x: x['symptoms']))
y = sample_df['high_risk']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict on Test Set
y_pred = rf_model.predict(X_test)

# Evaluate Model
print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model and the MultiLabelBinarizer
joblib.dump(rf_model, 'determine_high_risk.pkl')
joblib.dump(mlb_symptoms, 'mlb_symptoms.pkl')

# Print sample high-risk predictions
print(sample_df[['age', 'classified_medical_terms', 'high_risk']])



print(sample_df['high_risk'].value_counts())  # Count High vs. Low Risk cases




# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# # Paste the above Streamlit code here
import joblib
import streamlit as st
import plotly.express as px
import pandas as pd
import urllib.parse
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load Models and Multi-Label Binarizer
rf_model = joblib.load("determine_high_risk.pkl")
mlb_symptoms = joblib.load("mlb_symptoms.pkl")
disease_model = joblib.load("predict_disease.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")
HOSPITAL_EMAIL = "chhaviel04@gmail.com"

CLIENT_ID = "************************************"
CLIENT_SECRET = "********************************"
REFRESH_TOKEN = "*****************************************"
YOUR_GMAIL = "chhavichadha07@gmail.com"

# ✅ Gmail API Authentication
def authenticate_gmail():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    return build("gmail", "v1", credentials=creds)

# ✅ Function to Send High-Risk Alert Email
def send_high_risk_email(patient_id, name, number, age, gender, symptoms, risk_level):
    service = authenticate_gmail()

    subject = "🚨 Emergency Alert: High-Risk Patient"
    body = f"""
    ⚠️ High-Risk Patient Report ⚠️

    Patient ID: {patient_id}
    Name: {name}
    Mobile: {number}
    Age: {age}
    Gender: {gender}
    Symptoms: {', '.join(symptoms)}
    Risk Level: {risk_level}

    Please take necessary action.
    """

    msg = MIMEMultipart()
    msg["From"] = YOUR_GMAIL
    msg["To"] = YOUR_GMAIL  # Change if sending to a doctor/hospital email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    message = {"raw": raw_message}

    try:
        service.users().messages().send(userId="me", body=message).execute()
        print(f"✅ Email sent successfully to {YOUR_GMAIL}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# High-risk assessment function
import numpy as np
import pandas as pd

def determine_high_risk(symptoms, age):
    try:
        # Ensure symptoms are a list
        if not isinstance(symptoms, list):
            symptoms = [symptoms]

        # Convert symptoms into binary format using the trained mlb_symptoms
        symptoms_vectorized = mlb_symptoms.transform([symptoms])

        # Convert to dense array if necessary
        if hasattr(symptoms_vectorized, 'toarray'):
            symptoms_vectorized = symptoms_vectorized.toarray()

        # Make a prediction with the trained RandomForest model
        prediction = rf_model.predict(symptoms_vectorized)

        # Return high or low risk based on the model's prediction
        return "High Risk" if prediction[0] == 1 else "Low Risk"

    except Exception as e:
        print(f"Error in determine_high_risk: {e}")
        raise e






# Initialize Session State for Patient Reports
if 'patient_reports' not in st.session_state:
    st.session_state.patient_reports = []

# Set Background Image for Homepage
def set_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("/content/Untitled design (7).png");
            background-size: 200px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



def predict_disease(symptoms_string):
    try:
        # Ensure input is a clean, properly formatted string
        symptoms_list = [s.strip() for s in symptoms_string.split(',') if s.strip()]

        if not symptoms_list:
            return "Unknown Disease"  # Handle empty input safely

        # Convert symptoms into a single string (expected format for vectorizer)
        symptoms_transformed = vectorizer.transform([" ".join(symptoms_list)])

        # Convert sparse matrix to dense array if necessary
        if hasattr(symptoms_transformed, 'toarray'):
            symptoms_transformed = symptoms_transformed.toarray()

        # Make prediction using trained model
        prediction = model.predict(symptoms_transformed)

        # Ensure prediction is extracted properly
        if isinstance(prediction, (list, np.ndarray)):
            predicted_disease = prediction[0]  # Extract first element
        else:
            predicted_disease = prediction

        return predicted_disease

    except Exception as e:
        print(f"Error in predict_disease: {e}")  # Debugging error messages
        import traceback
        traceback.print_exc()
        return "Unknown Disease"


# Homepage
def homepage():
    set_bg_image()
    st.title("🏥 Welcome to Mediboard")
    st.write("This platform allows patients to securely submit their health details and symptoms for risk assessment by medical professionals.")

# Visualization Board
def visualization_board():
    st.title("📊 Health Analysis Dashboard")
    if len(st.session_state.patient_reports) == 0:
        st.warning("No patient data available for analysis.")
        return

    df = pd.DataFrame(st.session_state.patient_reports, columns=["Patient ID", "Name", "Mobile.no", "Age", "Gender", "Symptoms", "Risk Level"])

    symptom_counts = df["Symptoms"].explode().value_counts()
    fig1 = px.bar(symptom_counts, x=symptom_counts.index, y=symptom_counts.values, title="Most Common Symptoms")

    risk_counts = df["Risk Level"].value_counts()
    fig2 = px.pie(names=risk_counts.index, values=risk_counts.values, title="Risk Level Distribution")

    fig3 = px.box(df, x="Risk Level", y="Age", title="Age Distribution by Risk levels")



    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)


# Patient Dashboard
def patient_dashboard():
    st.title("🩺 Patient Information")
    name = st.text_input("Enter Patient Name")
    number = st.text_input("Enter Mobile.no")
    age = st.number_input("Enter Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Enter Gender", ["M", "F", "Other"])
    symptoms = st.text_area("Enter Symptoms (comma-separated)")

    if st.button("Submit"):
      if symptoms:
        symptoms_list = [s.strip() for s in symptoms.split(',')]

        # Use the trained model for risk assessment
        high_risk = determine_high_risk(symptoms_list, age)

        patient_id = len(st.session_state.patient_reports) + 1
        st.session_state.patient_reports.append([patient_id, name, number, age, gender, symptoms_list, high_risk])

        st.write("### Patient Summary")
        st.write(f"**Patient ID:** {patient_id}")
        st.write(f"**Name:** {name}")
        st.write(f"**Mobile.no:** {number}")
        st.write(f"**Age:** {age}")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Symptoms:** {', '.join(symptoms_list)}")
        st.write(f"**Risk Level:** {high_risk}")

        if high_risk == "High Risk":
          email_subject = "!!Emergency Alert: High-Risk Patient"
          email_body = f"""
                SEND YOUR REPORT TO MEDICARE.\n
                FROM:{name}\n
                Patient ID: {patient_id}\n
                Name: {name}\n
                Mobile.no: {number}\n
                Age: {age}\n
                Gender: {gender}\n
                Symptoms: {', '.join(symptoms_list)}\n
                Risk Level: {high_risk}\n
                Please take
                necessary action.
                """
          st.error("!! We had sent your report to doctor for evaluation !!.")
          send_high_risk_email(patient_id, name, number, age, gender, symptoms_list, high_risk)
          st.success("🚨 Email sent to the hospital for review, We will get in touch with you soon! ")



# Doctor Dashboard
def doctor_dashboard():
    st.title("👨‍⚕️ Doctor Dashboard")
    if len(st.session_state.patient_reports) == 0:
        st.warning("No patient reports available.")
        return
    df = pd.DataFrame(st.session_state.patient_reports, columns=["Patient ID", "Name", "Mobile.no", "Age", "Gender", "Symptoms", "Risk Level"])
    st.dataframe(df)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Healthcare Analytics Panel", "Health Assessment Portal", "Clinical Insights Hub"])
if page == "Home":
    homepage()
elif page == "Healthcare Analytics Panel":
    visualization_board()
elif page == "Health Assessment Portal":
    patient_dashboard()
elif page == "Clinical Insights Hub":
    doctor_dashboard()







