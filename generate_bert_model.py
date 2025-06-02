from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Create label encoder for your 4 classes
labels = ['Incident', 'Request', 'Change', 'Problem']
le = LabelEncoder()
le.fit(labels)

# Save the label encoder
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

# Download BERT tokenizer and base model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=4)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Save model and tokenizer
os.makedirs("bert_model", exist_ok=True)
model.save_pretrained("bert_model")
tokenizer.save_pretrained("bert_model")

print("✅ Pretrained model and label encoder saved.")
