import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

def preprocess_text(text):
    """Clean and preprocess ticket text."""
    # 1. Lowercase
    text = text.lower()
    # 2. Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # 3. Tokenize
    tokens = word_tokenize(text)
    # 4. Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Rejoin tokens
    return ' '.join(tokens)

def main():
    file_path = 'support_tickets_synthetic.csv'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run generate_dummy_data.py first.")
        return

    print("Loading data...")
    df = pd.read_csv(file_path)
    
    print("\n--- Initial Data Sample ---")
    print(df.head())
    
    print("\nPreprocessing text data...")
    df['cleaned_text'] = df['ticket_text'].apply(preprocess_text)
    
    # 1. Split data for Category Classification
    print("\n--- Training Category Classifier ---")
    X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
        df['cleaned_text'], df['category'], test_size=0.2, random_state=42
    )

    # Feature Extraction (TF-IDF)
    tfidf_cat = TfidfVectorizer(max_features=5000)
    X_train_cat_tfidf = tfidf_cat.fit_transform(X_train_cat)
    X_test_cat_tfidf = tfidf_cat.transform(X_test_cat)
    
    # Train Category Model
    rf_cat = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_cat.fit(X_train_cat_tfidf, y_train_cat)
    
    # Evaluate Category Model
    y_pred_cat = rf_cat.predict(X_test_cat_tfidf)
    print("Category Accuracy:", accuracy_score(y_test_cat, y_pred_cat))
    print("\nCategory Classification Report:")
    print(classification_report(y_test_cat, y_pred_cat))
    
    # 2. Split data for Priority Classification
    print("\n--- Training Priority Classifier ---")
    X_train_pri, X_test_pri, y_train_pri, y_test_pri = train_test_split(
        df['cleaned_text'], df['priority'], test_size=0.2, random_state=42
    )

    # Feature Extraction (TF-IDF)
    tfidf_pri = TfidfVectorizer(max_features=5000)
    X_train_pri_tfidf = tfidf_pri.fit_transform(X_train_pri)
    X_test_pri_tfidf = tfidf_pri.transform(X_test_pri)
    
    # Train Priority Model
    rf_pri = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_pri.fit(X_train_pri_tfidf, y_train_pri)
    
    # Evaluate Priority Model
    y_pred_pri = rf_pri.predict(X_test_pri_tfidf)
    print("Priority Accuracy:", accuracy_score(y_test_pri, y_pred_pri))
    print("\nPriority Classification Report:")
    print(classification_report(y_test_pri, y_pred_pri))
    
    # Visualizing the Confusion Matrix for Category
    plt.figure(figsize=(8, 6))
    cm_cat = confusion_matrix(y_test_cat, y_pred_cat)
    sns.heatmap(cm_cat, annot=True, fmt='d', cmap='Blues', 
                xticklabels=rf_cat.classes_, yticklabels=rf_cat.classes_)
    plt.title('Confusion Matrix - Category')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig('confusion_matrix_category.png')
    print("\nSaved Category Confusion Matrix to 'confusion_matrix_category.png'")
    
    # Test with a custom string
    print("\n--- Live Prediction Test ---")
    sample_ticket = "Hi support, my credit card payment failed twice, please help me fix this urgently!"
    cleaned_sample = preprocess_text(sample_ticket)
    
    sample_cat_tfidf = tfidf_cat.transform([cleaned_sample])
    sample_pri_tfidf = tfidf_pri.transform([cleaned_sample])
    
    pred_category = rf_cat.predict(sample_cat_tfidf)[0]
    pred_priority = rf_pri.predict(sample_pri_tfidf)[0]
    
    print(f"Ticket: '{sample_ticket}'")
    print(f"Predicted Category: {pred_category}")
    print(f"Predicted Priority: {pred_priority}")

if __name__ == "__main__":
    main()
