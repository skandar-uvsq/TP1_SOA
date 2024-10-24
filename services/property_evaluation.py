import json
import random
from .information_extraction import extract_infos

market_prices = {"paris": 30, "lyon": 18, "cean": 5}

property_conditions = {
    "good": 1.0,  # No deduction
    "average": 0.9,  # 10% deduction
    "poor": 0.8,  # 20% deduction
}

legal_compliance = {
    "compliant": 1.0,
    "non_compliant": 0.5,  # Property not fully compliant has a lower value
}


# This function simulates whether the property is legally compliant or not
def is_legally_compliant(address: str) -> bool:
    """
    Based on the exact address of the property, this function will do some requests
    to external sources and return whether it is legally compliant or not.
    Here just for simulation, we return a random value.
    """
    return random.choice([True, False])


# Main function to estimate the property value
def evaluate_property(address: str, region: str, area_sqm: int, condition: str):
    price_per_sqm = market_prices.get(region.lower())
    condition_multiplier = property_conditions.get(condition, "average")
    is_compliant = is_legally_compliant(address="")
    compliance_multiplier = (
        legal_compliance["compliant"]
        if is_compliant
        else legal_compliance["non_compliant"]
    )
    estimated_value = (
        area_sqm * price_per_sqm * condition_multiplier * compliance_multiplier
    )
    print(f"Estimated property monthly cost ==> {estimated_value}")
    return estimated_value


# Test
# region = "paris"  # Chosen region
# area_sqm = 100  # Property area in square meters
# condition = "average"  # Property condition
# is_compliant = True  # Compliance status
# estimated_value = evaluate_property(region, area_sqm, condition, is_compliant)


# for i in range(1, 6):
#     with open(file=f"TP1_SOAP/sample_data/{i}.txt", encoding="utf-8") as f:
#         text = f.read()
#         data = extract_infos(text=text)

#     estimated_value = evaluate_property(
#         address=data["property_details"]["address"],
#         region=data["property_details"]["region"],
#         area_sqm=data["property_details"]["surface"],
#         condition=data["property_details"]["description"][-1].split(" ")[0],
#     )

#     print("Estimated monthly cost:", estimated_value)
