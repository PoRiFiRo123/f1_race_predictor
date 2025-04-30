import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix
from app.data_preprocessor import preprocess_data
from app.model_trainer import train_and_save_model

def load_model():
    clf = joblib.load('./models/race_winner_model.pkl')
    return clf

def display_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    st.pyplot(fig)

def model_dashboard():
    st.title("🧠 Model Training Dashboard")

    # Load data
    X, y, _, _ = preprocess_data('./data/raw_data.csv')

    # Load model
    clf = load_model()

    # Predict
    y_pred = clf.predict(X)

    # Accuracy
    accuracy = accuracy_score(y, y_pred)
    st.write(f"**Model Accuracy:** {accuracy:.2f}")

    # Confusion Matrix
    st.write("**Confusion Matrix:**")
    display_confusion_matrix(y, y_pred)

    # Retrain model
    if st.button("Retrain Model"):
        train_and_save_model()
        st.success("Model retrained and saved successfully.")
