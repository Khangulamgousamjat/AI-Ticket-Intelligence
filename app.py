from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# Ensure NLTK packages are loaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

print("Training Machine Learning Models on Startup. Please wait...")

# Global Model Variables
rf_cat = None
rf_pri = None
tfidf_cat = None
tfidf_pri = None
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

try:
    df = pd.read_csv('support_tickets_synthetic.csv')

    df['cleaned_text'] = df['ticket_text'].apply(preprocess_text)
    
    # Train Category Classifier
    tfidf_cat = TfidfVectorizer(max_features=5000)
    X_cat_tfidf = tfidf_cat.fit_transform(df['cleaned_text'])
    rf_cat = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_cat.fit(X_cat_tfidf, df['category'])
    
    # Train Priority Classifier
    tfidf_pri = TfidfVectorizer(max_features=5000)
    X_pri_tfidf = tfidf_pri.fit_transform(df['cleaned_text'])
    rf_pri = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_pri.fit(X_pri_tfidf, df['priority'])
    
    print("✅ Models initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing models: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')
    if not text.strip():
        return jsonify({'error': 'Empty text query provided.'})
        
    cleaned = preprocess_text(text)
    
    try:
        cat_pred = rf_cat.predict(tfidf_cat.transform([cleaned]))[0]
        pri_pred = rf_pri.predict(tfidf_pri.transform([cleaned]))[0]
        
        return jsonify({
            'success': True,
            'category': str(cat_pred),
            'priority': str(pri_pred)
        })
    except Exception as e:
         return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
