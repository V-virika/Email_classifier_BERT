import pandas as pd
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch
import pickle
from pii_masker import mask_pii

print("📦 Step 1: Reading CSV...")
df = pd.read_csv("combined_emails_with_natural_pii.csv")

# ✅ Take only 10% of the data early on
print("📉 Step 2: Sampling 10% of the dataset for quick training...")
df = df.sample(frac=0.1, random_state=42).reset_index(drop=True)

print("🛡️ Step 3: Masking emails using pii_masker...")
df['masked_email'] = df['email'].apply(lambda x: mask_pii(x)[0])

print("🏷️ Step 4: Encoding target labels...")
le = LabelEncoder()
df['label'] = le.fit_transform(df['type'])

print("🔠 Step 5: Tokenizing with BERT tokenizer...")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize(batch):
    return tokenizer(batch['masked_email'], truncation=True, padding=True)

dataset = Dataset.from_pandas(df[['masked_email', 'label']])
dataset = dataset.train_test_split(test_size=0.2)  # 80% train, 20% test

print("🧹 Step 6: Mapping tokens and setting format...")
dataset = dataset.map(tokenize, batched=True)
dataset.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])

print("🧠 Step 7: Loading BERT model for sequence classification...")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(le.classes_))

print("⚙️ Step 8: Configuring training arguments...")
training_args = TrainingArguments(
    output_dir='./bert-results',
    per_device_train_batch_size=4,  # Keep this low
    num_train_epochs=2,  # Keep epochs low for faster execution
    logging_dir='./logs',
    logging_steps=10,
    dataloader_pin_memory=False,
)

print("🚀 Step 9: Initializing Hugging Face Trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['test']
)

print("🧪 Step 10: Starting training...")
trainer.train()

print("💾 Step 11: Saving fine-tuned model and tokenizer...")
model.save_pretrained("./bert_model")
tokenizer.save_pretrained("./bert_model")

print("💾 Step 12: Saving LabelEncoder...")
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ Training complete! Model saved in ./bert_model, labels in label_encoder.pkl")

