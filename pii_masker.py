import re
import spacy 

nlp = spacy.load("en_core_web_sm")

def mask_pii(text):
    doc = nlp(text)
    masked_text = text
    entities = []

    # spaCy NER
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            masked_text = masked_text.replace(ent.text, "[full_name]")
            entities.append({
                "position": [ent.start_char, ent.end_char],
                "classification": "full_name",
                "entity": ent.text
            })

    # Regex
    patterns = {
        "email": r"\b[\w.-]+?@\w+?\.\w+?\b",
        "phone_number": r"\b(?:\+91[-\s]?|0)?[6-9]\d{9}\b",
        "aadhar_num": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
        "cvv_no": r"\b\d{3}\b",
        "expiry_no": r"\b(0[1-9]|1[0-2])\/?([0-9]{2}|[0-9]{4})\b",
        "dob": r"\b(?:\d{1,2}[-/]){2}\d{2,4}\b"
    }

    for label, pattern in patterns.items():
        for match in re.finditer(pattern, masked_text):
            start, end = match.start(), match.end()
            original = match.group()
            masked_text = masked_text.replace(original, f"[{label}]")
            entities.append({
                "position": [start, end],
                "classification": label,
                "entity": original
            })

    return masked_text, entities
