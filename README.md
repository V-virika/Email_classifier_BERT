---
title: Email Classification with BERT
emoji: ✉️
colorFrom: indigo
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---
# ✉️ Email Classification API with BERT (PII Masking Enabled)

This project is a FastAPI-based RESTful API that:

🔐 Masks Personally Identifiable Information (PII)  
🤖 Classifies email content using a fine-tuned BERT model  
📦 Returns structured results in JSON format

---

## 🚀 API Features

- **POST `/classify`**
  - Input: Email body as plain text
  - Output: Masked version + PII entity list + Predicted category

---

## 📊 Categories Predicted

The model classifies emails into the following support types:

- `Incident`
- `Request`
- `Change`
- `Problem`

---

## 🔐 PII Masking Includes

- Full names (`PERSON`)
- Phone numbers
- Emails
- Aadhaar
- Credit/Debit numbers
- CVV, Expiry
- Dates of Birth

---

## 📤 Example Input

```json
{
  "input_email_body": "Hi, I’m John. My number is 9876543210. I need help with billing."
}
