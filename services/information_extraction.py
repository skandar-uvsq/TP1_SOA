import spacy
import re
from ..utils.db import load_data

nlp = spacy.load("en_core_web_sm")


def extract_infos(text: str):
    extracted_data = {"personal_information": {}, "property_details": {}}
    doc = nlp(text)
    # ---------------- Personal information
    # ---- Name
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            extracted_data["personal_information"]["name"] = ent.text
            break

    # ---- email
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    match = email_pattern.search(text)
    if match:
        extracted_data["personal_information"]["email"] = match.group()

    # ---- phone
    phone_pattern = re.compile(r"\+?\d[\d\s-]{8,}\d")
    match = phone_pattern.search(text)
    if match:
        extracted_data["personal_information"]["phone_number"] = match.group()

    # ---------------- Property details
    # ---- address
    address_pattern = re.compile(
        r"\d+\s[\w\s\-]+,\s\d{5}\s[\w\s\-]+,\s[\w\s\-\°]+,\s[\w\s\-\°]+"
    )
    match = address_pattern.search(text)
    if match:
        extracted_data["property_details"]["address"] = match.group()

    # ---- surface
    surface_pattern = re.compile(r"\b\d+(?:\.\d+)?m²\b")
    match = surface_pattern.search(text)
    if match:
        extracted_data["property_details"]["surface"] = match.group()

    # ---- loan amount
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            extracted_data["property_details"]["loan_amount"] = ent.text

    # ---- description
    description = []
    for token in doc:
        # Check if the token is an adjective
        if token.pos_ == "ADJ":
            # Find the noun that follows the adjective
            if token.head.pos_ == "NOUN":
                extracted_data["property_details"]["description"] = ent.text
                description.append(f"{token.text} {token.head.text}")
    extracted_data["property_details"]["description"] = description
    load_data(data=extracted_data)


for i in range(1, 6):
    with open(file=f"TP1_SOAP/sample_data/{i}.txt", encoding="utf-8") as f:
        text = f.read()
        extract_infos(text=text)
