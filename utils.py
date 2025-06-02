import re

def mask_pii(email_body: str) -> dict:
    masked_email = email_body
    list_of_masked_entities = []

    pii_patterns = {
        "full_name": r"\b[A-Z][a-z]+(?: [A-Z][a-z]+){1,3}\b",
        "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
        "phone_number": r"\b(?:\+?\d{1,3}[-.●]?)?\(?\d{3}\)?[-.●]?\d{3}[-.●]?\d{4}\b",
        "dob": r"\b(?:0?[1-9]|[12]\d|3[01])[-/.](?:0?[1-9]|1[0-2])[-/.](?:19|20)\d{2}\b",
        "aadhar_num": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
        "cvv_no": r"\b\d{3,4}\b",
        "expiry_no": r"\b(?:0[1-9]|1[0-2])\/?([0-9]{2})\b"
    }

    replacements = []
    for entity_type, pattern in pii_patterns.items():
        for match in re.finditer(pattern, email_body):
            original_entity = match.group(0)
            start, end = match.span()

            replacements.append({
                "start": start,
                "end": end,
                "replacement_tag": f"[{entity_type}]",
                "original_entity": original_entity,
                "classification": entity_type
            })

    replacements.sort(key=lambda x: x['start'], reverse=True)

    final_masked_email = list(email_body)
    final_list_of_masked_entities = []

    for rep in replacements:
        start = rep['start']
        end = rep['end']
        replacement_tag = rep['replacement_tag']

        final_masked_email[start:end] = list(replacement_tag)

        final_list_of_masked_entities.append({
            "position": [start, end],
            "classification": rep['classification'],
            "entity": rep['original_entity']
        })

    final_masked_email_str = "".join(final_masked_email)

    final_list_of_masked_entities.sort(key=lambda x: x['position'][0])

    return {
        "masked_email": final_masked_email_str,
        "list_of_masked_entities": final_list_of_masked_entities
    }

if __name__ == "__main__":
    test_email = "Hello, my name is John Doe, and my email is johndoe@example.com. My phone is +1-555-123-4567. Date of birth: 01/10/1985. Aadhar number: 1234 5678 9012. My card is 1234-5678-1234-5678, CVV 123, expiry 12/25."
    result = mask_pii(test_email)
    print("Original Email:\n", test_email)
    print("\nMasked Email:\n", result["masked_email"])
    print("\nMasked Entities:\n", result["list_of_masked_entities"])

    test_email_2 = "Account issue for Jane Smith (jane.smith@org.com). Contact at (987)654-3210. Card ending 4321."
    result_2 = mask_pii(test_email_2)
    print("\n---\nOriginal Email 2:\n", test_email_2)
    print("\nMasked Email 2:\n", result_2["masked_email"])
    print("\nMasked Entities 2:\n", result_2["list_of_masked_entities"])