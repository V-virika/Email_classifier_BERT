import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report 
import pickle
from pii_masker import mask_pii

# Load dataset
df = pd.read_csv("combined_emails_with_natural_pii.csv")

# Mask PII
masked_results = df['email'].apply(lambda x: mask_pii(x))
df['masked_email'] = masked_results.apply(lambda x: x[0])
df['pii_entities'] = masked_results.apply(lambda x: x[1])

# Vectorize
X = df['masked_email']
y = df['type']
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

print(classification_report(y_test, clf.predict(X_test)))

# Save models
pickle.dump(clf, open("classifier.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
