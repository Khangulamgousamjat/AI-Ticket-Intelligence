# Support Ticket Classification & Prioritization Pipeline

I have successfully built a dedicated Machine Learning pipeline for Support Ticket Classification and Prioritization. 

This system acts as a decision-support module that automates:
1. **Reading support tickets:** Cleans raw text data using NLTK to remove noise (stop words, punctuation, etc.).
2. **Text Vectorization:** Converts unstructured text into computational structures (TF-IDF mapping).
3. **Multi-label Prediction:** Uses `Scikit-Learn`'s Random Forest algorithms to classify **Category** and predict **Priority**.

## 🛠️ The Implementation
The solution consists of three main files located in **`b:/FUTURE_ML_02/support_ticket_classification/`**:

1. **`requirements.txt`**: Essential dependencies (pandas, scikit-learn, nltk, matplotlib, seaborn).
2. **`generate_dummy_data.py`**: A helper script I built to bypass Kaggle API restrictions and give you an immediate sandbox. It auto-generates 1,000 synthetic, realistic tickets across categories like Billing, Technical Issue, Account, and General Query.
3. **`ticket_classification.py`**: The core NLP pipeline that trains the dual Machine Learning models.

### How the Pipeline Works:
- **Preprocessing:** 
   ```python
   # Lowercasing, punctuation stripping, word tokenization, and stop-word filtering
   tokens = [word for word in word_tokenize(text.lower()) if word not in stop_words]
   ```
- **Feature Extraction:** Standardized `TfidfVectorizer(max_features=5000)` creates a Bag of Words / TF-IDF sparse matrix representation of tickets.
- **Classification Engine:** Deploys a robust `RandomForestClassifier` for its ability to avoid overfitting in sparse NLP arrays out-of-the-box.
- **Evaluation:** Performs standard `train_test_split` validation, reporting classification accuracy alongside an exported Confusion Matrix heatmap.

## 📊 Live Sample Demonstration
When I fed the trained model the following **unseen, noisy string**:
> *"Hi support, my credit card payment failed twice, please help me fix this urgently!"*

**The Model Predicted:**
* **Category:** Billing
* **Priority:** High

## 📂 Changing The Dataset

The system works cleanly on the synthetic dataset, but it is modular by design. To use one of the datasets you acquired from Kaggle (e.g., *Customer Support Ticket Dataset*):

1. Download the Kaggle `.csv` dataset and place it in the project folder.
2. Open `ticket_classification.py`.
3. Update `file_path = 'your_kaggle_dataset.csv'`.
4. Ensure the target dataframe columns map to `['ticket_text', 'category', 'priority']`, renaming them via `pandas` if necessary!
```python
# Quick rename logic template if needed:
df.rename(columns={'Customer_Message': 'ticket_text', 'Issue_Type': 'category', 'Ticket_Priority': 'priority'}, inplace=True)
```

## 📸 Artifacts Generated
- The execution generated the synthetic dataset: `support_tickets_synthetic.csv`.
- The confusion matrix was output as an image: `confusion_matrix_category.png`.

> **Performance Edge:** As you transition to the real IT Ticket datasets (which contain much messier real-world slang), consider swapping out `RandomForest` for a `LinearSVC` algorithm (Support Vector Classifier), as it often demonstrates superior accuracy in high-dimensional TF-IDF NLP spaces!
