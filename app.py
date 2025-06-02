from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import pickle
from pii_masker import mask_pii

# Load model, tokenizer, label encoder from bert_model/ directory
model = BertForSequenceClassification.from_pretrained("./bert_model")
tokenizer = BertTokenizer.from_pretrained("./bert_model")
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

app = FastAPI()

# Input format
class EmailInput(BaseModel):
    input_email_body: str

# POST /classify route
@app.post("/classify")
def classify_email(email: EmailInput):
    original = email.input_email_body

    # Step 1: Mask PII
    masked_text, entities = mask_pii(original)

    # Step 2: Tokenize & classify
    inputs = tokenizer(masked_text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=1).item()
    label = label_encoder.inverse_transform([predicted_class_id])[0]

    # Step 3: Return structured result
    return {
        "input_email_body": original,
        "list_of_masked_entities": entities,
        "masked_email": masked_text,
        "category_of_the_email": label
    }

# Run locally on port 7860
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860)
